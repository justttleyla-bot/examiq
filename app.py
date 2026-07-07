import streamlit as st
import tempfile
import os
from dotenv import load_dotenv
from extractor import extract_text_from_pdf, extract_questions, clean_text
from analyzer import analyze_exam, clean_topics_with_ai
from generator import generate_practice_questions, predict_likely_topics

load_dotenv()

st.set_page_config(page_title="ExamIQ", page_icon="✦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

.stApp { background: #f7f6f3 !important; }

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    max-width: 680px !important;
    padding: 3.5rem 1.5rem !important;
}

.hero-eyebrow {
    display: inline-block;
    background: #ede9fe;
    color: #6d28d9;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 100px;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #111;
    letter-spacing: -2px;
    line-height: 1.08;
    margin-bottom: 12px;
}

.hero-title em { font-style: normal; color: #7c3aed; }

.hero-sub {
    font-size: 1rem;
    color: #6b7280;
    line-height: 1.65;
    margin-bottom: 2.5rem;
}

.sec-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.6rem;
    margin-top: 1.75rem;
}

.stTextInput > div > div > input {
    background: #fff !important;
    border: 1.5px solid #e2ddd6 !important;
    border-radius: 10px !important;
    padding: 0.72rem 1rem !important;
    font-size: 0.93rem !important;
    color: #111 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}

.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #aaa !important;
}

/* File uploader — force white */
[data-testid="stFileUploader"] {
    background: #fff !important;
    border: 1.5px dashed #d1ccc4 !important;
    border-radius: 12px !important;
    padding: 0.25rem !important;
}

[data-testid="stFileUploadDropzone"] {
    background-color: #ffffff !important;
    color: #374151 !important;
    border: none !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploadDropzone"] > div {
    background-color: #ffffff !important;
}

[data-testid="stFileUploadDropzone"] button {
    background-color: #f3f4f6 !important;
    color: #111 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploadDropzone"] small {
    color: #6b7280 !important;
}

[data-testid="stFileUploaderFileName"] {
    color: #111 !important;
}

section[data-testid="stFileUploader"] * {
    color: #111 !important;
    background: transparent !important;
}

[data-testid="stFileUploaderFile"] {
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    color: #374151 !important;
}

.stButton > button {
    background: #111 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.68rem 1.5rem !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
    transition: all 0.15s !important;
}

.stButton > button:hover {
    background: #2d2d2d !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.18) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #fff !important;
    border: 1.5px solid #e2ddd6 !important;
    border-radius: 10px !important;
    color: #111 !important;
}

[data-testid="stSelectbox"] span {
    color: #111 !important;
    font-weight: 500 !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #a78bfa) !important;
}

.stats-row {
    display: flex;
    gap: 10px;
    margin: 1rem 0;
}

.stat-box {
    flex: 1;
    background: #fff;
    border: 1px solid #e9e6e0;
    border-radius: 12px;
    padding: 1.1rem 1rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.stat-n {
    font-size: 1.9rem;
    font-weight: 700;
    color: #111;
    letter-spacing: -1px;
    line-height: 1;
}

.stat-l {
    font-size: 0.7rem;
    color: #9ca3af;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 3px;
}

.pills { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 0.5rem; }
.pill {
    background: #f5f3ff;
    color: #5b21b6;
    border: 1px solid #ddd6fe;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 0.82rem;
    font-weight: 500;
}

.de { background:#f0fdf4; color:#15803d; border:1px solid #bbf7d0; border-radius:6px; padding:3px 9px; font-size:0.77rem; font-weight:500; margin-right:4px; display:inline-block; }
.dm { background:#fffbeb; color:#b45309; border:1px solid #fde68a; border-radius:6px; padding:3px 9px; font-size:0.77rem; font-weight:500; margin-right:4px; display:inline-block; }
.dh { background:#fef2f2; color:#b91c1c; border:1px solid #fecaca; border-radius:6px; padding:3px 9px; font-size:0.77rem; font-weight:500; margin-right:4px; display:inline-block; }

.exam-row {
    background: #fafaf9;
    border: 1px solid #ede9e3;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 8px;
}

.exam-nm {
    font-size: 0.86rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 7px;
}

.info-txt {
    font-size: 0.85rem;
    color: #6b7280;
    margin-bottom: 1rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# Session state
for key, val in {
    'analysis_done': False,
    'all_questions': [],
    'all_topics': [],
    'exam_texts': [],
    'analysis_results': [],
    'subject': "",
    'prediction': None,
    'generated': None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── HERO ──
st.markdown("""
<div class="hero-eyebrow">✦ AI-Powered Exam Prep</div>
<div class="hero-title">Study smarter<br>with <em>ExamIQ</em></div>
<div class="hero-sub">Upload your past exams and let AI predict what's coming next — then practice with generated questions in the same style.</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── SETUP ──
st.markdown('<div class="sec-label">Subject</div>', unsafe_allow_html=True)
subject = st.text_input("", placeholder="e.g. Operating Systems, Algorithms, Linear Algebra", label_visibility="collapsed")

st.markdown('<div class="sec-label">Upload Past Exams (PDF)</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type=['pdf'], accept_multiple_files=True, label_visibility="collapsed")

if uploaded_files:
    st.markdown(f'<p style="font-size:0.8rem;color:#7c3aed;font-weight:500;">✓ {len(uploaded_files)} file{"s" if len(uploaded_files)>1 else ""} ready</p>', unsafe_allow_html=True)

analyze_btn = st.button("Analyze Exams →")

# ── ANALYSIS ──
if analyze_btn and uploaded_files and subject:
    all_questions, all_topics, exam_texts, analysis_results = [], [], [], []
    prog = st.progress(0)
    status = st.empty()

    for i, f in enumerate(uploaded_files):
        status.markdown(f'<p style="font-size:0.85rem;color:#6b7280;">Reading <b>{f.name}</b>...</p>', unsafe_allow_html=True)
        prog.progress((i+1)/(len(uploaded_files)+1))

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(f.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        questions = extract_questions(text)
        analysis = analyze_exam(questions)
        all_questions.extend(questions)
        all_topics.extend(analysis['topics'])
        exam_texts.append(clean_text(text))
        analysis_results.append({"name": f.name, "analysis": analysis})
        os.unlink(tmp_path)

    status.markdown('<p style="font-size:0.85rem;color:#6b7280;">Cleaning topics with AI...</p>', unsafe_allow_html=True)
    prog.progress(0.95)
    cleaned = clean_topics_with_ai(list(set(all_topics)), subject)
    prog.progress(1.0)
    status.empty()
    prog.empty()

    st.session_state.update({
        'all_questions': all_questions,
        'all_topics': cleaned,
        'exam_texts': exam_texts,
        'analysis_results': analysis_results,
        'analysis_done': True,
        'subject': subject,
        'prediction': None,
        'generated': None,
    })

elif analyze_btn:
    st.warning("Please fill in the subject and upload at least one PDF.")

# ── RESULTS ──
if st.session_state.analysis_done:
    subject = st.session_state.subject
    total_q = len(st.session_state.all_questions)
    total_e = len(st.session_state.analysis_results)
    total_t = len(st.session_state.all_topics)

    st.markdown("---")

    # Stats
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box"><div class="stat-n">{total_e}</div><div class="stat-l">Exams</div></div>
        <div class="stat-box"><div class="stat-n">{total_q}</div><div class="stat-l">Questions</div></div>
        <div class="stat-box"><div class="stat-n">{total_t}</div><div class="stat-l">Topics</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Topics
    st.markdown('<div class="sec-label" style="margin-top:1.5rem;">Topics Detected</div>', unsafe_allow_html=True)
    pills = "".join([f'<span class="pill">{t}</span>' for t in st.session_state.all_topics])
    st.markdown(f'<div class="pills">{pills}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Difficulty
    st.markdown('<div class="sec-label">Difficulty Breakdown</div>', unsafe_allow_html=True)
    for r in st.session_state.analysis_results:
        dist = r['analysis']['difficulty_distribution']
        e, m, h = dist.get('Easy',0), dist.get('Medium',0), dist.get('Hard',0)
        total = e+m+h or 1
        st.markdown(f"""
        <div class="exam-row">
            <div class="exam-nm">{r['name']}</div>
            <span class="de">Easy {e}</span>
            <span class="dm">Medium {m}</span>
            <span class="dh">Hard {h}</span>
            <div style="margin-top:10px;background:#f0ede8;border-radius:4px;height:3px;overflow:hidden;display:flex;">
                <div style="width:{e/total*100:.0f}%;background:#16a34a;"></div>
                <div style="width:{m/total*100:.0f}%;background:#d97706;"></div>
                <div style="width:{h/total*100:.0f}%;background:#dc2626;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Prediction
    st.markdown('<div class="sec-label">AI Topic Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-txt">Based on patterns across your exams, here\'s what\'s likely on your next one.</div>', unsafe_allow_html=True)
    if st.button("Predict Likely Topics →"):
        with st.spinner("Analyzing patterns..."):
            st.session_state.prediction = predict_likely_topics(
                st.session_state.all_topics, subject, st.session_state.exam_texts
            )
    if st.session_state.prediction:
        st.markdown(st.session_state.prediction)

    st.markdown("---")

    # Generator
    st.markdown('<div class="sec-label">Generate Practice Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-txt">AI-generated questions that match your exam style and difficulty.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("Difficulty", ["Mixed", "Easy", "Medium", "Hard"])
    with col2:
        num_q = st.selectbox("Questions", [5, 10, 15, 20])

    if st.button("Generate Practice Questions →"):
        with st.spinner("Generating questions..."):
            st.session_state.generated = generate_practice_questions(
                st.session_state.all_topics, subject, difficulty, num_q,
                st.session_state.all_questions
            )
    if st.session_state.generated:
        st.markdown(st.session_state.generated)