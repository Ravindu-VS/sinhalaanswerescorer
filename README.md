# 📝 Offline Intelligent Sinhala Answer Scorer

A fully offline, agent-based AI pipeline for grading open-ended Sinhala historical answers. Built using local LLMs via Ollama, RAG (Retrieval-Augmented Generation) via ChromaDB, and ontological knowledge mapping.

## Features
- **100% Offline**: No internet connection required. Model inferences and embeddings are processed locally.
- **RAG Architecture**: Uses `sentence-transformers` and `ChromaDB` to fetch factual historical contexts from local texts.
- **Ontology Verification**: Verifies conceptual accuracy using `owlready2` against an Anuradhapura era OWL ontology.
- **Multi-Agent Design**:
  - `Retrieval Agent`: Gathers factual documents.
  - `Ontology Agent`: Maps student answers to semantic concepts.
  - `Scoring Agent`: Uses local LLMs (`gemma3:4b`) to logically grade the answer against marking criteria and produce structured JSON.
- **Modern UI**: A beautiful, dark-themed Streamlit interface.

## Prerequisites
1. **Python 3.10+**
2. **Ollama**: You must install Ollama and have the `gemma3:4b` model pulled locally.
   ```cmd
   ollama pull gemma3:4b
   ```

## Setup & Installation

1. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

2. **Initialize the Knowledge Base**
   Run the setup script to chunk, embed, and store the `.txt` files into the ChromaDB vector database.
   ```cmd
   python setup_kb.py
   ```

3. **Run the Application**
   Launch the Streamlit dashboard.
   ```cmd
   python -m streamlit run app.py
   ```

## Workflow
1. Select a Sinhala history question from the sidebar.
2. Enter the student's answer in the text area.
3. Click "Grade Answer". The system will retrieve context, verify ontological concepts, and use the local LLM to generate a breakdown of scores and Sinhala feedback.

## Configuration
You can change the primary model, embedding model, or UI settings in `config.py`.

*Developed by Ravindu-VS*
