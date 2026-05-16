# 📝 Offline Intelligent Sinhala Answer Scorer (History of Sri Lanka)

A fully offline, multi-agent AI pipeline for automatically evaluating and grading open-ended Sinhala historical answers. This project fulfills the requirements for the **40_CS4032 Natural Language Processing — Individual Assignment 02**.

## 🎯 Assignment Scope & Alignment
- **Topic Scope**: Ancient Sri Lanka (Anuradhapura Period) - *Option 1*
- **Focus Areas**: Administration, Irrigation/Civilization, Buddhism & Culture, Notable Rulers/Events.
- **Question Set**: 5 well-designed Sinhala history questions (graded out of 20 with specific marking rubrics).

---

## 🌟 System Requirements Met

1. **Offline Operation**: 100% offline. No internet connectivity is required during execution. Model inferences and embeddings are processed strictly locally.
2. **OLLAMA-based Scoring**: Uses `llama3:latest` for accurate Sinhala response generation and logical JSON structuring.
3. **RAG (Retrieval-Augmented Generation)**: Uses `sentence-transformers` and `ChromaDB` to retrieve relevant factual evidence from local `.txt` knowledge bases to ground the scoring.
4. **Ontology**: Implements an `owlready2` Anuradhapura era OWL ontology to represent key historical concepts (Kings, Reservoirs, Temples) and verify semantic coverage.
5. **Agent-Based Architecture**:
   - `Retrieval Agent`: Gathers factual documents from ChromaDB.
   - `Ontology Agent`: Checks concept coverage against the OWL file.
   - `Scoring Agent`: Evaluates the answer and generates explainable scores using the LLM.
6. **Explainable Scoring**: Provides a final score out of 20, a breakdown per marking criterion, and a 1-sentence Sinhala evidence-based justification.
7. **Streamlit UI**: A clean dashboard to select questions, enter Sinhala answers, and view the score breakdown and RAG/Ontology evidence.

---

## ⚙️ Prerequisites

1. **Python 3.10+**
2. **Ollama**: Installed and running locally.
3. **Local Models**: You must pull the primary Llama 3 model.
   ```cmd
   ollama pull llama3
   ```

---

## 🚀 Setup & Installation

1. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

2. **Initialize the Knowledge Base**
   Run the setup script. This reads all `.txt` documents in the `knowledge_base/documents` folder, splits them into logical chunks, calculates local embeddings, and stores them in the ChromaDB vector database.
   ```cmd
   python setup_kb.py
   ```

3. **Launch the Application**
   Run the Streamlit dashboard.
   ```cmd
   python -m streamlit run app.py
   ```

---

## 📖 Usage Workflow

1. **Select a Question**: Open the sidebar and choose a Sinhala history question (e.g., *Introduction of Buddhism*, *Irrigation Civilization*).
2. **Review the Marking Guide**: The sidebar dynamically updates to show the specific marking rubric.
3. **Enter Answer**: Type or paste the student's Sinhala answer into the main text area.
4. **Grade**: Click "⚖️ පිළිතුර ඇගයීම කරන්න (Grade Answer)".
5. **Review Results**: The system will execute the Multi-Agent pipeline offline. Once finished, you will see a total score, a percentage badge, a breakdown of marks per criterion with Sinhala justifications, and detailed expanders showing exact RAG document matches and Ontology coverage.

---

## 🛠️ Configuration & Optimization

All major settings can be tweaked inside `config.py`:
- `OLLAMA_MODEL`: Set to `"llama3:latest"` for accurate Sinhala generation.
- `LLM_NUM_CTX`: Reduced to `2048` to heavily optimize speed and memory.
- `num_predict` (in `scoring_agent.py`): Limited to `512` to force fast, punchy responses.

---

*Developed by Ravindu-VS | For 40_CS4032 NLP Assignment 02*
