"""
Retrieval Agent: Handles RAG - retrieves relevant Sinhala historical content
from ChromaDB to provide factual context for scoring.
"""
import os
# Force offline mode BEFORE importing sentence_transformers
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import chromadb
from sentence_transformers import SentenceTransformer
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL, TOP_K_RESULTS


class RetrievalAgent:
    """Agent responsible for retrieving relevant context from the knowledge base."""

    def __init__(self):
        self.embedding_model = None
        self.collection = None
        self._initialize()

    def _initialize(self):
        """Initialize the embedding model and ChromaDB connection."""
        # Load embedding model
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

        # Connect to ChromaDB
        client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def retrieve(self, question, student_answer, top_k=None):
        """
        Retrieve relevant context from the knowledge base.

        Args:
            question: The question being answered
            student_answer: The student's answer text
            top_k: Number of results to retrieve

        Returns:
            dict with retrieved documents and metadata
        """
        if top_k is None:
            top_k = TOP_K_RESULTS

        # Combine question and key parts of answer for better retrieval
        query_text = f"{question} {student_answer[:200]}"

        # Generate embedding
        query_embedding = self.embedding_model.encode(query_text).tolist()

        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        # Format results
        retrieved_docs = []
        if results and results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                distance = results["distances"][0][i] if results["distances"] else 0

                retrieved_docs.append({
                    "content": doc,
                    "source": metadata.get("source", "unknown"),
                    "chunk_id": metadata.get("chunk_id", i),
                    "similarity": round(1 - distance, 4)  # Convert distance to similarity
                })

        return {
            "agent": "RetrievalAgent",
            "status": "success",
            "query": query_text[:100] + "...",
            "num_results": len(retrieved_docs),
            "retrieved_documents": retrieved_docs
        }

    def get_context_for_scoring(self, question, student_answer):
        """
        Get formatted context string for the scoring agent.

        Returns a single string combining all retrieved documents.
        """
        result = self.retrieve(question, student_answer)

        if not result["retrieved_documents"]:
            return "No relevant context found in knowledge base."

        context_parts = ["### Retrieved Context from Knowledge Base:\n"]
        for i, doc in enumerate(result["retrieved_documents"], 1):
            context_parts.append(
                f"**[Source {i}: {doc['source']}]** (similarity: {doc['similarity']})\n"
                f"{doc['content']}\n"
            )

        return "\n".join(context_parts)
