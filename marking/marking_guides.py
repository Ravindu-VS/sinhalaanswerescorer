"""
Marking guides for all 5 Anuradhapura Period questions.
Each question has: text (Sinhala), criteria list with marks, and expected concepts.
"""

MARKING_GUIDES = {
    "Q1": {
        "id": "Q1",
        "title": "ජලාශ ශිෂ්ටාචාරය (Irrigation Civilization)",
        "question": (
            "අනුරාධපුර රාජධානියේ ජල සම්පාදන ක්‍රමය ගැන විස්තරාත්මකව සාකච්ඡා කරන්න. "
            "ප්‍රධාන ජලාශ, ඇළ මාර්ග සහ කෘෂිකර්මාන්තයට ඒවායේ බලපෑම පැහැදිලි කරන්න."
        ),
        "total_marks": 20,
        "criteria": [
            {
                "name": "ප්‍රධාන ජලාශ හඳුනාගැනීම",
                "description": "Naming key tanks: Abhaya Wewa, Tissa Wewa, Nuwara Wewa, Kala Wewa, Minneriya",
                "description_si": "ප්‍රධාන ජලාශ නම් කිරීම (අභය වැව, තිස්ස වැව, නුවර වැව, කලා වැව, මින්නේරිය)",
                "max_marks": 5
            },
            {
                "name": "ඇළ මාර්ග විස්තර කිරීම",
                "description": "Describing canal systems: Jaya Ganga/Yoda Ela, gradient technology",
                "description_si": "ඇළ මාර්ග පද්ධති විස්තර කිරීම (ජය ගඟ/යෝද ඇල, බෑවුම් තාක්ෂණය)",
                "max_marks": 4
            },
            {
                "name": "කෘෂිකර්මාන්තයට සම්බන්ධ කිරීම",
                "description": "Linking irrigation to agriculture, food security, and economic prosperity",
                "description_si": "ජලාශ ක්‍රමය කෘෂිකර්මාන්තයට, ආහාර සුරක්ෂිතතාවයට හා ආර්ථික සමෘද්ධියට සම්බන්ධ කිරීම",
                "max_marks": 4
            },
            {
                "name": "ජලාශ ඉදිකළ රජවරු",
                "description": "Mentioning key builders: Vasabha (11 tanks), Mahasena (Minneriya), Dhatusena (Kala Wewa)",
                "description_si": "ප්‍රධාන ජලාශ ඉදිකළ රජවරු සඳහන් කිරීම (වසභ, මහාසේන, ධාතුසේන)",
                "max_marks": 4
            },
            {
                "name": "සමස්ත ගුණාත්මකභාවය",
                "description": "Overall coherence, Sinhala quality, depth of analysis",
                "description_si": "සමස්ත සුසංගතතාව, සිංහල භාෂා ගුණාත්මකභාවය, විශ්ලේෂණයේ ගැඹුර",
                "max_marks": 3
            }
        ]
    },
    "Q2": {
        "id": "Q2",
        "title": "බුදුදහම හඳුන්වාදීම (Introduction of Buddhism)",
        "question": (
            "බුදුදහම ශ්‍රී ලංකාවට හඳුන්වා දුන් ආකාරය සහ අනුරාධපුර සමාජයට හා "
            "සංස්කෘතියට එයින් ඇති වූ බලපෑම් පැහැදිලි කරන්න."
        ),
        "total_marks": 20,
        "criteria": [
            {
                "name": "මහින්ද තෙරුන්ගේ මෙහෙවර",
                "description": "Mahinda's mission, Ashoka's role, Devanampiya Tissa's acceptance",
                "description_si": "මහින්ද තෙරුන්ගේ මෙහෙවර, අශෝක අධිරාජයාගේ කාර්යභාරය, දේවානම්පිය තිස්ස",
                "max_marks": 5
            },
            {
                "name": "ප්‍රධාන බෞද්ධ ස්ථාන",
                "description": "Key Buddhist sites: Thuparamaya, Sri Maha Bodhiya, Ruwanwelisaya",
                "description_si": "ප්‍රධාන බෞද්ධ ස්ථාන (ථූපාරාමය, ශ්‍රී මහා බෝධිය, රුවන්වැලිසෑය)",
                "max_marks": 4
            },
            {
                "name": "ත්‍රිවිධ නිකාය",
                "description": "Three monastic fraternities: Mahavihara, Abhayagiri, Jetavana",
                "description_si": "සාමනේර සම්ප්‍රදාය තුන (මහාවිහාරය, අභයගිරිය, ජේතවනය)",
                "max_marks": 4
            },
            {
                "name": "සමාජ හා සංස්කෘතික බලපෑම",
                "description": "Impact on governance, law, art, culture, and education",
                "description_si": "පාලනයට, නීතියට, කලාවට, සංස්කෘතියට හා අධ්‍යාපනයට බලපෑම",
                "max_marks": 4
            },
            {
                "name": "සමස්ත ගුණාත්මකභාවය",
                "description": "Overall coherence, Sinhala quality, depth of analysis",
                "description_si": "සමස්ත සුසංගතතාව, සිංහල භාෂා ගුණාත්මකභාවය, විශ්ලේෂණයේ ගැඹුර",
                "max_marks": 3
            }
        ]
    },
    "Q3": {
        "id": "Q3",
        "title": "ප්‍රධාන රජවරුන් (Key Rulers & Contributions)",
        "question": (
            "අනුරාධපුර යුගයේ ප්‍රධාන රජවරුන් තිදෙනෙකු තෝරා ඔවුන්ගේ පාලන කාලය, "
            "ජයග්‍රහණ සහ ශ්‍රී ලංකාවට කළ දායකත්වය සාකච්ඡා කරන්න."
        ),
        "total_marks": 20,
        "criteria": [
            {
                "name": "රජවරු හඳුනාගැනීම",
                "description": "Correctly identifying 3 major rulers with reign periods",
                "description_si": "ප්‍රධාන රජවරු තිදෙනෙකු නිවැරදිව හඳුනාගැනීම සහ පාලන කාල සඳහන් කිරීම",
                "max_marks": 5
            },
            {
                "name": "යුද්ධමය ජයග්‍රහණ",
                "description": "Describing military achievements (e.g., Dutugemunu vs. Elara)",
                "description_si": "යුද්ධමය ජයග්‍රහණ විස්තර කිරීම (උදා: දුටුගැමුණු vs එළාර)",
                "max_marks": 4
            },
            {
                "name": "යටිතල පහසුකම් දායකත්වය",
                "description": "Infrastructure and construction contributions",
                "description_si": "යටිතල පහසුකම් හා ඉදිකිරීම් දායකත්වය",
                "max_marks": 4
            },
            {
                "name": "ආගමික හා සංස්කෘතික දායකත්වය",
                "description": "Religious and cultural patronage",
                "description_si": "ආගමික හා සංස්කෘතික අනුග්‍රහය",
                "max_marks": 4
            },
            {
                "name": "සමස්ත ගුණාත්මකභාවය",
                "description": "Overall coherence, Sinhala quality, depth of analysis",
                "description_si": "සමස්ත සුසංගතතාව, සිංහල භාෂා ගුණාත්මකභාවය, විශ්ලේෂණයේ ගැඹුර",
                "max_marks": 3
            }
        ]
    },
    "Q4": {
        "id": "Q4",
        "title": "පරිපාලන ක්‍රමය (Administrative System)",
        "question": (
            "අනුරාධපුර රාජධානියේ පරිපාලන ව්‍යුහය විස්තර කරන්න. "
            "රජු, උපරාජවරුන්, රට විභාග සහ ග්‍රාමික නිලධාරීන්ගේ කාර්යභාරය පැහැදිලි කරන්න."
        ),
        "total_marks": 20,
        "criteria": [
            {
                "name": "රජුගේ බලතල",
                "description": "King's supreme authority and citadel",
                "description_si": "රජුගේ සර්වබලධාරී බලතල හා මහා ප්‍රාසාදය",
                "max_marks": 4
            },
            {
                "name": "පළාත් පරිපාලනය",
                "description": "Provincial system: Uvarajas, Ratas",
                "description_si": "පළාත් ක්‍රමය: උපරාජවරු, රට විභාග",
                "max_marks": 4
            },
            {
                "name": "ග්‍රාම පරිපාලනය",
                "description": "Village-level administration: Gamikas and their roles",
                "description_si": "ග්‍රාම මට්ටමේ පරිපාලනය: ග්‍රාමිකයන්ගේ කාර්යභාරය",
                "max_marks": 4
            },
            {
                "name": "නීතිය, බදු, ජල කළමනාකරණය",
                "description": "Law, taxation, and water distribution management",
                "description_si": "නීතිය, බදු ක්‍රමය, ජල බෙදාහැරීම කළමනාකරණය",
                "max_marks": 4
            },
            {
                "name": "සමස්ත ගුණාත්මකභාවය",
                "description": "Overall coherence, Sinhala quality, depth of analysis",
                "description_si": "සමස්ත සුසංගතතාව, සිංහල භාෂා ගුණාත්මකභාවය, විශ්ලේෂණයේ ගැඹුර",
                "max_marks": 4
            }
        ]
    },
    "Q5": {
        "id": "Q5",
        "title": "පරිහානිය (Decline of Anuradhapura)",
        "question": (
            "අනුරාධපුර රාජධානියේ පරිහානියට හේතු වූ සාධක සාකච්ඡා කරන්න. "
            "දකුණු ඉන්දීය ආක්‍රමණ, අභ්‍යන්තර ගැටුම් සහ රාජධානිය පොළොන්නරුවට "
            "මාරු කිරීම ගැන පැහැදිලි කරන්න."
        ),
        "total_marks": 20,
        "criteria": [
            {
                "name": "දකුණු ඉන්දීය ආක්‍රමණ",
                "description": "South Indian invasions: Chola, Pandya dynasties",
                "description_si": "දකුණු ඉන්දීය ආක්‍රමණ (චෝල, පාණ්ඩ්‍ය)",
                "max_marks": 5
            },
            {
                "name": "අභ්‍යන්තර ගැටුම්",
                "description": "Internal conflicts and succession disputes",
                "description_si": "අභ්‍යන්තර ගැටුම් සහ රාජ්‍ය අනුප්‍රාප්තික ආරවුල්",
                "max_marks": 4
            },
            {
                "name": "මහින්ද V සහ අනුරාධපුරයේ පතනය",
                "description": "Mahinda V's capture and fall of Anuradhapura (1017 CE)",
                "description_si": "මහින්ද V අල්ලා ගැනීම සහ ක්‍රි.ව. 1017 අනුරාධපුරයේ පතනය",
                "max_marks": 4
            },
            {
                "name": "පොළොන්නරුවට මාරු වීම",
                "description": "Shift to Polonnaruwa and its strategic reasons",
                "description_si": "පොළොන්නරුව අගනුවර ලෙස තෝරාගැනීම සහ එයට හේතු",
                "max_marks": 4
            },
            {
                "name": "සමස්ත ගුණාත්මකභාවය",
                "description": "Overall coherence, Sinhala quality, depth of analysis",
                "description_si": "සමස්ත සුසංගතතාව, සිංහල භාෂා ගුණාත්මකභාවය, විශ්ලේෂණයේ ගැඹුර",
                "max_marks": 3
            }
        ]
    }
}


def get_marking_guide(question_id):
    """Return the marking guide for a specific question."""
    return MARKING_GUIDES.get(question_id)


def get_all_questions():
    """Return a dict of question IDs to their titles."""
    return {qid: q["title"] for qid, q in MARKING_GUIDES.items()}


def format_marking_guide_for_llm(question_id):
    """Format the marking guide as a structured text for LLM prompt."""
    guide = get_marking_guide(question_id)
    if not guide:
        return ""

    lines = [
        f"### Marking Guide for: {guide['title']}",
        f"Total Marks: {guide['total_marks']}\n",
        "| # | Criterion | Max Marks | Description |",
        "|---|-----------|-----------|-------------|"
    ]

    for i, c in enumerate(guide["criteria"], 1):
        lines.append(f"| {i} | {c['name']} | {c['max_marks']} | {c['description_si']} |")

    return "\n".join(lines)
