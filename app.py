"""
Streamlit UI for the Offline Intelligent Sinhala Open-Ended Answer Scorer.
Provides question selection, answer input, and displays score breakdown with explanations.
"""
import os
# Force offline mode BEFORE any HuggingFace imports
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import streamlit as st
import sys
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from marking.marking_guides import MARKING_GUIDES, get_marking_guide, get_all_questions
from agents.orchestrator import OrchestratorAgent

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="සිංහල පිළිතුරු ඇගයීම් පද්ධතිය",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* System fonts - no network required */

    /* Global */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #050a1f 0%, #010308 100%);
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #010308;
    }
    ::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #8b5cf6;
    }

    /* Main container */
    .main .block-container {
        padding-top: 3rem;
        max-width: 1200px;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.7), rgba(2, 6, 23, 0.9));
        border-radius: 20px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.15), inset 0 0 20px rgba(139, 92, 246, 0.05);
        backdrop-filter: blur(20px);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(139,92,246,0.1) 0%, transparent 70%);
        pointer-events: none;
    }

    .main-header h1 {
        font-family: 'Noto Sans Sinhala', sans-serif;
        background: linear-gradient(to right, #00f2fe 0%, #4facfe 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 0 40px rgba(79, 172, 254, 0.4);
    }

    .main-header p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 0.8rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 15px 35px -10px rgba(56, 189, 248, 0.2);
    }

    /* Score display */
    .score-card {
        text-align: center;
        padding: 3rem;
        background: radial-gradient(circle at center, rgba(30, 27, 75, 0.8) 0%, rgba(2, 6, 23, 0.9) 100%);
        border: 1px solid rgba(167, 139, 250, 0.4);
        border-radius: 24px;
        margin: 2rem 0;
        box-shadow: 0 0 40px rgba(139, 92, 246, 0.2), inset 0 0 30px rgba(167, 139, 250, 0.1);
        position: relative;
    }

    .score-number {
        font-size: 5.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        filter: drop-shadow(0 0 20px rgba(0, 242, 254, 0.4));
    }

    .score-label {
        font-size: 1.3rem;
        color: #cbd5e1;
        margin-top: 1rem;
        font-weight: 500;
    }

    /* Criterion row */
    .criterion-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding: 1.2rem;
        margin: 0.8rem 0;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 12px;
        border-left: 4px solid;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .criterion-row:hover {
        background: rgba(30, 41, 59, 0.7);
        transform: scale(1.01);
    }

    .criterion-pass { border-left-color: #10b981; box-shadow: -4px 0 15px rgba(16, 185, 129, 0.2); }
    .criterion-partial { border-left-color: #f59e0b; box-shadow: -4px 0 15px rgba(245, 158, 11, 0.2); }
    .criterion-fail { border-left-color: #ef4444; box-shadow: -4px 0 15px rgba(239, 68, 68, 0.2); }

    .criterion-name {
        font-weight: 700;
        color: #f8fafc;
        font-size: 1.05rem;
        letter-spacing: 0.5px;
    }

    .criterion-score {
        font-weight: 800;
        font-size: 1.4rem;
        white-space: nowrap;
        margin-left: 1.5rem;
        background: rgba(0,0,0,0.3);
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
    }

    .criterion-justification {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 0.5rem;
        line-height: 1.6;
        font-family: 'Noto Sans Sinhala', sans-serif;
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .badge-excellent { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); box-shadow: 0 0 10px rgba(16, 185, 129, 0.2); }
    .badge-good { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 0 10px rgba(59, 130, 246, 0.2); }
    .badge-average { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); box-shadow: 0 0 10px rgba(245, 158, 11, 0.2); }
    .badge-poor { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); box-shadow: 0 0 10px rgba(239, 68, 68, 0.2); }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; right: 0; bottom: 0; width: 1px;
        background: linear-gradient(to bottom, transparent, #38bdf8, transparent);
        opacity: 0.5;
    }

    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #38bdf8;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* Workflow step */
    .workflow-step {
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        font-size: 0.95rem;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        display: flex;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .workflow-step:hover {
        background: rgba(30, 41, 59, 0.9);
        border-color: rgba(56, 189, 248, 0.3);
    }

    /* Concept tag */
    .concept-found {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 8px;
        font-size: 0.9rem;
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.1);
    }

    .concept-missing {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 8px;
        font-size: 0.9rem;
        background: rgba(239, 68, 68, 0.1);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    /* Fix text area colors */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.7) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
        font-family: 'Noto Sans Sinhala', sans-serif !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        line-height: 1.6 !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.3) !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2), inset 0 2px 10px rgba(0,0,0,0.3) !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        padding: 0.8rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6), inset 0 1px 0 rgba(255,255,255,0.3) !important;
        background: linear-gradient(135deg, #0284c7, #4f46e5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        font-weight: 600 !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 8px !important;
        color: white !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00f2fe, #4facfe, #f093fb) !important;
        border-radius: 10px !important;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ==================== INITIALIZE SESSION STATE ====================
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "grading_result" not in st.session_state:
    st.session_state.grading_result = None
if "is_grading" not in st.session_state:
    st.session_state.is_grading = False
if "prev_question" not in st.session_state:
    st.session_state.prev_question = None


def get_orchestrator():
    """Lazy-load the orchestrator agent."""
    if st.session_state.orchestrator is None:
        with st.spinner("🔄 Initializing agents..."):
            st.session_state.orchestrator = OrchestratorAgent()
    return st.session_state.orchestrator


def get_score_badge(score, max_marks):
    """Return appropriate badge based on score percentage."""
    pct = (score / max_marks * 100) if max_marks > 0 else 0
    if pct >= 80:
        return "badge-excellent", "Excellent"
    elif pct >= 60:
        return "badge-good", "Good"
    elif pct >= 40:
        return "badge-average", "Average"
    else:
        return "badge-poor", "Poor"


def get_criterion_class(score, max_marks):
    """Return CSS class for criterion row."""
    pct = (score / max_marks * 100) if max_marks > 0 else 0
    if pct >= 70:
        return "criterion-pass"
    elif pct >= 40:
        return "criterion-partial"
    else:
        return "criterion-fail"


# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>📝 සිංහල පිළිතුරු ඇගයීම් පද්ධතිය</h1>
    <p>Offline Intelligent Sinhala Open-Ended Answer Scorer | Anuradhapura Period</p>
    <p>OLLAMA + RAG + Ontology + Agent Architecture</p>
</div>
""", unsafe_allow_html=True)


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 📋 ප්‍රශ්න තේරීම")
    st.markdown("*Question Selection*")

    # Question selector
    questions = get_all_questions()
    question_options = {f"{qid}: {title}": qid for qid, title in questions.items()}

    selected = st.selectbox(
        "ප්‍රශ්නය තෝරන්න:",
        options=list(question_options.keys()),
        index=0,
        key="question_selector"
    )
    selected_qid = question_options[selected]
    guide = get_marking_guide(selected_qid)

    # Clear answer and results when question changes
    if st.session_state.prev_question != selected_qid:
        st.session_state.prev_question = selected_qid
        st.session_state.answer_input = ""
        st.session_state.grading_result = None

    st.markdown("---")

    # Display marking guide
    st.markdown("## 📊 ලකුණු ක්‍රමය")
    st.markdown("*Marking Guide*")

    if guide:
        for c in guide["criteria"]:
            st.markdown(f"**{c['name']}**: `{c['max_marks']}` marks")
            st.caption(c["description_si"])

        st.markdown(f"**මුළු ලකුණු / Total: `{guide['total_marks']}`**")

    st.markdown("---")
    st.markdown("### ⚙️ System Info")
    st.markdown(f"- **Model**: llama3:latest")
    st.markdown(f"- **RAG**: ChromaDB + MiniLM")
    st.markdown(f"- **Ontology**: Owlready2 OWL")
    st.markdown(f"- **Mode**: 🔒 Offline")


# ==================== MAIN CONTENT ====================
if guide:
    # Display question
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="color: #a78bfa; margin-top: 0;">
            ප්‍රශ්නය {selected_qid[-1]}: {guide['title']}
        </h3>
        <p style="font-size: 1.1rem; color: #e2e8f0; font-family: 'Noto Sans Sinhala', sans-serif; line-height: 1.8;">
            {guide['question']}
        </p>
        <p style="color: #60a5fa; font-size: 0.9rem;">මුළු ලකුණු: {guide['total_marks']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Answer input
    st.markdown("### ✍️ ඔබේ පිළිතුර ඇතුළත් කරන්න")
    st.markdown("*Enter your answer in Sinhala*")

    student_answer = st.text_area(
        label="Student Answer",
        height=200,
        placeholder="මෙහි ඔබේ සිංහල පිළිතුර ලියන්න...",
        key="answer_input",
        label_visibility="collapsed"
    )

    # Grade button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        grade_button = st.button(
            "⚖️ පිළිතුර ඇගයීම කරන්න (Grade Answer)",
            use_container_width=True,
            disabled=not student_answer.strip()
        )

    # ==================== GRADING WORKFLOW ====================
    if grade_button and student_answer.strip():
        st.markdown("---")
        st.markdown("### 🔄 ඇගයීම් ක්‍රියාවලිය (Grading Workflow)")

        # Progress container
        progress_placeholder = st.empty()
        status_container = st.container()

        with status_container:
            step_placeholders = {}
            for i, step_name in enumerate([
                "📚 Retrieval Agent: Searching knowledge base...",
                "🧠 Ontology Agent: Analyzing concepts...",
                "⚖️ Scoring Agent: Evaluating with LLM...",
                "✅ Validation Agent: Cross-checking scores...",
                "📝 Assembling final results..."
            ], 1):
                step_placeholders[i] = st.empty()
                step_placeholders[i].markdown(
                    f'<div class="workflow-step">⏳ Step {i}: {step_name}</div>',
                    unsafe_allow_html=True
                )

        def progress_callback(step, message):
            """Update progress in the UI."""
            if step in step_placeholders:
                icon = "✅" if "✅" in message else "⏳"
                step_placeholders[step].markdown(
                    f'<div class="workflow-step">{message}</div>',
                    unsafe_allow_html=True
                )

        # Run grading
        try:
            orchestrator = get_orchestrator()
            result = orchestrator.grade_answer(
                question_id=selected_qid,
                question_text=guide["question"],
                student_answer=student_answer,
                progress_callback=progress_callback
            )
            st.session_state.grading_result = result
        except Exception as e:
            st.error(f"Error during grading: {str(e)}")
            st.session_state.grading_result = None

    # ==================== DISPLAY RESULTS ====================
    result = st.session_state.grading_result
    if result:
        st.markdown("---")

        # Score Card
        total_score = result["total_score"]
        total_max = result["total_max"]
        badge_class, badge_text = get_score_badge(total_score, total_max)
        pct = (total_score / total_max * 100) if total_max > 0 else 0

        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{total_score}/{total_max}</div>
            <div class="score-label">
                <span class="status-badge {badge_class}">{badge_text}</span>
                &nbsp; ({pct:.0f}%)
            </div>
            <div style="margin-top: 0.5rem; color: #64748b; font-size: 0.85rem;">
                ⏱️ {result.get('elapsed_seconds', 0)}s | 🤖 {result.get('model_used', 'N/A')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        st.progress(pct / 100)

        # Criteria Breakdown
        st.markdown("### 📊 ලකුණු විභාජනය (Score Breakdown)")

        criteria_scores = result.get("criteria_scores", [])
        for cs in criteria_scores:
            awarded = cs.get("awarded_marks", 0)
            max_m = cs.get("max_marks", 0)
            name = cs.get("criterion_name", "Unknown")
            justification = cs.get("justification_si", "")
            css_class = get_criterion_class(awarded, max_m)

            score_color = "#34d399" if awarded >= max_m * 0.7 else (
                "#fbbf24" if awarded >= max_m * 0.4 else "#f87171"
            )

            st.markdown(f"""
            <div class="criterion-row {css_class}">
                <div style="flex: 1;">
                    <div class="criterion-name">{name}</div>
                    <div class="criterion-justification">{justification}</div>
                </div>
                <div class="criterion-score" style="color: {score_color};">
                    {awarded}/{max_m}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Overall Feedback
        overall = result.get("overall_feedback", "")
        if overall:
            st.markdown("### 💬 සමස්ත ප්‍රතිපෝෂණය (Overall Feedback)")
            st.markdown(f"""
            <div class="glass-card">
                <p style="font-family: 'Noto Sans Sinhala', sans-serif; line-height: 1.8; color: #cbd5e1;">
                    {overall}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Expandable sections for evidence
        st.markdown("### 🔍 සාක්ෂි සහ සන්දර්භය (Evidence & Context)")

        # Validation Report
        with st.expander("✅ Validation Report (Consistency Checks)", expanded=False):
            val_report = result.get("validation_report", {})
            if val_report and val_report.get("checks"):
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Passed", f"{val_report.get('passed', 0)}/{val_report.get('total_checks', 0)}")
                col_b.metric("Warnings", str(val_report.get("warnings", 0)))
                col_c.metric("Corrected", str(val_report.get("corrected", 0)))

                for check in val_report.get("checks", []):
                    status = check.get("status", "")
                    icon = "✅" if status == "pass" else ("⚠️" if status == "warning" else "🔧")
                    st.markdown(f"{icon} **{check.get('check', '')}**: {check.get('detail', '')}")
            else:
                st.info("Validation data not available.")

        # Ontology Coverage
        with st.expander("🧠 Ontology Concept Coverage", expanded=False):
            onto_cov = result.get("ontology_coverage", {})
            if onto_cov and "coverage_percentage" in onto_cov:
                st.metric(
                    "Concept Coverage",
                    f"{onto_cov['coverage_percentage']}%",
                    f"{onto_cov.get('total_found', 0)}/{onto_cov.get('total_expected', 0)} concepts"
                )

                found = onto_cov.get("found_concepts", [])
                missing = onto_cov.get("missing_concepts", [])

                if found:
                    st.markdown("**✅ Found Concepts:**")
                    found_html = " ".join(
                        f'<span class="concept-found">{c["concept"]}</span>'
                        for c in found
                    )
                    st.markdown(found_html, unsafe_allow_html=True)

                if missing:
                    st.markdown("**❌ Missing Concepts:**")
                    missing_html = " ".join(
                        f'<span class="concept-missing">{c["concept"]}</span>'
                        for c in missing
                    )
                    st.markdown(missing_html, unsafe_allow_html=True)
            else:
                st.info("Ontology coverage data not available.")

        # Retrieved Documents
        with st.expander("📚 Retrieved Documents (RAG)", expanded=False):
            docs = result.get("retrieved_documents", [])
            if docs:
                for i, doc in enumerate(docs, 1):
                    st.markdown(f"**Source {i}: {doc.get('source', 'N/A')}** "
                                f"(similarity: {doc.get('similarity', 0):.3f})")
                    st.text(doc.get("content", "")[:300] + "...")
                    st.markdown("---")
            else:
                st.info("No documents retrieved.")

        # Workflow Log
        with st.expander("📋 Workflow Log", expanded=False):
            log = result.get("workflow_log", [])
            for entry in log:
                st.markdown(
                    f'<div class="workflow-step">'
                    f'[{entry["timestamp"]:.1f}s] {entry["message"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )
