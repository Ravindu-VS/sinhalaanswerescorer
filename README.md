# 📝 Offline Intelligent Sinhala Open-Ended Answer Scorer

> An AI-powered offline system that grades Sinhala open-ended answers for History of Sri Lanka (Anuradhapura Period) using **OLLAMA + RAG + Ontology + Agent Architecture**.

## 🎯 Overview

This system evaluates student answers written in Sinhala for questions about the Anuradhapura Period of Sri Lankan history. Each answer is graded out of **20 marks** using a structured marking guide, with an **explainable score breakdown** showing exactly why marks were awarded or deducted.

### Key Features

- 🔒 **Fully Offline** — No internet connection required during execution
- 🤖 **OLLAMA-based Scoring** — Local LLM inference using `llama3:latest`
- 📚 **RAG Pipeline** — ChromaDB + multilingual sentence embeddings for context retrieval
- 🧠 **OWL Ontology** — Formal knowledge representation with concept verification
- 🏗️ **5-Agent Architecture** — Retrieval → Ontology → Scoring → Validation → Assembly
- 📊 **Explainable Scoring** — Per-criterion marks with evidence-based Sinhala justifications
- 🎨 **Streamlit UI** — Modern dark-themed interface with real-time workflow visualization

---

## 📋 Topic Scope

**Option 1: Ancient Sri Lanka (Anuradhapura Period)**

| Focus Area | Questions |
|-----------|-----------|
| Irrigation & Civilization | Q1: ජලාශ ශිෂ්ටාචාරය |
| Buddhism & Culture | Q2: බුදුදහම හඳුන්වාදීම |
| Notable Rulers & Events | Q3: ප්‍රධාන රජවරුන් |
| Administration | Q4: පරිපාලන ක්‍රමය |
| Decline & Fall | Q5: පරිහානිය |

Each question is graded out of **20 marks** using 4-5 structured criteria.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI (app.py)                     │
│        Question Selection → Answer Input → Results          │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Orchestrator Agent (orchestrator.py)            │
│              Coordinates the 5-step workflow                │
└──┬──────────┬──────────┬──────────┬──────────┬──────────────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────────┐
│Step 1│  │Step 2│  │Step 3│  │Step 4│  │  Step 5  │
│ RAG  │  │Onto- │  │Score │  │Valid-│  │ Assembly │
│Agent │  │logy  │  │Agent │  │ation │  │          │
│      │  │Agent │  │      │  │Agent │  │          │
└──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──────────┘
   │         │         │         │
   ▼         ▼         ▼         ▼
ChromaDB   OWL      OLLAMA   Cross-check
+ MiniLM  Ontology  llama3   Scores
```

### Agents

| Agent | File | Responsibility |
|-------|------|---------------|
| **Orchestrator** | `agents/orchestrator.py` | Coordinates workflow, dispatches tasks |
| **Retrieval Agent** | `agents/retrieval_agent.py` | RAG: queries ChromaDB for relevant context |
| **Ontology Agent** | `agents/ontology_agent.py` | Verifies concept coverage against OWL ontology |
| **Scoring Agent** | `agents/scoring_agent.py` | LLM scoring with evidence-based justifications |
| **Validation Agent** | `agents/validation_agent.py` | Cross-checks score consistency & bounds |

---

## 📚 RAG Pipeline

```
Documents (5 Sinhala .txt files)
    │
    ▼ chunk_text() — 500-char chunks, 100-char overlap
    │
    ▼ SentenceTransformer (paraphrase-multilingual-MiniLM-L12-v2)
    │
    ▼ ChromaDB (PersistentClient, cosine similarity)
    │
    ▼ Top-5 retrieval → Context for scoring prompt
