"""
backend/app/models/schemas.py
Pydantic data models for request and response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Resume Parsing Schemas ---
class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class ResumeParseResponse(BaseModel):
    filename: str
    page_count: int
    word_count: int
    text: str
    text_preview: str
    contact_info: ContactInfo
    extracted_skills: List[str]
    categorized_skills: Dict[str, List[str]]

# --- Job Description Analysis Schemas ---
class JobAnalysisRequest(BaseModel):
    job_description: str = Field(..., min_length=20, description="Raw job description text")
    job_title: Optional[str] = Field("Target Role", description="Optional title of the role")

class JobAnalysisResponse(BaseModel):
    job_title: str
    word_count: int
    detected_skills: List[str]
    categorized_skills: Dict[str, List[str]]

# --- Matching Schemas ---
class MatchingRequest(BaseModel):
    resume_text: str = Field(..., min_length=10)
    job_text: str = Field(..., min_length=20)
    resume_filename: Optional[str] = "Uploaded_Resume.pdf"
    job_title: Optional[str] = "Target Role"
    resume_skills: Optional[List[str]] = None
    save_to_history: Optional[bool] = True

class MatchingResponse(BaseModel):
    analysis_id: Optional[int] = None
    similarity_score: float
    skill_coverage_percentage: float
    score_type: str
    matched_skills: List[str]
    missing_skills: List[str]
    additional_skills: List[str]
    resume_skills: List[str]
    job_skills: List[str]
    gap_analysis: Dict[str, Any]
    explanation: str

# --- History Schemas ---
class AnalysisHistoryItem(BaseModel):
    id: int
    timestamp: str
    resume_filename: str
    job_title: str
    similarity_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    resume_skills: List[str]
    job_skills: List[str]
    notes: Optional[str] = ""

class DashboardStatsResponse(BaseModel):
    total_analyses: int
    average_similarity_score: float
    recent_analyses: List[Dict[str, Any]]
