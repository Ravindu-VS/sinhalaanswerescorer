"""
Ontology Agent: Queries the OWL ontology for concept relationships,
verifies concept coverage, and enriches the scoring context.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ontology.ontology_loader import OntologyManager


class OntologyAgent:
    """Agent responsible for ontology-based concept verification and enrichment."""

    def __init__(self):
        self.ontology_manager = OntologyManager()

    def analyze(self, question_id, student_answer):
        """
        Analyze the student answer against the ontology.

        Args:
            question_id: The question identifier (Q1-Q5)
            student_answer: The student's answer text

        Returns:
            dict with ontology analysis results
        """
        # Verify concept coverage
        coverage = self.ontology_manager.verify_concept_coverage(
            student_answer, question_id
        )

        # Get ontology context for scoring
        ontology_context = self.ontology_manager.get_ontology_context_for_scoring(
            question_id
        )

        return {
            "agent": "OntologyAgent",
            "status": "success",
            "question_id": question_id,
            "coverage_report": coverage,
            "ontology_context": ontology_context
        }

    def get_coverage_summary(self, question_id, student_answer):
        """
        Get a formatted summary of concept coverage for the scoring agent.

        Returns a string summarizing which concepts were found/missing.
        """
        result = self.analyze(question_id, student_answer)
        coverage = result["coverage_report"]

        if "error" in coverage:
            return "Ontology analysis unavailable."

        lines = [
            f"### Ontology Concept Coverage Report",
            f"**Topic:** {coverage.get('topic', '')}",
            f"**Coverage:** {coverage['total_found']}/{coverage['total_expected']} "
            f"concepts ({coverage['coverage_percentage']}%)\n",
        ]

        if coverage["found_concepts"]:
            lines.append("**✅ Concepts Found in Answer:**")
            for c in coverage["found_concepts"]:
                sig = c.get("significance", "")
                lines.append(f"  - {c['concept']}: {sig}")

        if coverage["missing_concepts"]:
            lines.append("\n**❌ Missing Concepts:**")
            for c in coverage["missing_concepts"]:
                sig = c.get("significance", "")
                lines.append(f"  - {c['concept']}: {sig}")

        return "\n".join(lines)

    def get_ontology_context(self, question_id):
        """Get the textual ontology context for a question."""
        return self.ontology_manager.get_ontology_context_for_scoring(question_id)
