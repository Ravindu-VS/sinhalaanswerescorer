"""
Validation Agent: Cross-checks scoring results for consistency and reliability.
Validates scores against ontology coverage and ensures marking integrity.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from marking.marking_guides import get_marking_guide


class ValidationAgent:
    """Agent responsible for validating scoring consistency and reliability."""

    def validate(self, scoring_result, ontology_result, question_id):
        """
        Validate the scoring result for consistency.

        Args:
            scoring_result: Output from the ScoringAgent
            ontology_result: Output from the OntologyAgent
            question_id: Question identifier (Q1-Q5)

        Returns:
            dict with validation report and any corrections
        """
        guide = get_marking_guide(question_id)
        if not guide:
            return {"status": "error", "message": f"No guide for {question_id}"}

        checks = []
        corrections_made = False
        criteria_scores = scoring_result.get("criteria_scores", [])

        # ========== CHECK 1: Score bounds ==========
        for i, cs in enumerate(criteria_scores):
            max_m = guide["criteria"][i]["max_marks"] if i < len(guide["criteria"]) else 0
            awarded = cs.get("awarded_marks", 0)

            if awarded < 0:
                cs["awarded_marks"] = 0
                corrections_made = True
                checks.append({
                    "check": "score_bounds",
                    "criterion": cs.get("criterion_name", f"C{i+1}"),
                    "status": "corrected",
                    "detail": f"Negative score ({awarded}) corrected to 0"
                })
            elif awarded > max_m:
                cs["awarded_marks"] = max_m
                corrections_made = True
                checks.append({
                    "check": "score_bounds",
                    "criterion": cs.get("criterion_name", f"C{i+1}"),
                    "status": "corrected",
                    "detail": f"Score ({awarded}) exceeded max ({max_m}), capped"
                })
            else:
                checks.append({
                    "check": "score_bounds",
                    "criterion": cs.get("criterion_name", f"C{i+1}"),
                    "status": "pass",
                    "detail": f"{awarded}/{max_m} within bounds"
                })

        # ========== CHECK 2: Total consistency ==========
        recalculated_total = sum(cs.get("awarded_marks", 0) for cs in criteria_scores)
        reported_total = scoring_result.get("total_score", 0)

        if recalculated_total != reported_total:
            scoring_result["total_score"] = recalculated_total
            corrections_made = True
            checks.append({
                "check": "total_consistency",
                "status": "corrected",
                "detail": f"Reported total ({reported_total}) != sum ({recalculated_total}), corrected"
            })
        else:
            checks.append({
                "check": "total_consistency",
                "status": "pass",
                "detail": f"Total {recalculated_total} matches sum of criteria"
            })

        # ========== CHECK 3: Criteria count ==========
        expected_count = len(guide["criteria"])
        actual_count = len(criteria_scores)

        if actual_count != expected_count:
            checks.append({
                "check": "criteria_count",
                "status": "warning",
                "detail": f"Expected {expected_count} criteria, got {actual_count}"
            })
        else:
            checks.append({
                "check": "criteria_count",
                "status": "pass",
                "detail": f"All {expected_count} criteria scored"
            })

        # ========== CHECK 4: Ontology-score cross-validation ==========
        coverage_report = ontology_result.get("coverage_report", {})
        coverage_pct = coverage_report.get("coverage_percentage", 0)

        # If ontology coverage is very low but scores are very high, flag it
        if coverage_pct < 20 and recalculated_total > guide["total_marks"] * 0.7:
            checks.append({
                "check": "ontology_cross_check",
                "status": "warning",
                "detail": (
                    f"Low ontology coverage ({coverage_pct}%) but high score "
                    f"({recalculated_total}/{guide['total_marks']}). "
                    f"Scores may be inflated."
                )
            })
        elif coverage_pct > 80 and recalculated_total < guide["total_marks"] * 0.3:
            checks.append({
                "check": "ontology_cross_check",
                "status": "warning",
                "detail": (
                    f"High ontology coverage ({coverage_pct}%) but low score "
                    f"({recalculated_total}/{guide['total_marks']}). "
                    f"Scores may be deflated."
                )
            })
        else:
            checks.append({
                "check": "ontology_cross_check",
                "status": "pass",
                "detail": (
                    f"Ontology coverage ({coverage_pct}%) is consistent "
                    f"with score ({recalculated_total}/{guide['total_marks']})"
                )
            })

        # ========== CHECK 5: Justification presence ==========
        missing_justifications = []
        for cs in criteria_scores:
            justification = cs.get("justification_si", "")
            if not justification or len(justification.strip()) < 10:
                missing_justifications.append(cs.get("criterion_name", "Unknown"))

        if missing_justifications:
            checks.append({
                "check": "justification_presence",
                "status": "warning",
                "detail": f"Missing/short justifications for: {', '.join(missing_justifications)}"
            })
        else:
            checks.append({
                "check": "justification_presence",
                "status": "pass",
                "detail": "All criteria have justifications"
            })

        # Summary
        passed = sum(1 for c in checks if c["status"] == "pass")
        warnings = sum(1 for c in checks if c["status"] == "warning")
        corrected = sum(1 for c in checks if c["status"] == "corrected")

        return {
            "agent": "ValidationAgent",
            "status": "success",
            "total_checks": len(checks),
            "passed": passed,
            "warnings": warnings,
            "corrected": corrected,
            "corrections_made": corrections_made,
            "validated_score": scoring_result.get("total_score", 0),
            "checks": checks
        }
