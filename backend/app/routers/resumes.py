"""
backend/app/routers/resumes.py
Route handlers for PDF resume upload and parsing.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.services.pdf_parser import parse_pdf_resume
from backend.app.services.skill_extractor import extract_skills_from_text, categorize_skills
from backend.app.models.schemas import ResumeParseResponse
from backend.app.core.config import settings

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/parse", response_model=ResumeParseResponse)
async def parse_resume(file: UploadFile = File(...)):
    """
    Accepts a PDF resume, validates it, extracts selectable text using pypdf,
    and returns basic contact info and extracted skills.
    """
    # Validate extension
    filename = file.filename or "resume.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a standard PDF document (.pdf)."
        )

    try:
        content = await file.read()
        parsed_data = parse_pdf_resume(
            file_bytes=content,
            filename=filename,
            max_size_mb=settings.MAX_FILE_SIZE_MB
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error processing PDF: {str(e)}")

    # Extract skills
    skills = extract_skills_from_text(parsed_data["text"])
    categorized = categorize_skills(skills)

    return {
        "filename": parsed_data["filename"],
        "page_count": parsed_data["page_count"],
        "word_count": parsed_data["word_count"],
        "text": parsed_data["text"],
        "text_preview": parsed_data["text_preview"],
        "contact_info": parsed_data["contact_info"],
        "extracted_skills": skills,
        "categorized_skills": categorized
    }
