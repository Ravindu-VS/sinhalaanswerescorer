# 📝 Offline Intelligent Sinhala Answer Scorer

A fully offline, multi-agent AI pipeline for automatically evaluating and grading open-ended Sinhala historical answers. The system operates entirely on your local machine, ensuring 100% data privacy and no reliance on internet connectivity.

Built primarily to score answers related to the **Anuradhapura Period** of Sri Lankan history, utilizing a custom marking guide, factual retrieval, and a domain-specific ontology.

---

## 🌟 Key Features

- **100% Offline Capability**: Runs entirely locally via Ollama. No API keys, no data sent to the cloud, and no network errors.
- **RAG Architecture**: Uses `sentence-transformers` and `ChromaDB` to fetch factual historical contexts from localized `.txt` knowledge bases.
- **Ontology Verification**: Verifies conceptual accuracy using `owlready2` against an Anuradhapura era OWL ontology to ensure the student hit the correct semantic concepts.
- **Multi-Agent Design**:
  - `Retrieval Agent`: Gathers factual documents related to the question and answer.
  - `Ontology Agent`: Maps the student's answer to core semantic concepts (e.g., specific kings, reservoirs).
  - `Scoring Agent`: Uses local LLMs (`gemma3:4b` or `llama3`) to logically grade the answer against the rubric and produce structured JSON scoring and feedback.
- **Modern UI**: A beautiful, dark-themed Streamlit interface that tracks workflow progress and dynamically renders score breakdowns.

---

## ⚙️ Prerequisites

1. **Python 3.10+**
2. **Ollama**: Installed and running on your local machine.
3. **Local Models**: You must pull the underlying models via Ollama.
   ```cmd
   ollama pull gemma3:4b
   ollama pull llama3
   ```
   *(Note: `gemma3:4b` is set as the default in `config.py` for highly accelerated inference speeds).*

---

## 🚀 Setup & Installation

1. **Clone the Repository**
   ```cmd
   git clone https://github.com/Ravindu-VS/sinhalaanswerescorer.git
   cd sinhalaanswerescorer
   ```

2. **Install Dependencies**
   It is recommended to use a virtual environment (`python -m venv .venv`).
   ```cmd
   pip install -r requirements.txt
   ```

3. **Initialize the Knowledge Base**
   Run the setup script. This reads all `.txt` documents in the `knowledge_base/documents` folder, splits them into logical chunks, calculates local embeddings, and stores them in the ChromaDB vector database.
   ```cmd
   python setup_kb.py
   ```

4. **Launch the Application**
   Run the Streamlit dashboard.
   ```cmd
   python -m streamlit run app.py
   ```
   The dashboard will open automatically in your browser at `http://localhost:8501` (or `8502`).

---

## 📖 Usage Workflow

1. **Select a Question**: Open the sidebar and choose a Sinhala history question from the dropdown list.
2. **Review the Marking Guide**: The sidebar dynamically updates to show the specific marking rubric (e.g., marks for identifying reservoirs, naming kings, mentioning agriculture).
3. **Enter Answer**: Type or paste the student's Sinhala answer into the main text area.
4. **Grade**: Click "⚖️ පිළිතුර ඇගයීම කරන්න (Grade Answer)".
5. **Review Results**: The system will execute the Multi-Agent pipeline. Once finished, you will see a total score, a percentage badge, a breakdown of marks per criterion with Sinhala justifications, and detailed expanders showing exact RAG document matches and Ontology coverage.
6. **Next Question**: When you select a new question from the sidebar, the interface automatically resets the input and previous results so you have a clean slate.

---

## 🛠️ Configuration

All major settings can be easily tweaked inside `config.py`:
- `OLLAMA_MODEL`: Change between `"gemma3:4b"`, `"llama3:latest"`, etc.
- `LLM_NUM_CTX`: Set context window size.
- `LLM_TEMPERATURE`: Kept at `0.1` for deterministic, logical grading.
- `TOP_K_RESULTS`: Number of RAG chunks to retrieve per query.

---

*Developed by Ravindu-VS*
