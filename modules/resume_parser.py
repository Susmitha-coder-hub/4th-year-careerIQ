"""
modules/resume_parser.py
Module 1: Resume Intelligence
- PDF text extraction using PyMuPDF (fitz)
- Section identification (Education, Experience, Projects, Skills, Certifications)
- Skill extraction using curated taxonomy and regex word boundary matching
- Transparent ATS Scoring algorithm with break-down
- Fact-grounded resume improvement suggestions
"""

import re
import io
from typing import Dict, List, Any, Tuple
try:
    import pymupdf as fitz
except ImportError:
    import fitz
from utils.skill_database import ALL_SKILLS, SKILL_CATEGORIES, get_skill_category


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract raw text from a PDF file buffer or path using PyMuPDF.
    Handles bytes, io.BytesIO, or filepath strings.
    """
    try:
        if isinstance(pdf_file, (bytes, bytearray)):
            doc = fitz.open(stream=pdf_file, filetype="pdf")
        elif isinstance(pdf_file, io.BytesIO):
            doc = fitz.open(stream=pdf_file.getvalue(), filetype="pdf")
        elif hasattr(pdf_file, "read"):
            content = pdf_file.read()
            doc = fitz.open(stream=content, filetype="pdf")
        else:
            doc = fitz.open(pdf_file)

        full_text = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if text:
                full_text.append(text)
        doc.close()

        extracted = "\n".join(full_text).strip()
        if not extracted:
            raise ValueError("Extracted text is empty. The PDF may be scanned (image-only) or empty.")
        return extracted
    except Exception as e:
        raise RuntimeError(f"Error parsing PDF: {str(e)}")


def extract_contact_info(text: str) -> Dict[str, Any]:
    """Extract contact information: email, phone, links (GitHub, LinkedIn)."""
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b'
    linkedin_pattern = r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+'
    github_pattern = r'(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+'

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
    github = re.findall(github_pattern, text, re.IGNORECASE)

    return {
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None,
    }


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract skills from text by checking against the ontology with
    appropriate word boundaries to avoid false substrings.
    """
    text_lower = " " + text.lower() + " "
    # Replace common separators with spaces for boundary tokenization
    normalized_text = re.sub(r'[/,;:()•\n\r|]', ' ', text_lower)

    matched_skills = set()
    for skill in ALL_SKILLS:
        # For single or 2-letter skills like C, R, GO, require strict boundary
        if len(skill) <= 2:
            pattern = rf'(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])'
        else:
            pattern = rf'(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])'
        
        if re.search(pattern, normalized_text):
            matched_skills.add(skill)

    # Return sorted title-cased or canonical list
    return sorted(list(matched_skills))


def detect_sections(text: str) -> Dict[str, bool]:
    """Detect key sections in the resume text."""
    sections = {
        "education": bool(re.search(r'\b(education|academic|qualifications|degree|b\.?tech|b\.?e|m\.?tech)\b', text, re.IGNORECASE)),
        "experience": bool(re.search(r'\b(experience|work experience|employment|internship|internships|work history)\b', text, re.IGNORECASE)),
        "projects": bool(re.search(r'\b(projects|academic projects|personal projects|key projects)\b', text, re.IGNORECASE)),
        "skills": bool(re.search(r'\b(skills|technical skills|technologies|proficiencies|competencies)\b', text, re.IGNORECASE)),
        "certifications": bool(re.search(r'\b(certifications|certificate|certified|licenses|courses)\b', text, re.IGNORECASE)),
    }
    return sections


