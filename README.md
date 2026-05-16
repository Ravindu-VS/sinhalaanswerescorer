# Sinhala Answer Scorer

An offline intelligent Sinhala open-ended answer scoring system focused on the **Anuradhapura period**.  
It combines **RAG (ChromaDB)**, **ontology reasoning (OWLReady2)**, and **LLM-based scoring (Ollama + Llama 3)** behind a Streamlit UI.

## Features

- Sinhala answer grading with criterion-level mark breakdowns
- Retrieval-augmented factual context from a local knowledge base
- Ontology-based concept coverage checking
- Multi-agent workflow:
  - `RetrievalAgent`
  - `OntologyAgent`
  - `ScoringAgent`
  - `OrchestratorAgent`
- Offline-first setup (local model + local vector DB + local ontology)

## Tech Stack

- Python
- Streamlit
- LangChain (core/community)
- ChromaDB
- sentence-transformers
- owlready2
- Ollama (`llama3:latest`)

## Project Structure

```text
.
├── app.py                       # Streamlit UI
├── config.py                    # Central configuration
├── setup_kb.py                  # Builds Chroma knowledge base from txt docs
├── test_pipeline.py             # End-to-end pipeline smoke test script
├── agents/
│   ├── orchestrator.py
│   ├── retrieval_agent.py
│   ├── ontology_agent.py
│   └── scoring_agent.py
├── marking/
│   └── marking_guides.py
├── ontology/
│   ├── ontology_loader.py
│   ├── create_ontology.py
│   └── anuradhapura.owl
└── knowledge_base/
    └── documents/*.txt
```

## Prerequisites

- Python 3.10+
- Ollama installed and running locally
- `llama3:latest` model available in Ollama

## Setup

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Pull and run Llama 3 in Ollama:

```bash
ollama pull llama3:latest
ollama serve
```

3. Build the local knowledge base:

```bash
python setup_kb.py
```

## Run the App

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit in your browser.

## Optional: Pipeline Smoke Test

```bash
python test_pipeline.py
```

This script checks retrieval, ontology analysis, scoring, and full orchestration.

## Notes

- The system is configured for offline behavior where possible (`HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`).
- Ensure Ollama is reachable at `http://localhost:11434` (see `config.py`).
