"""
Scoring Agent: Uses OLLAMA (llama3) to evaluate the student's answer
against the marking criteria, retrieved context, and ontology concepts.
Produces structured score breakdown with evidence-based justifications.
"""
import json
import re
import os
import sys
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OLLAMA_MODEL, OLLAMA_BASE_URL, LLM_TEMPERATURE, LLM_NUM_CTX
from marking.marking_guides import get_marking_guide, format_marking_guide_for_llm


class ScoringAgent:
    """Agent responsible for LLM-based scoring and explanation generation."""

    def __init__(self):
        self.model = OLLAMA_MODEL
        self.base_url = OLLAMA_BASE_URL

    def _call_ollama(self, prompt, system_prompt=""):
        """Call the Ollama API for inference."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": LLM_TEMPERATURE,
                "num_ctx": LLM_NUM_CTX,
                "num_predict": 2048,
            }
        }

        try:
            # Increased timeout from 120s to 600s to allow for slower model inference
            response = requests.post(url, json=payload, timeout=600)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.RequestException as e:
            return f"Error calling Ollama: {str(e)}"

    def score(self, question_id, question_text, student_answer,
              retrieved_context, ontology_coverage, ontology_context):
        """
        Score the student's answer using the LLM.

        Args:
            question_id: Question identifier (Q1-Q5)
            question_text: The question in Sinhala
            student_answer: Student's answer in Sinhala
            retrieved_context: Context from RAG retrieval
            ontology_coverage: Coverage report from ontology agent
            ontology_context: Ontology knowledge context

        Returns:
            dict with scores, breakdown, and justifications
        """
        guide = get_marking_guide(question_id)
        if not guide:
            return {"error": f"No marking guide found for {question_id}"}

        marking_guide_text = format_marking_guide_for_llm(question_id)

        # Build the scoring prompt
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_scoring_prompt(
            question_text, student_answer, marking_guide_text,
            retrieved_context, ontology_coverage, ontology_context, guide
        )

        # Call LLM
        llm_response = self._call_ollama(user_prompt, system_prompt)

        # Parse the response
        parsed = self._parse_response(llm_response, guide)

        return {
            "agent": "ScoringAgent",
            "status": "success",
            "question_id": question_id,
            "raw_response": llm_response,
            **parsed
        }

    def _build_system_prompt(self):
        """Build the system prompt for the scoring LLM."""
        return """You are an expert Sinhala History teacher specializing in the Anuradhapura Period of Sri Lanka. 
Your task is to grade a student's Sinhala open-ended answer based on a marking guide.

IMPORTANT RULES:
1. You MUST evaluate EACH criterion in the marking guide separately.
2. You MUST assign a score for each criterion (0 to max_marks for that criterion).
3. You MUST provide justification in Sinhala for each criterion score.
4. Use the retrieved context and ontology coverage to verify factual accuracy.
5. Be fair but rigorous - award marks only for correct, relevant content.
6. Your response MUST be valid JSON format.
7. All justifications should be in Sinhala language."""

    def _build_scoring_prompt(self, question, answer, marking_guide,
                               retrieved_context, ontology_coverage,
                               ontology_context, guide):
        """Build the detailed scoring prompt."""
        criteria_json = []
        for i, c in enumerate(guide["criteria"]):
            criteria_json.append({
                "criterion_number": i + 1,
                "criterion_name": c["name"],
                "max_marks": c["max_marks"],
                "description": c["description_si"]
            })

        prompt = f"""
## TASK: Grade the following Sinhala answer

### QUESTION:
{question}

### STUDENT'S ANSWER:
{answer}

### MARKING GUIDE:
{marking_guide}

### RETRIEVED FACTUAL CONTEXT (from knowledge base):
{retrieved_context}

### ONTOLOGY CONCEPT COVERAGE:
{ontology_coverage}

### ONTOLOGY KNOWLEDGE:
{ontology_context}

---

## INSTRUCTIONS:
Evaluate the student's answer against EACH criterion in the marking guide.
For each criterion, determine how many marks to award based on:
1. How well the student's answer covers the criterion requirements
2. Factual accuracy (verified against the retrieved context)
3. Concept coverage (verified against the ontology)
4. Quality and depth of explanation

CRITICAL: Keep all Sinhala justifications VERY SHORT and concise (maximum 1-2 sentences). Do not write long paragraphs.
CRITICAL: You MUST create exactly one entry in the `criteria_scores` array for EACH and EVERY criterion listed in the "MARKING GUIDE" above. DO NOT invent new criteria. Use the exact `criterion_name` and `max_marks` from the marking guide.

## RESPOND IN THIS EXACT JSON FORMAT:
```json
{{
    "criteria_scores": [
        {{
            "criterion_number": 1,
            "criterion_name": "<exact name from marking guide>",
            "max_marks": <exact max from marking guide>,
            "awarded_marks": <score>,
            "justification_si": "<Sinhala justification explaining why marks were awarded/deducted>"
        }},
        ...for each criterion...
    ],
    "total_score": <sum of all awarded marks>,
    "total_max": 20,
    "overall_feedback_si": "<Overall Sinhala feedback about the answer>"
}}
```

IMPORTANT: Return ONLY the JSON. No additional text before or after the JSON."""

        return prompt

    def _parse_response(self, response, guide):
        """Parse the LLM response into structured scores."""
        try:
            # Try to extract JSON from the response
            # Sometimes LLMs forget the final closing brace, so we append it if the response ends with a string quote.
            clean_response = response.strip()
            if clean_response.endswith('"'):
                clean_response += '\n}'
                
            json_match = re.search(r'\{[\s\S]*\}', clean_response)
            if json_match:
                parsed = json.loads(json_match.group())

                # Validate and cap scores
                criteria_scores = parsed.get("criteria_scores", [])
                total = 0

                for i, score_item in enumerate(criteria_scores):
                    max_marks = guide["criteria"][i]["max_marks"] if i < len(guide["criteria"]) else 0
                    awarded = min(score_item.get("awarded_marks", 0), max_marks)
                    awarded = max(awarded, 0)  # Ensure non-negative
                    score_item["awarded_marks"] = awarded
                    total += awarded

                return {
                    "criteria_scores": criteria_scores,
                    "total_score": total,
                    "total_max": guide["total_marks"],
                    "overall_feedback": parsed.get("overall_feedback_si", ""),
                    "parse_success": True
                }
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            pass

        # Fallback: create a basic response if parsing fails
        return self._create_fallback_response(response, guide)

    def _create_fallback_response(self, raw_response, guide):
        """Create a fallback response when JSON parsing fails."""
        criteria_scores = []
        for c in guide["criteria"]:
            criteria_scores.append({
                "criterion_number": len(criteria_scores) + 1,
                "criterion_name": c["name"],
                "max_marks": c["max_marks"],
                "awarded_marks": 0,
                "justification_si": "ස්වයංක්‍රීය විශ්ලේෂණය අසාර්ථක විය. කරුණාකර නැවත උත්සාහ කරන්න."
            })

        return {
            "criteria_scores": criteria_scores,
            "total_score": 0,
            "total_max": guide["total_marks"],
            "overall_feedback": f"LLM response parsing failed. Raw response:\n{raw_response[:500]}",
            "parse_success": False
        }
