"""
Ontology loader and query utilities for the Anuradhapura OWL ontology.
Provides functions to load, query, and verify concept coverage.
"""
from owlready2 import *
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ONTOLOGY_FILE


class OntologyManager:
    """Manages the Anuradhapura ontology for querying and concept verification."""

    def __init__(self):
        self.onto = None
        self._load_ontology()

    def _load_ontology(self):
        """Load the OWL ontology file."""
        if not os.path.exists(ONTOLOGY_FILE):
            # Create ontology if it doesn't exist
            from ontology.create_ontology import create_ontology, save_ontology
            self.onto = create_ontology()
            save_ontology(self.onto, ONTOLOGY_FILE)
        else:
            # Use onto_path for Windows compatibility (handles spaces in paths)
            onto_dir = os.path.dirname(ONTOLOGY_FILE)
            onto_filename = os.path.basename(ONTOLOGY_FILE)
            if onto_dir not in onto_path:
                onto_path.append(onto_dir)
            self.onto = get_ontology(
                "http://sinhala-history.org/anuradhapura.owl"
            ).load(only_local=True)

    def get_all_individuals(self):
        """Return all individuals in the ontology."""
        return list(self.onto.individuals())

    def get_all_classes(self):
        """Return all classes in the ontology."""
        return list(self.onto.classes())

    def get_individual_info(self, individual_name):
        """Get detailed info about an individual entity."""
        individual = self.onto.search_one(iri=f"*{individual_name}")
        if not individual:
            return None

        info = {
            "name": individual.name,
            "type": [cls.name for cls in individual.is_a if cls != Thing],
            "significance_si": getattr(individual, "significance_si", None),
            "significance_en": getattr(individual, "significance_en", None),
            "properties": {}
        }

        # Collect all object properties
        for prop in self.onto.object_properties():
            values = getattr(individual, prop.name, [])
            if values:
                info["properties"][prop.name] = [v.name for v in values]

        # Collect data properties
        for prop in self.onto.data_properties():
            value = getattr(individual, prop.name, None)
            if value:
                info["properties"][prop.name] = value

        return info

    def get_related_concepts(self, concept_name):
        """Find all concepts related to a given concept."""
        individual = self.onto.search_one(iri=f"*{concept_name}")
        if not individual:
            return []

        related = set()
        for prop in self.onto.object_properties():
            # Forward relationships
            values = getattr(individual, prop.name, [])
            for v in values:
                related.add((prop.name, v.name, getattr(v, "significance_si", "")))

            # Inverse relationships
            for other in self.onto.individuals():
                other_values = getattr(other, prop.name, [])
                if individual in other_values:
                    related.add((f"inverse_{prop.name}", other.name,
                                 getattr(other, "significance_si", "")))

        return list(related)

    def get_concepts_for_question(self, question_id):
        """Return expected ontology concepts for each question."""
        concept_map = {
            "Q1": {
                "topic": "ජලාශ ශිෂ්ටාචාරය (Irrigation)",
                "expected_concepts": [
                    "Abhaya_Wewa", "Tissa_Wewa", "Nuwara_Wewa",
                    "Kala_Wewa", "Minneriya_Wewa", "Jaya_Ganga",
                    "Vasabha", "Mahasena", "Dhatusena"
                ],
                "expected_classes": ["Tank", "Canal", "Ruler"]
            },
            "Q2": {
                "topic": "බුදුදහම (Buddhism)",
                "expected_concepts": [
                    "Devanampiya_Tissa", "Theravada_Buddhism",
                    "Thuparamaya", "Sri_Maha_Bodhi", "Ruwanwelisaya",
                    "Mahavihara", "Abhayagiri_Nikaya", "Jetavana_Nikaya",
                    "Abhayagiri_Stupa", "Jetavanarama"
                ],
                "expected_classes": ["Stupa", "MonasticOrder", "Religion", "Ruler"]
            },
            "Q3": {
                "topic": "ප්‍රධාන රජවරුන් (Key Rulers)",
                "expected_concepts": [
                    "Pandukabhaya", "Devanampiya_Tissa", "Dutugemunu",
                    "Vattagamani_Abhaya", "Vasabha", "Mahasena",
                    "Dhatusena", "Battle_of_Vijithapura", "Ruwanwelisaya"
                ],
                "expected_classes": ["Ruler", "Battle", "Stupa", "Tank"]
            },
            "Q4": {
                "topic": "පරිපාලන ක්‍රමය (Administration)",
                "expected_concepts": [
                    "Anuradhapura_Kingdom", "Province_Rata",
                    "Village_Gama", "Anuradhapura"
                ],
                "expected_classes": ["AdministrativeUnit", "Location"]
            },
            "Q5": {
                "topic": "පරිහානිය (Decline)",
                "expected_concepts": [
                    "Mahinda_V", "Chola_Invasion_1017",
                    "Polonnaruwa", "Anuradhapura"
                ],
                "expected_classes": ["Ruler", "Invasion", "Location"]
            }
        }
        return concept_map.get(question_id, {})

    def verify_concept_coverage(self, answer_text, question_id):
        """
        Check which expected ontology concepts appear in the student's answer.
        Returns a coverage report.
        """
        question_concepts = self.get_concepts_for_question(question_id)
        if not question_concepts:
            return {"error": "Unknown question ID"}

        expected = question_concepts.get("expected_concepts", [])

        # Build a mapping of concept names to their Sinhala significance
        concept_details = {}
        for concept_name in expected:
            info = self.get_individual_info(concept_name)
            if info:
                concept_details[concept_name] = info

        # Check which concepts are mentioned in the answer
        found = []
        missing = []

        for concept_name in expected:
            info = concept_details.get(concept_name)
            if not info:
                missing.append({
                    "concept": concept_name,
                    "significance": "Unknown"
                })
                continue

            # Check against concept name, Sinhala significance, and common variants
            search_terms = [concept_name.replace("_", " ")]
            if info.get("significance_si"):
                search_terms.append(info["significance_si"])

            # Add common Sinhala name variants
            name_map = {
                "Abhaya_Wewa": ["අභය වැව", "අභය"],
                "Tissa_Wewa": ["තිස්ස වැව", "තිස්ස"],
                "Nuwara_Wewa": ["නුවර වැව"],
                "Kala_Wewa": ["කලා වැව", "කලාවැව"],
                "Minneriya_Wewa": ["මින්නේරිය", "මින්නේරිය වැව"],
                "Jaya_Ganga": ["ජය ගඟ", "යෝද ඇල", "යෝද ඇළ"],
                "Vasabha": ["වසභ"],
                "Mahasena": ["මහාසේන"],
                "Dhatusena": ["ධාතුසේන"],
                "Devanampiya_Tissa": ["දේවානම්පිය තිස්ස", "දේවානම්පියතිස්ස"],
                "Dutugemunu": ["දුටුගැමුණු", "දුටුගෑමුණු"],
                "Pandukabhaya": ["පණ්ඩුකාභය"],
                "Vattagamani_Abhaya": ["වට්ටගාමිණී", "වට්ටගාමිණී අභය"],
                "Mahinda_V": ["මහින්ද", "මහින්ද V"],
                "Thuparamaya": ["ථූපාරාමය", "ථූපාරාම"],
                "Ruwanwelisaya": ["රුවන්වැලිසෑය", "රුවන්වැලිසෑ"],
                "Jetavanarama": ["ජේතවනාරාම", "ජේතවනාරාමය"],
                "Abhayagiri_Stupa": ["අභයගිරි", "අභයගිරිය"],
                "Sri_Maha_Bodhi": ["ශ්‍රී මහා බෝධිය", "මහා බෝධිය", "බෝධිය"],
                "Mahavihara": ["මහාවිහාරය", "මහාවිහාර"],
                "Abhayagiri_Nikaya": ["අභයගිරි නිකාය"],
                "Jetavana_Nikaya": ["ජේතවන නිකාය", "ජේතවන"],
                "Theravada_Buddhism": ["බුදුදහම", "ථේරවාද", "බුද්ධාගම"],
                "Anuradhapura_Kingdom": ["අනුරාධපුර රාජධානිය", "අනුරාධපුර"],
                "Province_Rata": ["රට", "පළාත්"],
                "Village_Gama": ["ගම", "ග්‍රාම"],
                "Anuradhapura": ["අනුරාධපුර"],
                "Polonnaruwa": ["පොළොන්නරුව", "පොළොන්නරුවය"],
                "Chola_Invasion_1017": ["චෝල", "චෝල ආක්‍රමණය"],
                "Battle_of_Vijithapura": ["විජිතපුර", "එළාර", "යුද්ධය"],
            }

            search_terms.extend(name_map.get(concept_name, []))

            is_found = any(term.lower() in answer_text.lower() for term in search_terms)

            if is_found:
                found.append({
                    "concept": concept_name,
                    "significance": info.get("significance_si", ""),
                    "type": info.get("type", [])
                })
            else:
                missing.append({
                    "concept": concept_name,
                    "significance": info.get("significance_si", ""),
                    "type": info.get("type", [])
                })

        coverage_pct = (len(found) / len(expected) * 100) if expected else 0

        return {
            "topic": question_concepts.get("topic", ""),
            "total_expected": len(expected),
            "total_found": len(found),
            "coverage_percentage": round(coverage_pct, 1),
            "found_concepts": found,
            "missing_concepts": missing,
            "expected_classes": question_concepts.get("expected_classes", [])
        }

    def get_ontology_context_for_scoring(self, question_id):
        """Generate a textual summary of ontology knowledge for a question."""
        concepts = self.get_concepts_for_question(question_id)
        if not concepts:
            return ""

        lines = [f"### Ontology Context for: {concepts.get('topic', '')}\n"]
        lines.append("Expected key concepts and their relationships:\n")

        for concept_name in concepts.get("expected_concepts", []):
            info = self.get_individual_info(concept_name)
            if info:
                sig = info.get("significance_si", "")
                types = ", ".join(info.get("type", []))
                lines.append(f"- **{concept_name}** ({types}): {sig}")

                # Add relationships
                relations = self.get_related_concepts(concept_name)
                for rel_type, rel_target, rel_sig in relations[:3]:
                    lines.append(f"  → {rel_type}: {rel_target} ({rel_sig})")

        return "\n".join(lines)
