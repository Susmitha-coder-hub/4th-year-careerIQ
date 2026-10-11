"""
backend/app/services/skill_extractor.py
Configurable skill taxonomy and transparent regex extraction logic.
Reusable across both resume parsing and job description analysis.
"""

import re
from typing import List, Dict, Set

# Configurable Skill Dictionary categorized by technical domain
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "c", "javascript", "typescript",
        "go", "golang", "rust", "ruby", "php", "swift", "kotlin", "r",
        "dart", "sql", "html", "css", "bash", "shell"
    ],
    "Web & Backend Frameworks": [
        "react", "angular", "vue", "next.js", "node.js", "express",
        "django", "flask", "fastapi", "spring", "spring boot", "asp.net",
        ".net", "laravel", "tailwind css", "bootstrap", "redux", "graphql", "rest api"
    ],
    "Data Science & AI/ML": [
        "machine learning", "deep learning", "natural language processing", "nlp",
        "computer vision", "artificial intelligence", "data analysis", "data science",
        "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas",
        "numpy", "scipy", "matplotlib", "seaborn", "tableau", "power bi"
    ],
    "Databases & Storage": [
        "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis",
        "oracle", "cassandra", "dynamodb", "firebase"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "google cloud", "gcp",
        "docker", "kubernetes", "jenkins", "git", "github", "gitlab",
        "ci/cd", "linux", "unix", "terraform"
    ],
    "Core Computer Science": [
        "data structures", "algorithms", "dsa", "object oriented programming", "oop",
        "system design", "operating systems", "computer networks", "dbms"
    ],
    "Professional & Soft Skills": [
        "communication", "teamwork", "problem solving", "leadership",
        "critical thinking", "agile", "scrum", "time management"
    ]
}

# Pre-compiled mapping for fast lookup
ALL_TAXONOMY_SKILLS: Set[str] = set()
SKILL_TO_CATEGORY: Dict[str, str] = {}

for cat, skills in SKILL_TAXONOMY.items():
    for skill in skills:
        s_lower = skill.lower()
        ALL_TAXONOMY_SKILLS.add(s_lower)
        SKILL_TO_CATEGORY[s_lower] = cat


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract recognized skills from arbitrary text using regex word-boundary matching.
    Handles short tokens like 'c', 'r', 'go' safely without partial match false positives.
    """
    if not text or not text.strip():
        return []

    # Normalize delimiters
    text_normalized = " " + text.lower() + " "
    clean_text = re.sub(r'[/,;:()•\n\r|\[\]{}]', ' ', text_normalized)

    detected: Set[str] = set()

    for skill in ALL_TAXONOMY_SKILLS:
        if len(skill) <= 2:
            # Stricter word boundary for single/2-letter tokens
            pattern = rf'(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])'
        else:
            pattern = rf'(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])'

        if re.search(pattern, clean_text):
            detected.add(skill)

    # Return sorted alphabetical list
    return sorted(list(detected))


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """Group a list of skills into domain categories."""
    categorized: Dict[str, List[str]] = {}
    for s in skills:
        cat = SKILL_TO_CATEGORY.get(s.lower(), "Other / Domain-Specific")
        categorized.setdefault(cat, []).append(s)
    return categorized
