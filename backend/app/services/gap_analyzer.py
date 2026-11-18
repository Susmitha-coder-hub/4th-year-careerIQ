"""
backend/app/services/gap_analyzer.py
Module 4: Skill Gap Analysis
Generates practical, ethical suggestions to bridge missing skills without fabricating experience.
"""

from typing import Dict, List, Any
from backend.app.services.skill_extractor import categorize_skills

def generate_skill_gap_suggestions(missing_skills: List[str]) -> List[Dict[str, str]]:
    """
    Produce constructive, actionable recommendations for candidate upskilling.
    Does NOT suggest falsely inserting skills into the resume.
    """
    suggestions = []
    if not missing_skills:
        return [{
            "type": "positive",
            "skill": "All Requirements Covered",
            "message": "Your resume text includes all explicit technical skills recognized in the target job description."
        }]

    for skill in missing_skills:
        skill_cap = skill.title()
        s_lower = skill.lower()
        if s_lower in ["docker", "kubernetes", "ci/cd", "terraform"]:
            suggestions.append({
                "type": "DevOps / Infrastructure",
                "skill": skill_cap,
                "action": f"Containerize one of your existing projects using {skill_cap} and document the container setup in your GitHub repository.",
                "recommended_course": f"{skill_cap} Essentials & Hands-on Lab (freeCodeCamp / Docker Official Docs)",
                "estimated_effort": "1–2 weeks (10 hours)",
                "practice_project": f"Create a Dockerfile and multi-container docker-compose setup for a web app + database."
            })
        elif s_lower in ["sql", "postgresql", "mysql", "mongodb", "redis"]:
            suggestions.append({
                "type": "Database & Querying",
                "skill": skill_cap,
                "action": f"Demonstrate schema design, query optimization, or indexing with {skill_cap} in a practical project.",
                "recommended_course": f"Relational Database Design & SQL Optimization (Khan Academy / PostgreSQL Docs)",
                "estimated_effort": "1 week (8 hours)",
                "practice_project": f"Build a database schema with indexing and benchmark complex JOIN queries vs unindexed tables."
            })
        elif s_lower in ["machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "scikit-learn"]:
            suggestions.append({
                "type": "AI & Machine Learning",
                "skill": skill_cap,
                "action": f"Build a reproducible end-to-end model pipeline with {skill_cap} and publish documentation with evaluation metrics.",
                "recommended_course": f"Machine Learning Specialization (DeepLearning.AI / Scikit-Learn Tutorials)",
                "estimated_effort": "3–4 weeks (25 hours)",
                "practice_project": f"Train, evaluate, and serialize a classification model with cross-validation and feature importance analysis."
            })
        elif s_lower in ["react", "node.js", "django", "fastapi", "flask", "spring boot"]:
            suggestions.append({
                "type": "Framework Competency",
                "skill": skill_cap,
                "action": f"Develop a functional CRUD or microservice application with {skill_cap} to substantiate practical familiarity.",
                "recommended_course": f"Full-Stack Web Development with {skill_cap} (Official Interactive Documentation)",
                "estimated_effort": "2–3 weeks (15 hours)",
                "practice_project": f"Create a REST API with authentication (JWT), pagination, and automated unit tests."
            })
        elif s_lower in ["data structures", "algorithms"]:
            suggestions.append({
                "type": "Core Computer Science",
                "skill": skill_cap,
                "action": f"Practice problem-solving on standardized coding platforms to prepare for initial technical assessment rounds.",
                "recommended_course": "NeetCode 150 / Striver's A2Z DSA Sheet (Free Community Roadmaps)",
                "estimated_effort": "3–4 weeks ongoing (2 hours/day)",
                "practice_project": "Implement 15 foundational DSA patterns (Two Pointers, Sliding Window, Trees, Graphs)."
            })
        else:
            suggestions.append({
                "type": "Domain Skill",
                "skill": skill_cap,
                "action": f"If you have hands-on exposure to {skill_cap}, ensure it is explicitly listed in your resume. Otherwise, allocate 1-2 weeks to study its core concepts.",
                "recommended_course": f"Introductory {skill_cap} Fundamentals (Documentation & Hands-on Tutorials)",
                "estimated_effort": "1–2 weeks (8 hours)",
                "practice_project": f"Implement a minimal working example utilizing {skill_cap} and commit to GitHub."
            })

    return suggestions

def perform_skill_gap_analysis(
    resume_skills: List[str],
    job_skills: List[str],
    matched_skills: List[str],
    missing_skills: List[str]
) -> Dict[str, Any]:
    """
    Format complete skill gap analysis data with domain categorization and guidance.
    """
    categorized_missing = categorize_skills(missing_skills)
    suggestions = generate_skill_gap_suggestions(missing_skills)

    return {
        "summary": {
            "total_job_skills": len(job_skills),
            "matched_count": len(matched_skills),
            "missing_count": len(missing_skills),
            "coverage_percentage": round((len(matched_skills) / len(job_skills) * 100), 1) if job_skills else 100.0
        },
        "categorized_missing": categorized_missing,
        "actionable_suggestions": suggestions,
        "disclaimer": (
            "A missing skill indicates that the term was not detected in the provided resume text. "
            "Never fabricate experience. Only list skills on your resume that you are prepared to discuss and demonstrate."
        )
    }
