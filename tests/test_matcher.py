"""
Basic unit tests for the core logic (no Streamlit needed to run these).

Run with: python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.skill_extractor import extract_skills
from src.matcher import analyze, compute_text_similarity


def test_extract_skills_finds_known_skills():
    text = "Experienced in Python, SQL and Machine Learning."
    skills = extract_skills(text)
    assert "python" in skills
    assert "sql" in skills
    assert "machine learning" in skills


def test_extract_skills_ignores_substrings():
    # 'r' should not match inside "experience" etc.
    text = "I have great experience in customer service."
    skills = extract_skills(text)
    assert "r" not in skills


def test_text_similarity_identical_texts():
    text = "Python developer with machine learning experience."
    score = compute_text_similarity(text, text)
    assert score > 0.9


def test_text_similarity_unrelated_texts():
    resume = "Python data scientist with machine learning skills."
    jd = "Looking for a chef experienced in French cuisine."
    score = compute_text_similarity(resume, jd)
    assert score < 0.2


def test_analyze_returns_expected_keys():
    resume = "Python, SQL, Machine Learning, Communication"
    jd = "Python, AWS, Docker, Communication"
    result = analyze(resume, jd)
    expected_keys = {
        "final_score_pct", "text_similarity", "skill_overlap_ratio",
        "matched_skills", "missing_skills", "extra_skills",
        "resume_skills", "jd_skills", "suggestions",
    }
    assert expected_keys.issubset(result.keys())


def test_analyze_missing_skills_ranked_by_jd_priority():
    resume = "Python developer."
    jd = "Docker Docker Docker AWS. Python required."
    result = analyze(resume, jd)
    # 'docker' mentioned 3x in JD should rank above 'aws' mentioned once
    assert result["missing_skills"][0] == "docker"


if __name__ == "__main__":
    test_extract_skills_finds_known_skills()
    test_extract_skills_ignores_substrings()
    test_text_similarity_identical_texts()
    test_text_similarity_unrelated_texts()
    test_analyze_returns_expected_keys()
    test_analyze_missing_skills_ranked_by_jd_priority()
    print("All tests passed!")
