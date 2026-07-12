"""
Core matching engine.

Combines two signals into a final job-fit score:
  1. Semantic/textual similarity (TF-IDF + cosine similarity) between the
     full resume text and the full job description text.
  2. Explicit skill overlap (from skill_extractor) between resume and JD.

Phase-2 upgrade path (documented in README): swap the TF-IDF vectorizer
for sentence-transformer embeddings for better semantic matching once
you have internet access to pull a pretrained model.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.skill_extractor import extract_skills

# Weights for combining the two signals into a final score.
TEXT_SIMILARITY_WEIGHT = 0.4
SKILL_OVERLAP_WEIGHT = 0.6


def compute_text_similarity(resume_text: str, jd_text: str) -> float:
    """TF-IDF cosine similarity between resume and job description, 0-1."""
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    except ValueError:
        # Happens if one of the texts is empty after stopword removal.
        return 0.0
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(similarity), 4)


def compute_skill_overlap(resume_skills: dict, jd_skills: dict) -> dict:
    """
    Compare skill sets and return overlap stats + missing skills.
    resume_skills / jd_skills are {skill: count} dicts from extract_skills.
    """
    resume_set = set(resume_skills.keys())
    jd_set = set(jd_skills.keys())

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    extra = sorted(resume_set - jd_set)

    overlap_ratio = len(matched) / len(jd_set) if jd_set else 0.0

    # Rank missing skills by how often the JD emphasizes them - higher
    # mention count in the JD suggests higher priority to add/learn.
    missing_ranked = sorted(missing, key=lambda s: -jd_skills.get(s, 0))

    return {
        "matched": matched,
        "missing": missing_ranked,
        "extra": extra,
        "overlap_ratio": round(overlap_ratio, 4),
    }


def generate_suggestions(overlap_result: dict, text_similarity: float) -> list:
    """Simple rule-based suggestions. Swap for an LLM call for phase-2."""
    suggestions = []

    missing = overlap_result["missing"]
    if missing:
        top_missing = missing[:5]
        suggestions.append(
            "Add these JD-relevant skills to your resume if you have them: "
            + ", ".join(top_missing)
        )

    if overlap_result["overlap_ratio"] < 0.4:
        suggestions.append(
            "Your skill overlap with this JD is low - consider whether this "
            "role is a strong fit, or tailor your resume's language to match "
            "the JD's terminology more closely."
        )

    if text_similarity < 0.15:
        suggestions.append(
            "Overall phrasing differs a lot from the JD. Mirror key phrases "
            "from the job description (e.g. exact tool/framework names) "
            "since many ATS systems do literal keyword matching."
        )

    if not overlap_result["extra"]:
        suggestions.append(
            "Consider adding a couple of standout skills beyond the JD's "
            "requirements to differentiate yourself."
        )

    if not suggestions:
        suggestions.append("Strong match! Focus on quantifying your achievements "
                            "for these overlapping skills with concrete metrics.")

    return suggestions


def analyze(resume_text: str, jd_text: str) -> dict:
    """
    Main entry point: given raw resume text and JD text, return a full
    analysis dict ready to render in the UI.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    text_similarity = compute_text_similarity(resume_text, jd_text)
    overlap_result = compute_skill_overlap(resume_skills, jd_skills)

    final_score = (
        TEXT_SIMILARITY_WEIGHT * text_similarity
        + SKILL_OVERLAP_WEIGHT * overlap_result["overlap_ratio"]
    )
    final_score_pct = round(final_score * 100, 1)

    suggestions = generate_suggestions(overlap_result, text_similarity)

    return {
        "final_score_pct": final_score_pct,
        "text_similarity": text_similarity,
        "skill_overlap_ratio": overlap_result["overlap_ratio"],
        "matched_skills": overlap_result["matched"],
        "missing_skills": overlap_result["missing"],
        "extra_skills": overlap_result["extra"],
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "suggestions": suggestions,
    }
