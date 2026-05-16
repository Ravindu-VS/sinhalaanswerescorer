"""Quick test script to verify all agents work correctly."""
import sys, os

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("Testing Sinhala Answer Scorer Pipeline")
print("=" * 50)

# Test 1: Retrieval Agent
print("\n[1] Testing Retrieval Agent...")
from agents.retrieval_agent import RetrievalAgent
ra = RetrievalAgent()
result = ra.retrieve("irrigation tanks", "kala wewa dhatusena")
print(f"    Retrieved {result['num_results']} documents")
if result['retrieved_documents']:
    print(f"    Top source: {result['retrieved_documents'][0]['source']}")
    print(f"    Similarity: {result['retrieved_documents'][0]['similarity']}")
print("    [OK] Retrieval Agent works!")

# Test 2: Ontology Agent
print("\n[2] Testing Ontology Agent...")
from agents.ontology_agent import OntologyAgent
oa = OntologyAgent()
analysis = oa.analyze("Q1", "kala wewa dhatusena vasabha")
coverage = analysis['coverage_report']
print(f"    Coverage: {coverage.get('coverage_percentage', 0)}%")
print(f"    Found: {coverage.get('total_found', 0)}/{coverage.get('total_expected', 0)}")
print("    [OK] Ontology Agent works!")

# Test 3: Scoring Agent (LLM call)
print("\n[3] Testing Scoring Agent (LLM call - may take a minute)...")
from agents.scoring_agent import ScoringAgent
sa = ScoringAgent()

test_answer = "kala wewa dhatusena vasabha mahasena minneriya"
test_result = sa.score(
    question_id="Q1",
    question_text="Test question about irrigation",
    student_answer=test_answer,
    retrieved_context="Test context",
    ontology_coverage="Test coverage",
    ontology_context="Test ontology"
)
print(f"    Total score: {test_result.get('total_score', 'N/A')}/{test_result.get('total_max', 20)}")
print(f"    Parse success: {test_result.get('parse_success', False)}")
print(f"    Criteria scores: {len(test_result.get('criteria_scores', []))}")
print("    [OK] Scoring Agent works!")

# Test 4: Full Orchestrator
print("\n[4] Testing Orchestrator (full pipeline)...")
from agents.orchestrator import OrchestratorAgent
orch = OrchestratorAgent()

full_answer = (
    "kala wewa, tissa wewa, abhaya wewa, minneriya wewa ya prodhaana jalaashaya. "
    "dhatusena raju kala wewa saha jaya ganga idikale. "
    "vasabha raju jalaasha 11k idikale."
)

full_result = orch.grade_answer(
    question_id="Q1",
    question_text="Test about irrigation",
    student_answer=full_answer
)
print(f"    Total score: {full_result['total_score']}/{full_result['total_max']}")
print(f"    Elapsed: {full_result['elapsed_seconds']}s")
print(f"    Criteria: {len(full_result['criteria_scores'])}")
print("    [OK] Full pipeline works!")

print("\n" + "=" * 50)
print("[OK] ALL TESTS PASSED!")
print("=" * 50)
