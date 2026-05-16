# Offline Intelligent Sinhala Open-Ended Answer Scorer
## History of Sri Lanka — Anuradhapura Period
### Module: 40_CS4032 Natural Language Processing — Individual Assignment 02

**Student:** Vinusha Rathnayaka  
**Technology Stack:** OLLAMA + RAG + Ontology + Agent Architecture  
**Scope:** Option 1 — Ancient Sri Lanka (Anuradhapura Period)

---

## 1. Problem Setup & History Scope

This system is a fully **offline** intelligent scorer for Sinhala open-ended answers about the **Anuradhapura Period**. Focus areas:

- **Administration** — Royal governance, provincial and village-level systems
- **Irrigation/Civilization** — Tanks (wewa), canals, agricultural engineering
- **Buddhism & Culture** — Introduction of Buddhism, stupas, monastic orders
- **Notable Rulers/Events** — Dutugemunu, Dhatusena, Vasabha, Mahasena
- **Decline** — South Indian invasions, fall of Anuradhapura

The system grades each answer out of **20 marks** using structured marking guides and produces **explainable score breakdowns** with Sinhala justifications.

---

## 2. System Architecture — Operational Flow Chart

![System Architecture Flowchart](C:\Users\Vinusha Rathnayaka\.gemini\antigravity\brain\1fbde531-c20b-4b5d-9441-6480cd8f0522\system_flowchart_1778931979270.png)

![Agent Workflow Pipeline](C:\Users\Vinusha Rathnayaka\.gemini\antigravity\brain\1fbde531-c20b-4b5d-9441-6480cd8f0522\agent_workflow_1778932041500.png)

**Step-by-step workflow:**

| Step | Agent | Action |
|------|-------|--------|
| 1 | UI → Orchestrator | User selects question, enters Sinhala answer |
| 2 | Retrieval Agent | Semantic search over ChromaDB knowledge base |
| 3 | Ontology Agent | Concept coverage check against OWL ontology |
| 4 | Scoring Agent | LLM evaluation via OLLAMA with all context |
| 5 | Orchestrator → UI | Assembles score + breakdown + explanations |

---

## 3. Question Set & Marking Guides (5 Questions)

### Q1: ජලාශ ශිෂ්ටාචාරය (Irrigation Civilization) — 20 marks
| # | Criterion | Marks |
|---|-----------|-------|
| 1 | ප්‍රධාන ජලාශ හඳුනාගැනීම | 5 |
| 2 | ඇළ මාර්ග විස්තර කිරීම | 4 |
| 3 | කෘෂිකර්මාන්තයට සම්බන්ධ කිරීම | 4 |
| 4 | ජලාශ ඉදිකළ රජවරු | 4 |
| 5 | සමස්ත ගුණාත්මකභාවය | 3 |

### Q2: බුදුදහම හඳුන්වාදීම (Introduction of Buddhism) — 20 marks
| # | Criterion | Marks |
|---|-----------|-------|
| 1 | මහින්ද තෙරුන්ගේ මෙහෙවර | 5 |
| 2 | ප්‍රධාන බෞද්ධ ස්ථාන | 4 |
| 3 | ත්‍රිවිධ නිකාය | 4 |
| 4 | සමාජ හා සංස්කෘතික බලපෑම | 4 |
| 5 | සමස්ත ගුණාත්මකභාවය | 3 |

### Q3: ප්‍රධාන රජවරුන් (Key Rulers) — 20 marks
| # | Criterion | Marks |
|---|-----------|-------|
| 1 | රජවරු හඳුනාගැනීම | 5 |
| 2 | යුද්ධමය ජයග්‍රහණ | 4 |
| 3 | යටිතල පහසුකම් දායකත්වය | 4 |
| 4 | ආගමික හා සංස්කෘතික දායකත්වය | 4 |
| 5 | සමස්ත ගුණාත්මකභාවය | 3 |

### Q4: පරිපාලන ක්‍රමය (Administrative System) — 20 marks
| # | Criterion | Marks |
|---|-----------|-------|
| 1 | රජුගේ බලතල | 4 |
| 2 | පළාත් පරිපාලනය | 4 |
| 3 | ග්‍රාම පරිපාලනය | 4 |
| 4 | නීතිය, බදු, ජල කළමනාකරණය | 4 |
| 5 | සමස්ත ගුණාත්මකභාවය | 4 |

