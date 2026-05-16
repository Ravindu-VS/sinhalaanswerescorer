"""
Knowledge Base Setup Script.
Reads all Sinhala history documents, chunks them, embeds them,
and stores them in ChromaDB for RAG retrieval.
"""
import os
import sys
import glob

# Force offline mode BEFORE importing sentence_transformers
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import chromadb
from sentence_transformers import SentenceTransformer

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    DOCUMENTS_DIR, CHROMA_DB_DIR, CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
)


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            if len(para) > chunk_size:
                words = para.split()
                current_chunk = ""
                for word in words:
                    if len(current_chunk) + len(word) + 1 <= chunk_size:
                        current_chunk += word + " "
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = word + " "
            else:
                current_chunk = para + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def setup_knowledge_base():
    """Main setup function to build the ChromaDB knowledge base."""
    print("=" * 60)
    print("Setting up Sinhala History Knowledge Base")
    print("=" * 60)

    os.makedirs(CHROMA_DB_DIR, exist_ok=True)

    print("\n1. Loading embedding model: " + EMBEDDING_MODEL)
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("   [OK] Model loaded successfully")

    print("\n2. Initializing ChromaDB at: " + CHROMA_DB_DIR)
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

    try:
        client.delete_collection(CHROMA_COLLECTION_NAME)
        print("   Deleted existing collection: " + CHROMA_COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    print("   [OK] Collection created: " + CHROMA_COLLECTION_NAME)

    print("\n3. Loading documents from: " + DOCUMENTS_DIR)
    doc_files = glob.glob(os.path.join(DOCUMENTS_DIR, "*.txt"))

    if not doc_files:
        print("   [ERROR] No .txt files found!")
        return

    all_chunks = []
    all_ids = []
    all_metadatas = []
    chunk_counter = 0

    for doc_path in doc_files:
        filename = os.path.basename(doc_path)
        print("\n   Processing: " + filename)

        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()

        chunks = chunk_text(content)
        print("   -> " + str(len(chunks)) + " chunks created")

        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(filename + "_" + str(i))
            all_metadatas.append({
                "source": filename,
                "chunk_id": i,
                "total_chunks": len(chunks)
            })
            chunk_counter += 1

    print("\n4. Generating embeddings for " + str(len(all_chunks)) + " chunks...")
    embeddings = model.encode(all_chunks, show_progress_bar=True).tolist()
    print("   [OK] Embeddings generated")

    print("\n5. Storing in ChromaDB...")
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        end = min(i + batch_size, len(all_chunks))
        collection.add(
            embeddings=embeddings[i:end],
            documents=all_chunks[i:end],
            ids=all_ids[i:end],
            metadatas=all_metadatas[i:end]
        )

    print("   [OK] " + str(len(all_chunks)) + " chunks stored successfully")

    print("\n6. Verification:")
    print("   Collection count: " + str(collection.count()))

    test_query = "anuradhapura irrigation"
    test_embedding = model.encode(test_query).tolist()
    test_results = collection.query(
        query_embeddings=[test_embedding],
        n_results=2,
        include=["documents", "metadatas"]
    )
    print("   Test query: '" + test_query + "'")
    if test_results["documents"][0]:
        print("   Top result source: " + str(test_results['metadatas'][0][0].get('source', 'N/A')))
        preview = test_results['documents'][0][0][:80]
        print("   Top result preview: " + preview + "...")

    print("\n" + "=" * 60)
    print("[OK] Knowledge base setup complete!")
    print("   Total documents: " + str(len(doc_files)))
    print("   Total chunks: " + str(chunk_counter))
    print("=" * 60)


if __name__ == "__main__":
    setup_knowledge_base()
