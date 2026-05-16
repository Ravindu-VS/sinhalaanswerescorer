"""
Orchestrator Agent: Coordinates the full scoring workflow.
Receives question + answer, dispatches to sub-agents, and assembles final output.
"""
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class OrchestratorAgent:
    """
    Main workflow coordinator for the Sinhala Answer Scoring system.

    Workflow:
    1. Receive question selection + student answer from UI
    2. Call Retrieval Agent → get relevant context from knowledge base
    3. Call Ontology Agent → get concept coverage analysis
    4. Call Scoring Agent → get score breakdown with justifications
    5. Assemble final result and return to UI
    """

    def __init__(self):
        self.retrieval_agent = None
        self.ontology_agent = None
        self.scoring_agent = None
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all sub-agents."""
        from agents.retrieval_agent import RetrievalAgent
        from agents.ontology_agent import OntologyAgent
        from agents.scoring_agent import ScoringAgent

        self.retrieval_agent = RetrievalAgent()
        self.ontology_agent = OntologyAgent()
        self.scoring_agent = ScoringAgent()

    def grade_answer(self, question_id, question_text, student_answer,
                     progress_callback=None):
        """
        Main grading workflow.

        Args:
            question_id: Question identifier (Q1-Q5)
            question_text: The question in Sinhala
            student_answer: Student's answer in Sinhala
            progress_callback: Optional callback for progress updates

        Returns:
            dict with complete grading results
        """
        start_time = time.time()
        workflow_log = []

        def log_step(step, message):
            """Log a workflow step."""
            entry = {
                "step": step,
                "message": message,
                "timestamp": time.time() - start_time
            }
            workflow_log.append(entry)
            if progress_callback:
                progress_callback(step, message)

        # ========== STEP 1: Retrieval Agent ==========
        log_step(1, "📚 Retrieval Agent: Searching knowledge base...")
        try:
            retrieval_result = self.retrieval_agent.retrieve(
                question_text, student_answer
            )
            retrieved_context = self.retrieval_agent.get_context_for_scoring(
                question_text, student_answer
            )
            log_step(1, f"✅ Retrieved {retrieval_result['num_results']} relevant documents")
        except Exception as e:
            retrieved_context = "Knowledge base retrieval failed."
            retrieval_result = {"num_results": 0, "retrieved_documents": []}
            log_step(1, f"⚠️ Retrieval failed: {str(e)}")

        # ========== STEP 2: Ontology Agent ==========
        log_step(2, "🧠 Ontology Agent: Analyzing concept coverage...")
        try:
            ontology_result = self.ontology_agent.analyze(
                question_id, student_answer
            )
            ontology_coverage = self.ontology_agent.get_coverage_summary(
                question_id, student_answer
            )
            ontology_context = self.ontology_agent.get_ontology_context(question_id)
            log_step(2, f"✅ Concept coverage: "
                        f"{ontology_result['coverage_report'].get('coverage_percentage', 0)}%")
        except Exception as e:
            ontology_coverage = "Ontology analysis unavailable."
            ontology_context = ""
            ontology_result = {"coverage_report": {}}
            log_step(2, f"⚠️ Ontology analysis failed: {str(e)}")

        # ========== STEP 3: Scoring Agent ==========
        log_step(3, "⚖️ Scoring Agent: Evaluating answer with LLM...")
        try:
            scoring_result = self.scoring_agent.score(
                question_id=question_id,
                question_text=question_text,
                student_answer=student_answer,
                retrieved_context=retrieved_context,
                ontology_coverage=ontology_coverage,
                ontology_context=ontology_context
            )
            log_step(3, f"✅ Scoring complete: {scoring_result.get('total_score', 0)}/20")
        except Exception as e:
            scoring_result = {
                "total_score": 0,
                "total_max": 20,
                "criteria_scores": [],
                "overall_feedback": f"Scoring failed: {str(e)}",
                "parse_success": False
            }
            log_step(3, f"⚠️ Scoring failed: {str(e)}")

        # ========== STEP 4: Assemble Final Result ==========
        log_step(4, "📝 Assembling final results...")
        elapsed = time.time() - start_time

        final_result = {
            "question_id": question_id,
            "question_text": question_text,
            "student_answer": student_answer,

            # Scoring results
            "total_score": scoring_result.get("total_score", 0),
            "total_max": scoring_result.get("total_max", 20),
            "criteria_scores": scoring_result.get("criteria_scores", []),
            "overall_feedback": scoring_result.get("overall_feedback", ""),
            "parse_success": scoring_result.get("parse_success", False),

            # Supporting evidence
            "retrieved_documents": retrieval_result.get("retrieved_documents", []),
            "ontology_coverage": ontology_result.get("coverage_report", {}),

            # Metadata
            "workflow_log": workflow_log,
            "elapsed_seconds": round(elapsed, 2),
            "model_used": self.scoring_agent.model
        }

        log_step(4, f"✅ Complete! Score: {final_result['total_score']}/20 "
                     f"(took {elapsed:.1f}s)")

        return final_result
