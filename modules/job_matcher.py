"""
modules/job_matcher.py
Module 2: Job Intelligence
- Extracts required skills from Job Descriptions (JD)
- Computes multi-level matching:
  1. Exact Skill Overlap (Matched, Missing, Additional skills)
  2. Jaccard Skill Coverage Score
  3. TF-IDF Cosine Similarity for semantic text alignment (Scikit-Learn)
  4. Composite Match Index (Weighted combination)
- Benchmarks profile against standard campus placement role profiles
"""

import re
from typing import Dict, List, Any, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.skill_database import ALL_SKILLS, get_skill_category
from modules.resume_parser import extract_skills_from_text


# Predefined campus job roles for automated recommendations
BENCHMARK_JOB_ROLES = [
    {
        "role": "Software Development Engineer (SDE) - Backend",
        "category": "Software Engineering",
        "required_skills": ["python", "java", "sql", "data structures", "algorithms", "rest api", "git", "linux", "dbms", "docker"],
        "min_cgpa": 7.0,
        "description": "Looking for backend engineers skilled in Python or Java, data structures, algorithms, databases (SQL), and REST APIs."
    },
    {
        "role": "Data Scientist / ML Engineer",
        "category": "AI & Data Science",
        "required_skills": ["python", "machine learning", "deep learning", "pandas", "numpy", "scikit-learn", "sql", "data analysis", "nlp"],
        "min_cgpa": 7.5,
        "description": "Responsible for developing ML and NLP models, exploratory data analysis with pandas/numpy, and productionizing models."
    },
    {
        "role": "Frontend / Full Stack Web Developer",
        "category": "Web Development",
        "required_skills": ["javascript", "typescript", "react", "html", "css", "node.js", "git", "rest api", "tailwind css", "mongodb"],
        "min_cgpa": 6.5,
        "description": "Building interactive web UIs using React, TypeScript, HTML, CSS with modern responsive design and REST API integrations."
    },
    {
        "role": "Cloud & DevOps Associate",
        "category": "Infrastructure & Cloud",
        "required_skills": ["linux", "aws", "docker", "kubernetes", "ci/cd", "git", "bash", "python", "terraform"],
        "min_cgpa": 6.5,
        "description": "Designing deployment pipelines, managing Docker containers, Kubernetes clusters, and cloud infrastructure on AWS/GCP."
    },
    {
        "role": "Junior Data Analyst",
        "category": "Analytics",
        "required_skills": ["sql", "python", "power bi", "tableau", "data analysis", "communication", "pandas", "problem solving"],
        "min_cgpa": 6.0,
        "description": "Creating actionable dashboards in Power BI/Tableau, executing complex SQL queries, and presenting insights to stakeholders."
    }
]


def extract_job_skills(job_description_text: str) -> List[str]:
    """Extract recognized technical and domain skills from the job description."""
    return extract_skills_from_text(job_description_text)


def compute_tfidf_similarity(resume_text: str, job_text: str) -> float:
    """
    Compute Cosine Similarity between resume text and job description using TF-IDF.
    Returns float score between 0.0 and 100.0.
    """
    try:
        if not resume_text.strip() or not job_text.strip():
            return 0.0
        
        # Stopwords removed, unigrams and bigrams for context
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score) * 100, 2)
    except Exception:
        return 0.0


def match_resume_to_job(resume_text: str, resume_skills: List[str], job_text: str) -> Dict[str, Any]:
    """
    Perform deep skill comparison and similarity scoring between resume and job.
    """
    job_skills = extract_job_skills(job_text)
    
    resume_skill_set: Set[str] = set(s.lower() for s in resume_skills)
    job_skill_set: Set[str] = set(s.lower() for s in job_skills)
    
    matched_skills = sorted(list(resume_skill_set.intersection(job_skill_set)))
    missing_skills = sorted(list(job_skill_set.difference(resume_skill_set)))
    additional_skills = sorted(list(resume_skill_set.difference(job_skill_set)))
    
    # Skill Coverage Ratio (Percentage of job skills candidate has)
    if job_skill_set:
        skill_coverage_score = round((len(matched_skills) / len(job_skill_set)) * 100, 1)
    else:
        skill_coverage_score = 0.0
        
    # Semantic text similarity via TF-IDF
    tfidf_score = compute_tfidf_similarity(resume_text, job_text)
    
    # Composite Score: 60% skill requirement coverage + 40% textual relevance
    composite_score = round((skill_coverage_score * 0.6) + (tfidf_score * 0.4), 1)
    
    # Recommendation status
    if composite_score >= 70:
        fit_status = "High Match - Highly Recommended to Apply"
        badge_color = "green"
    elif composite_score >= 45:
        fit_status = "Moderate Match - Address Key Skill Gaps Before Applying"
        badge_color = "orange"
    else:
        fit_status = "Low Match - Significant Skill Gaps Identified"
        badge_color = "red"
        
    return {
        "composite_score": composite_score,
        "skill_coverage_score": skill_coverage_score,
        "tfidf_score": tfidf_score,
        "fit_status": fit_status,
        "badge_color": badge_color,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "total_required_skills": len(job_skill_set),
        "total_matched_skills": len(matched_skills),
    }


def recommend_jobs_for_resume(resume_text: str, resume_skills: List[str]) -> List[Dict[str, Any]]:
    """
    Compare resume against all benchmark roles and return ranked list of matches.
    """
    recommendations = []
    for job in BENCHMARK_JOB_ROLES:
        match_result = match_resume_to_job(resume_text, resume_skills, job["description"])
        
        # Also compute direct skill coverage against explicit required_skills
        req_set = set(job["required_skills"])
        cand_set = set(s.lower() for s in resume_skills)
        matched = sorted(list(req_set.intersection(cand_set)))
        missing = sorted(list(req_set.difference(cand_set)))
        coverage = round((len(matched) / len(req_set)) * 100, 1)
        
        recommendations.append({
            "role": job["role"],
            "category": job["category"],
            "min_cgpa": job["min_cgpa"],
            "required_skills": job["required_skills"],
            "matched_skills": matched,
            "missing_skills": missing,
            "skill_coverage": coverage,
            "composite_score": round((coverage * 0.7) + (match_result["tfidf_score"] * 0.3), 1),
            "description": job["description"]
        })
        
    # Sort recommendations by highest score descending
    recommendations.sort(key=lambda x: x["composite_score"], reverse=True)
    return recommendations
