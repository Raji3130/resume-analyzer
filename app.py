"""
Smart Resume Analyzer & Job-Fit Predictor
Streamlit UI entry point.

Run with: streamlit run app.py
"""

import streamlit as st

from src.resume_parser import parse_resume, clean_text
from src.matcher import analyze

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="",
    layout="wide",
)

st.title("Smart Resume Analyzer & Job-Fit Predictor")
st.caption(
    "Upload a resume and paste a job description to get a fit score, "
    "skill-gap analysis, and improvement suggestions."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload your resume")
    uploaded_file = st.file_uploader(
        "PDF, DOCX or TXT", type=["pdf", "docx", "txt"]
    )

with col2:
    st.subheader("2. Paste the job description")
    jd_text_input = st.text_area("Job description", height=250)

analyze_clicked = st.button(" Analyze Fit", type="primary")

if analyze_clicked:
    if not uploaded_file:
        st.error("Please upload a resume first.")
    elif not jd_text_input.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            try:
                raw_resume_text = parse_resume(uploaded_file, uploaded_file.name)
                resume_text = clean_text(raw_resume_text)
                jd_text = clean_text(jd_text_input)

                if not resume_text:
                    st.error(
                        "Couldn't extract any text from that file. "
                        "If it's a scanned/image-based PDF, try a text-based one."
                    )
                else:
                    result = analyze(resume_text, jd_text)

                    st.divider()
                    score = result["final_score_pct"]

                    score_col, metric_col1, metric_col2 = st.columns([1, 1, 1])
                    with score_col:
                        st.metric("Overall Job-Fit Score", f"{score}%")
                    with metric_col1:
                        st.metric(
                            "Skill Overlap",
                            f"{round(result['skill_overlap_ratio'] * 100, 1)}%",
                        )
                    with metric_col2:
                        st.metric(
                            "Text Similarity",
                            f"{round(result['text_similarity'] * 100, 1)}%",
                        )

                    st.progress(min(int(score), 100))

                    st.divider()
                    tab1, tab2, tab3 = st.tabs(
                        ["Matched Skills", "Missing Skills", "Suggestions"]
                    )

                    with tab1:
                        if result["matched_skills"]:
                            st.write(", ".join(
                                f"`{s}`" for s in result["matched_skills"]
                            ))
                        else:
                            st.info("No overlapping skills detected.")

                    with tab2:
                        if result["missing_skills"]:
                            st.write(
                                "Skills the JD mentions that weren't found in "
                                "your resume, ranked by priority:"
                            )
                            st.write(", ".join(
                                f"`{s}`" for s in result["missing_skills"]
                            ))
                        else:
                            st.success("No missing skills detected — great coverage!")

                    with tab3:
                        for suggestion in result["suggestions"]:
                            st.write(f"- {suggestion}")

            except ValueError as e:
                st.error(str(e))

st.divider()
with st.expander("How the score is calculated"):
    st.markdown(
        """
        The final score blends two signals:
        - **Text similarity (40%)**: TF-IDF + cosine similarity between the
          full resume and job description text.
        - **Skill overlap (60%)**: fraction of JD-mentioned skills (from a
          curated skills taxonomy) that also appear in the resume.

        This is a transparent, fully local baseline (no external APIs).
        A natural phase-2 upgrade is swapping TF-IDF for sentence-transformer
        embeddings for deeper semantic matching — see the README.
        """
    )
