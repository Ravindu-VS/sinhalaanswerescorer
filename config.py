"""
Configuration file for the Offline Sinhala Answer Scorer.
All paths, model names, and parameters are centralized here.
"""
import os

# --- Base Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base")
DOCUMENTS_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "documents")
CHROMA_DB_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "chroma_db")
ONTOLOGY_DIR = os.path.join(BASE_DIR, "ontology")
ONTOLOGY_FILE = os.path.join(ONTOLOGY_DIR, "anuradhapura.owl")

# --- LLM Configuration ---
OLLAMA_MODEL = "llama3:latest"  # Primary LLM for scoring
OLLAMA_BASE_URL = "http://localhost:11434"
LLM_TEMPERATURE = 0.1  # Low temperature for consistent scoring
LLM_NUM_CTX = 2048  # Reduced Context window for faster processing

# --- Embedding Model ---
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# --- RAG Configuration ---
CHROMA_COLLECTION_NAME = "sinhala_history"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 5

# --- Scoring ---
MAX_MARKS_PER_QUESTION = 20