### Q5: පරිහානිය (Decline of Anuradhapura) — 20 marks
| # | Criterion | Marks |
|---|-----------|-------|
| 1 | දකුණු ඉන්දීය ආක්‍රමණ | 5 |
| 2 | අභ්‍යන්තර ගැටුම් | 4 |
| 3 | මහින්ද V සහ අනුරාධපුරයේ පතනය | 4 |
| 4 | පොළොන්නරුවට මාරු වීම | 4 |
| 5 | සමස්ත ගුණාත්මකභාවය | 3 |

---

## 4. RAG Implementation

### 4.1 Knowledge Base Documents
| File | Topic | Size |
|------|-------|------|
| `irrigation.txt` | Tanks, canals, agriculture | 4,467 bytes |
| `buddhism.txt` | Buddhism introduction | 5,167 bytes |
| `rulers.txt` | Key rulers & contributions | 5,081 bytes |
| `administration.txt` | Administrative systems | 2,549 bytes |
| `decline.txt` | Fall of Anuradhapura | 3,453 bytes |

### 4.2 Retrieval Pipeline (`setup_kb.py`)

```python
# Embedding model (offline, multilingual Sinhala support)
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Paragraph-aware chunking with overlap
def chunk_text(text, chunk_size=500, overlap=100):
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    # Combines paragraphs up to chunk_size, splits long ones by word
    return chunks

# ChromaDB persistent storage with cosine similarity
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = client.create_collection(
    name="sinhala_history", metadata={"hnsw:space": "cosine"}
)
collection.add(embeddings=embeddings, documents=chunks, ids=ids, metadatas=metadatas)
```

### 4.3 Retrieval Agent (`agents/retrieval_agent.py`)

```python
class RetrievalAgent:
    def retrieve(self, question, student_answer, top_k=5):
        query_text = f"{question} {student_answer[:200]}"
        query_embedding = self.embedding_model.encode(query_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        # Returns documents with similarity scores
```

Retrieved context is injected into the scoring prompt for evidence-based grading.

---

## 5. Ontology Implementation

### 5.1 OWL Ontology Structure

![Ontology Class Hierarchy](C:\Users\Vinusha Rathnayaka\.gemini\antigravity\brain\1fbde531-c20b-4b5d-9441-6480cd8f0522\ontology_diagram_1778932098865.png)

**12 Classes:** HistoricalEntity, Ruler, Location, Structure, Tank, Canal, Stupa, Monastery, Event, Battle, Invasion, MonasticOrder, TimePeriod, Religion, AdministrativeUnit

**9 Object Properties:** `built_by`, `ruled_during`, `located_in`, `part_of`, `introduced_by`, `associated_with`, `fought_in`, `succeeded_by`, `founded_by`

**30+ Individuals** with Sinhala significance annotations:

```python
# Example from create_ontology.py
dhatusena = Ruler("Dhatusena")
dhatusena.reign_start = "455 CE"
dhatusena.significance_si = "ධාතුසේන - කලා වැව හා ජය ගඟ ඉදිකළ රජු"

kala_wewa = Tank("Kala_Wewa")
kala_wewa.built_by = [dhatusena]  # Object property linking
kala_wewa.significance_si = "කලා වැව - ධාතුසේන විසින් ඉදිකළ මහා ජලාශය"
```

### 5.2 Ontology Agent — Concept Verification

```python
# From ontology_loader.py - Sinhala term mapping for concept matching
name_map = {
    "Kala_Wewa": ["කලා වැව", "කලාවැව"],
    "Dhatusena": ["ධාතුසේන"],
    "Jaya_Ganga": ["ජය ගඟ", "යෝද ඇල"],
    "Dutugemunu": ["දුටුගැමුණු"],
    # ... 25+ concept mappings
}

def verify_concept_coverage(self, answer_text, question_id):
    for concept_name in expected_concepts:
        is_found = any(term.lower() in answer_text.lower() 
                      for term in search_terms)
    return {
        "coverage_percentage": round(coverage_pct, 1),
        "found_concepts": found, "missing_concepts": missing
    }
```

---

## 6. Agent-Based Architecture

| Agent | File | Responsibility |
|-------|------|---------------|
| **OrchestratorAgent** | `orchestrator.py` | Coordinates workflow, dispatches to sub-agents |
| **RetrievalAgent** | `retrieval_agent.py` | Semantic search over ChromaDB |
| **OntologyAgent** | `ontology_agent.py` | Concept coverage verification |
| **ScoringAgent** | `scoring_agent.py` | LLM-based evaluation via OLLAMA |