```

### Knowledge Base Documents

| File | Topic | Size |
|------|-------|------|
| `irrigation.txt` | ජලාශ ශිෂ්ටාචාරය — Tanks, canals, agriculture | 4.5 KB |
| `buddhism.txt` | බුදුදහම — Buddhism, monasteries, culture | 5.2 KB |
| `rulers.txt` | රජවරුන් — Key rulers and contributions | 5.1 KB |
| `administration.txt` | පරිපාලනය — Administrative structure | 2.5 KB |
| `decline.txt` | පරිහානිය — Invasions and fall | 3.5 KB |

---

## 🧠 Ontology (OWL)

The ontology (`ontology/anuradhapura.owl`) formally represents 30+ entities with:

- **14 Classes**: HistoricalEntity, Ruler, Location, Structure, Tank, Canal, Stupa, Monastery, MonasticOrder, Event, Battle, Invasion, Religion, AdministrativeUnit, TimePeriod
- **9 Object Properties**: built_by, ruled_during, located_in, part_of, introduced_by, associated_with, fought_in, succeeded_by, founded_by
- **4 Data Properties**: reign_start, reign_end, significance_si, significance_en
- **30+ Individuals**: Kings, tanks, stupas, battles, monasteries with Sinhala descriptions

### Ontology Usage in Scoring

1. **Concept Coverage**: For each question, expected ontology concepts are checked against the student's answer using Sinhala keyword matching
2. **Enrichment**: Ontology relationships (e.g., `Kala_Wewa → built_by → Dhatusena`) provide factual context to the LLM
3. **Scoring Impact**: The LLM is instructed to deduct marks for missing ontology concepts and award marks for correctly mentioned ones

---

## ⚖️ Explainable Scoring

Each criterion produces:

```json
{
  "criterion_name": "ප්‍රධාන ජලාශ හඳුනාගැනීම",
  "max_marks": 5,
  "awarded_marks": 4,
  "justification_si": "Sinhala justification with quoted evidence...",
  "evidence_from_rag": "irrigation.txt — supports Kala Wewa details",
  "ontology_concepts_checked": ["Kala_Wewa", "Minneriya_Wewa", "Abhaya_Wewa"]
}
```

The Validation Agent then cross-checks:
- ✅ Score bounds (0 ≤ score ≤ max_marks)
- ✅ Total consistency (sum matches reported total)
- ✅ Criteria count (all criteria scored)
- ✅ Ontology-score cross-validation (coverage vs score alignment)
- ✅ Justification presence (all criteria justified)

---

## 🚀 Setup & Installation

### Prerequisites

- **Python 3.10+**
- **OLLAMA** installed and running locally
- **llama3** model pulled: `ollama pull llama3`

### Installation

```bash
# Clone the repository
git clone https://github.com/Ravindu-VS/sinhalaanswerescorer.git
cd sinhalaanswerescorer

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Build the knowledge base (first time only)
python setup_kb.py

# Run the application
python -m streamlit run app.py
```

### Dependencies

```
streamlit
langchain
chromadb
sentence-transformers
owlready2
requests
```

---

## 🖥️ Usage

1. **Start OLLAMA**: Ensure `ollama serve` is running
2. **Launch**: `python -m streamlit run app.py`
3. **Select a Question**: Choose from Q1-Q5 in the sidebar
4. **Enter Answer**: Type your Sinhala answer in the text area
5. **Grade**: Click "⚖️ පිළිතුර ඇගයීම කරන්න"
6. **View Results**: Score breakdown, justifications, evidence, and validation report

---

## 📁 Project Structure

```
├── app.py                          # Streamlit UI
├── config.py                       # Centralized configuration
├── setup_kb.py                     # Knowledge base builder
├── test_pipeline.py                # Pipeline test suite
├── requirements.txt                # Python dependencies
│
├── agents/                         # Agent modules
│   ├── __init__.py
│   ├── orchestrator.py             # Workflow coordinator
│   ├── retrieval_agent.py          # RAG retrieval
│   ├── ontology_agent.py           # Concept verification
│   ├── scoring_agent.py            # LLM scoring
│   └── validation_agent.py         # Score validation
│
├── knowledge_base/                 # RAG data store
│   ├── documents/                  # Sinhala source documents
│   │   ├── irrigation.txt
│   │   ├── buddhism.txt
│   │   ├── rulers.txt
│   │   ├── administration.txt
│   │   └── decline.txt
│   └── chroma_db/                  # ChromaDB persistent store
│
├── ontology/                       # OWL ontology
│   ├── anuradhapura.owl            # OWL file
│   ├── create_ontology.py          # Ontology builder
│   └── ontology_loader.py          # Query utilities
│
└── marking/                        # Marking guides
    ├── __init__.py
    └── marking_guides.py           # 5 questions with criteria
```

---

## 🧪 Testing

```bash
# Run the full pipeline test
python test_pipeline.py

# Expected output:
# [1] Testing Retrieval Agent... [OK]
# [2] Testing Ontology Agent... [OK]
# [3] Testing Scoring Agent... [OK]
# [4] Testing Orchestrator (full pipeline)... [OK]
```

---

## ⚙️ Configuration

All configuration is centralized in `config.py`:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `OLLAMA_MODEL` | `llama3:latest` | LLM model for scoring |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | OLLAMA API endpoint |
| `LLM_TEMPERATURE` | `0.1` | Low temperature for consistent scoring |
| `LLM_NUM_CTX` | `4096` | Context window size |
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | Multilingual embeddings |
| `CHUNK_SIZE` | `500` | Document chunk size (chars) |
| `TOP_K_RESULTS` | `5` | Number of retrieved documents |

---

## 📄 License

This project was developed as an individual assignment for **40_CS4032 Natural Language Processing** module.

## 👨‍💻 Author

**Ravindu Vinusha** — [GitHub](https://github.com/Ravindu-VS)
