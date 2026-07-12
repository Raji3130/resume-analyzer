"""
Curated skills taxonomy used for extraction & gap analysis.
Organized by category so the UI can show grouped results.
Extend this dictionary as you add more domains (this is intentionally
kept as plain Python data so it's trivial to grow without touching logic).
"""

SKILLS_DB = {
    "programming_languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "r",
        "sql", "scala", "go", "golang", "rust", "matlab", "julia", "bash",
        "shell scripting", "html", "css"
    ],
    "data_science_ml": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "reinforcement learning", "neural networks",
        "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras",
        "pandas", "numpy", "matplotlib", "seaborn", "xgboost", "lightgbm",
        "feature engineering", "hyperparameter tuning", "model deployment",
        "time series analysis", "statistics", "a/b testing", "hypothesis testing",
        "regression", "classification", "clustering", "recommendation systems",
        "generative ai", "llm", "large language models", "transformers",
        "bert", "gpt", "langchain", "rag", "prompt engineering", "opencv"
    ],
    "data_engineering": [
        "etl", "data pipeline", "apache spark", "pyspark", "hadoop", "kafka",
        "airflow", "data warehousing", "snowflake", "redshift", "bigquery",
        "dbt", "data modeling"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "oracle", "cassandra",
        "redis", "elasticsearch", "dynamodb", "nosql"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "ci/cd", "jenkins", "terraform", "ansible", "git", "github actions",
        "linux", "microservices", "rest api", "fastapi", "flask", "django",
        "streamlit", "mlops", "model monitoring"
    ],
    "tools_visualization": [
        "tableau", "power bi", "excel", "jupyter", "google analytics",
        "looker", "plotly", "d3.js"
    ],
    "soft_skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "project management", "stakeholder management", "agile", "scrum",
        "critical thinking", "collaboration", "presentation skills",
        "time management", "mentoring"
    ],
}


def flatten_skills():
    """Return a flat sorted list of all known skills across categories."""
    all_skills = []
    for skills in SKILLS_DB.values():
        all_skills.extend(skills)
    return sorted(set(all_skills), key=len, reverse=True)


def skill_category(skill: str):
    """Return the category a given skill belongs to (or 'other')."""
    skill_lower = skill.lower()
    for category, skills in SKILLS_DB.items():
        if skill_lower in skills:
            return category
    return "other"