### Orchestrator Workflow

```python
class OrchestratorAgent:
    def grade_answer(self, question_id, question_text, student_answer, progress_callback=None):
        # STEP 1: Retrieval Agent
        retrieval_result = self.retrieval_agent.retrieve(question_text, student_answer)
        retrieved_context = self.retrieval_agent.get_context_for_scoring(question_text, student_answer)
        
        # STEP 2: Ontology Agent
        ontology_result = self.ontology_agent.analyze(question_id, student_answer)
        ontology_coverage = self.ontology_agent.get_coverage_summary(question_id, student_answer)
        
        # STEP 3: Scoring Agent (LLM call with all context)
        scoring_result = self.scoring_agent.score(
            question_id=question_id, question_text=question_text,
            student_answer=student_answer,
            retrieved_context=retrieved_context,
            ontology_coverage=ontology_coverage,
            ontology_context=ontology_context
        )
        
        # STEP 4: Assemble final result
        return final_result
```

**Reliability Features:** Error isolation per agent, progress tracking with timestamps, score validation (capped to max_marks), fallback response on parse failure.

---

## 7. Explainable Scoring

The Scoring Agent produces structured JSON output:

```json
{
    "criteria_scores": [
        {
            "criterion_name": "ප්‍රධාන ජලාශ හඳුනාගැනීම",
            "max_marks": 5, "awarded_marks": 4,
            "justification_si": "සිසුවා අභය වැව, තිස්ස වැව, කලා වැව, මින්නේරිය සඳහන් කර ඇත. නමුත් නුවර වැව මග හැරී ඇත."
        }
    ],
    "total_score": 16, "total_max": 20,
    "overall_feedback_si": "..."
}
```

Score parsing with validation:
```python
def _parse_response(self, response, guide):
    json_match = re.search(r'\{[\s\S]*\}', response)
    parsed = json.loads(json_match.group())
    for i, score_item in enumerate(criteria_scores):
        awarded = min(score_item.get("awarded_marks", 0), max_marks)
        awarded = max(awarded, 0)  # Non-negative
```

---

## 8. Streamlit UI

![Streamlit UI](C:\Users\Vinusha Rathnayaka\.gemini\antigravity\brain\1fbde531-c20b-4b5d-9441-6480cd8f0522\main_page_full_view_1778931779428.png)

**Components:** Sidebar (question selector, marking guide, system info), Main area (question display, answer input), Results (score card, criterion breakdown, evidence panels)

---

## 9. Offline Operation

| Component | Offline Mechanism |
|-----------|-------------------|
| LLM | OLLAMA on `localhost:11434` |
| Embeddings | `MiniLM-L12-v2` cached locally |
| Vector Store | ChromaDB persistent on disk |
| Ontology | Local OWL file |
| Knowledge Base | 5 local text files |

---

## 10. Project Structure

```
NLP II/
├── app.py                    # Streamlit UI (638 lines)
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── setup_kb.py               # KB builder
├── test_pipeline.py          # Tests
├── agents/
│   ├── orchestrator.py       # Workflow coordinator
│   ├── retrieval_agent.py    # RAG retrieval
│   ├── ontology_agent.py     # Ontology verification
│   └── scoring_agent.py      # LLM scoring
├── knowledge_base/
│   ├── documents/            # 5 Sinhala text files
│   └── chroma_db/            # Vector store
├── ontology/
│   ├── create_ontology.py    # OWL builder
│   ├── ontology_loader.py    # Query utilities
│   └── anuradhapura.owl      # Serialized ontology
└── marking/
    └── marking_guides.py     # 5 questions + criteria
```

---

## 11. Execution Video

> **Video URL:** [INSERT YOUR VIDEO URL HERE]

---

## 12. Requirements Compliance

| Requirement | Status |
|-------------|--------|
| Offline operation | ✅ |
| OLLAMA-based scoring | ✅ |
| RAG implementation | ✅ |
| Ontology component | ✅ |
| Agent architecture | ✅ |
| Explainability | ✅ |
| Streamlit UI | ✅ |
| 5 Questions × 20 marks | ✅ |
| Flow chart | ✅ |
| Code snippets | ✅ |
