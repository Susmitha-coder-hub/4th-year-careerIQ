"""
backend/app/services/matcher.py
Module 3: Resume and Job Matching
Calculates baseline TF-IDF vectorization and Cosine Similarity (0-100).
Clearly distinguishes text-similarity baseline from official ATS scores or hiring decisions.
"""

from typing import Dict, List, Any, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.services.skill_extractor import extract_skills_from_text, ALL_TAXONOMY_SKILLS

def compute_tfidf_similarity_score(resume_text: str, job_text: str) -> float:
    """
    Computes cosine similarity between resume and job description using TF-IDF.
    Returns baseline score bounded between 0.0 and 100.0.
    """
    if not resume_text.strip() or not job_text.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        # Bound score between 0.0 and 100.0
        score = max(0.0, min(100.0, float(sim) * 100.0))
        return round(score, 1)
    except Exception:
        return 0.0

def match_resume_and_job(
    resume_text: str,
    job_text: str,
    pre_extracted_resume_skills: List[str] = None
) -> Dict[str, Any]:
    """
    Complete matching pipeline:
    - TF-IDF baseline similarity score
    - Overlapping detected skills
    - Missing skills required by job description
    - Additional skills present in resume
    - Transparent caveat disclosure
    """
    # 1. Skill Extraction
    resume_skills = pre_extracted_resume_skills or extract_skills_from_text(resume_text)
    job_skills = extract_skills_from_text(job_text)

    resume_set: Set[str] = set(s.lower() for s in resume_skills)
    job_set: Set[str] = set(s.lower() for s in job_skills)

    matched_skills = sorted(list(resume_set.intersection(job_set)))
    missing_skills = sorted(list(job_set.difference(resume_set)))
    additional_skills = sorted(list(resume_set.difference(job_set)))

    # 2. Baseline Similarity Score
    similarity_score = compute_tfidf_similarity_score(resume_text, job_text)

    # 3. Skill Coverage Ratio
    skill_coverage_pct = round((len(matched_skills) / len(job_set) * 100), 1) if job_set else 0.0

    return {
        "similarity_score": similarity_score,
        "skill_coverage_percentage": skill_coverage_pct,
        "score_type": "TF-IDF Cosine Similarity Baseline",
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "resume_skills": sorted(list(resume_set)),
        "job_skills": sorted(list(job_set)),
        "explanation": (
            "This score reflects textual and vocabulary similarity calculated via TF-IDF n-gram vectorization. "
            "It is a baseline reference and does not represent an official ATS ranking or employment guarantee."
        )
    }