def calculate_ats_score(
    text: str,
    contact_info: Dict[str, Any],
    skills: List[str],
    sections: Dict[str, bool]
) -> Dict[str, Any]:
    """
    Transparent ATS Scoring Breakdown (Total: 100 points):
    1. Contact completeness (Max 15 pts): Email (5), Phone (5), LinkedIn/GitHub (5)
    2. Section structural coverage (Max 25 pts): 5 pts each for Skills, Education, Projects, Experience, Certifications
    3. Technical Skill Depth & Diversity (Max 35 pts):
       - Skill count (up to 20 pts)
       - Category diversity (at least 3 skill categories: 15 pts)
    4. Action Verbs & Impact Metrics (Max 15 pts): presence of metrics (% / numbers) and action verbs
    5. Length & Readability (Max 10 pts): word count between 200 and 1200 words
    """
    breakdown = {}
    total_score = 0

    # 1. Contact Info (15 pts)
    contact_pts = 0
    if contact_info.get("email"): contact_pts += 5
    if contact_info.get("phone"): contact_pts += 5
    if contact_info.get("linkedin") or contact_info.get("github"): contact_pts += 5
    breakdown["Contact Information"] = {"score": contact_pts, "max": 15}
    total_score += contact_pts

    # 2. Section Coverage (25 pts)
    section_pts = sum(5 for s, present in sections.items() if present)
    breakdown["Standard Section Headings"] = {"score": section_pts, "max": 25}
    total_score += section_pts

    # 3. Skills (35 pts)
    skill_count = len(skills)
    skill_count_pts = min(20, skill_count * 2)  # 10 skills = 20 pts
    
    # Category diversity
    categories_found = set(get_skill_category(s) for s in skills)
    cat_diversity_pts = min(15, len(categories_found) * 4)
    skill_pts = skill_count_pts + cat_diversity_pts
    breakdown["Skills & Diversity"] = {"score": skill_pts, "max": 35}
    total_score += skill_pts

    # 4. Action Verbs & Quantifiable Results (15 pts)
    action_verbs = [
        "built", "developed", "designed", "implemented", "created", "led",
        "optimized", "improved", "increased", "reduced", "automated", "achieved",
        "engineered", "spearheaded", "deployed", "scaled"
    ]
    verb_count = sum(1 for v in action_verbs if re.search(rf'\b{v}\b', text, re.IGNORECASE))
    has_metrics = bool(re.search(r'\b\d+%\b|\b\d+\s*(?:users|clients|x|ms|times|stars)\b', text, re.IGNORECASE))
    
    impact_pts = min(10, verb_count * 2) + (5 if has_metrics else 0)
    breakdown["Impact & Action Verbs"] = {"score": impact_pts, "max": 15}
    total_score += impact_pts

    # 5. Readability & Length (10 pts)
    word_count = len(text.split())
    if 250 <= word_count <= 1100:
        length_pts = 10
    elif 150 <= word_count < 250 or 1100 < word_count <= 1500:
        length_pts = 6
    else:
        length_pts = 3
    breakdown["Length & Format"] = {"score": length_pts, "max": 10}
    total_score += length_pts

    return {
        "total_score": round(total_score, 1),
        "breakdown": breakdown,
        "word_count": word_count,
        "skill_count": skill_count,
        "categories_found": list(categories_found)
    }


def generate_resume_improvements(
    text: str,
    contact_info: Dict[str, Any],
    skills: List[str],
    sections: Dict[str, bool],
    ats_score_data: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    Generate actionable, grounded feedback without fabricating candidate experience.
    """
    suggestions = []

    # Check Contact Info
    if not contact_info.get("linkedin"):
        suggestions.append({
            "category": "Contact Details",
            "type": "Recommendation",
            "message": "Add a customized LinkedIn profile URL in your header to increase recruiter discovery."
        })
    if not contact_info.get("github"):
        suggestions.append({
            "category": "Portfolio",
            "type": "Recommendation",
            "message": "Add a GitHub / Portfolio link to provide verifiable evidence of your software projects."
        })

    # Check Missing Sections
    for sec_name, present in sections.items():
        if not present:
            suggestions.append({
                "category": "Structure",
                "type": "Missing Section",
                "message": f"Section '{sec_name.capitalize()}' is missing or not recognized by ATS parser. Add a clear standard heading."
            })

    # Check Impact / Metrics
    has_metrics = bool(re.search(r'\b\d+%\b|\b\d+\s*(?:users|clients|x|ms|times)\b', text, re.IGNORECASE))
    if not has_metrics:
        suggestions.append({
            "category": "Content & Impact",
            "type": "Actionable Tip",
            "message": "Quantify your achievements in project bullet points (e.g., 'Reduced response latency by 35%', 'Serving 500+ active users')."
        })

    # Check Skills Breadth
    if len(skills) < 6:
        suggestions.append({
            "category": "Skills Breadth",
            "type": "Skill Gap",
            "message": "Only a few technical skills were detected. Explicitly list tools, libraries, databases, and frameworks you have used."
        })

    # Check Word Count
    word_count = ats_score_data.get("word_count", 0)
    if word_count < 250:
        suggestions.append({
            "category": "Resume Length",
            "type": "Format Warning",
            "message": f"Resume is quite brief ({word_count} words). Elaborate on project architecture, key technical challenges, and responsibilities."
        })
    elif word_count > 1200:
        suggestions.append({
            "category": "Resume Length",
            "type": "Format Warning",
            "message": f"Resume is lengthy ({word_count} words). Aim for a concise 1-page to 2-page format tailored for early-career roles."
        })

    return suggestions


def analyze_resume(pdf_file) -> Dict[str, Any]:
    """
    Complete Resume Analysis Pipeline:
    1. Extract text from PDF
    2. Extract contact info
    3. Extract skills
    4. Detect sections
    5. Calculate ATS score
    6. Generate improvement suggestions
    """
    raw_text = extract_text_from_pdf(pdf_file)
    contact_info = extract_contact_info(raw_text)
    skills = extract_skills_from_text(raw_text)
    sections = detect_sections(raw_text)
    ats_score = calculate_ats_score(raw_text, contact_info, skills, sections)
    suggestions = generate_resume_improvements(raw_text, contact_info, skills, sections, ats_score)

    # Categorize detected skills
    categorized_skills = {}
    for skill in skills:
        cat = get_skill_category(skill)
        categorized_skills.setdefault(cat, []).append(skill)

    return {
        "raw_text": raw_text,
        "contact_info": contact_info,
        "skills": skills,
        "categorized_skills": categorized_skills,
        "sections": sections,
        "ats_score": ats_score,
        "suggestions": suggestions,
    }
