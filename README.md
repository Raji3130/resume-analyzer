#  Smart Resume Analyzer & Job-Fit Predictor

An NLP/ML tool that scores how well a resume matches a job description,
highlights missing skills, and suggests concrete improvements — the kind
of thing an ATS (Applicant Tracking System) does, but transparent and
open-source.

**[Live Demo](#deployment)** • **[How it works](#-how-it-works)** • **[Run locally](#-running-locally)**

---

##  Problem

Job seekers rarely know *why* their resume doesn't get a callback, and
manually comparing a resume against a job description for keyword/skill
gaps is tedious. This tool automates that comparison and gives an
actionable, ranked list of what to fix.

##  Features

- **Multi-format resume parsing** — PDF, DOCX, and TXT
- **Job-fit score (0-100%)** combining semantic text similarity + explicit skill overlap
- **Skill-gap analysis** — ranks missing skills by how much the JD emphasizes them
- **Actionable suggestions** — rule-based recommendations tailored to the gap
- **Zero external API dependency** — runs fully offline/locally, no API keys needed

##  How it works

```
Resume (PDF/DOCX/TXT) ──┐
                         ├─▶ Text extraction ─▶ Skill extraction (regex-based
Job Description (text) ─┘                       taxonomy matching, 100+ skills)
                                                          │
                         ┌────────────────────────────────┘
                         ▼
         ┌───────────────────────────────┐
         │  Text similarity (TF-IDF +    │  40% weight
         │  cosine similarity)           │
         ├───────────────────────────────┤
         │  Skill overlap ratio          │  60% weight
         │  (resume skills ∩ JD skills)  │
         └───────────────────────────────┘
                         │
                         ▼
              Final Job-Fit Score + Gap Report
```

The skill taxonomy (`src/skills_db.py`) covers ~150 skills across
programming languages, data science/ML, data engineering, databases,
cloud/DevOps, and soft skills — organized so it's easy to extend.

**Design tradeoff worth noting:** this uses TF-IDF and regex-based skill
matching rather than a heavyweight NLP model (spaCy/transformers). This
keeps the tool dependency-light and fully offline, at the cost of not
catching skill *synonyms* it doesn't already know about. See
[Roadmap](#-roadmap) for the planned embeddings upgrade.

##  Example

Using the sample resume/JD in `data/`:

| Metric | Value |
|---|---|
| Final Job-Fit Score | 23.3% |
| Matched Skills | `aws`, `machine learning`, `python`, `sql` |
| Top Missing Skills | `docker`, `kubernetes`, `mlops`, `pytorch`, `tensorflow` |

##  Running locally

```bash
git clone https://github.com/<your-username>/smart-resume-analyzer.git
cd smart-resume-analyzer
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`),
upload a resume from `data/sample_resume.txt` (or your own), paste the
sample JD from `data/sample_jd.txt`, and click **Analyze Fit**.

##  Running tests

```bash
python -m pytest tests/ -v
```

##  Deployment

This app is a single Streamlit file with no external API keys, so it
deploys directly to:
- **[Streamlit Community Cloud](https://streamlit.io/cloud)** (free) — connect your GitHub repo, point it at `app.py`
- **[Hugging Face Spaces](https://huggingface.co/spaces)** (free) — select the Streamlit SDK

##  Project structure

```
smart-resume-analyzer/
├── app.py                  # Streamlit UI
├── src/
│   ├── resume_parser.py    # PDF/DOCX/TXT text extraction
│   ├── skill_extractor.py  # Regex-based skill matching against taxonomy
│   ├── matcher.py          # Scoring engine (TF-IDF + skill overlap)
│   └── skills_db.py        # Curated skills taxonomy (~150 skills, 7 categories)
├── tests/
│   └── test_matcher.py     # Unit tests for extraction & scoring logic
├── data/
│   ├── sample_resume.txt
│   └── sample_jd.txt
└── requirements.txt

```
##  Tech Stack

Python · Streamlit · scikit-learn (TF-IDF) · pdfplumber · python-docx

## 📄 License

MIT
