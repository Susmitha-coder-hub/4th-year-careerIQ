"""
utils/skill_database.py
Taxonomy of technical skills, tools, frameworks, and domains for CareerIQ.
Used by Resume Parser and Job Matcher for accurate skill extraction.
"""

SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "c", "javascript", "typescript",
        "go", "golang", "rust", "ruby", "php", "swift", "kotlin", "r",
        "dart", "scala", "shell", "bash", "powershell", "sql", "html", "css"
    ],
    "Frameworks & Libraries": [
        "react", "angular", "vue", "vue.js", "next.js", "node.js", "express",
        "django", "flask", "fastapi", "spring", "spring boot", "asp.net",
        ".net", "laravel", "tailwind", "tailwind css", "bootstrap", "jquery",
        "redux", "graphql", "rest api", "restful api"
    ],
    "Data Science & Machine Learning": [
        "machine learning", "deep learning", "natural language processing", "nlp",
        "computer vision", "artificial intelligence", "data analysis", "data science",
        "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas",
        "numpy", "scipy", "matplotlib", "seaborn", "tableau", "power bi",
        "opencv", "hugging face", "nltk", "spacy", "large language models", "llm",
        "generative ai", "genai", "prompt engineering"
    ],
    "Databases": [
        "mysql", "postgresql", "postgres", "sqlite", "mongodb", "redis",
        "oracle", "cassandra", "dynamodb", "firebase", "mariadb", "neo4j",
        "elasticsearch"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "google cloud", "gcp",
        "docker", "kubernetes", "k8s", "jenkins", "git", "github", "gitlab",
        "ci/cd", "ci cd", "linux", "unix", "terraform", "ansible", "nginx",
        "apache"
    ],
    "Core CS & Engineering": [
        "data structures", "algorithms", "dsa", "object oriented programming", "oop",
        "system design", "operating systems", "computer networks", "dbms",
        "software engineering", "microservices", "unit testing", "agile", "scrum"
    ],
    "Soft Skills & Communication": [
        "communication", "teamwork", "problem solving", "leadership",
        "critical thinking", "time management", "adaptability", "presentation",
        "collaboration", "analytical skills"
    ]
}

# Flattened set of all skills (lowercase) for fast O(1) membership and matching
ALL_SKILLS = set()
for category_skills in SKILL_CATEGORIES.values():
    for s in category_skills:
        ALL_SKILLS.add(s.lower())

def get_skill_category(skill_name: str) -> str:
    """Return the category of a skill, or 'Other' if not categorized."""
    skill_lower = skill_name.lower().strip()
    for cat, skills in SKILL_CATEGORIES.items():
        if skill_lower in skills:
            return cat
    return "Other / Domain-Specific"
