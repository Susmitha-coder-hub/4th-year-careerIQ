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

# --- Milestone 2: Placement Readiness Schemas ---
class DimensionRating(BaseModel):
    category: str
    score: float
    status: str  # "Good", "Moderate", "Needs Improvement"
    details: str

class PlacementPredictionRequest(BaseModel):
    name: Optional[str] = "Student"
    branch: Optional[str] = "Computer Science and Engineering"
    cgpa: float = Field(..., ge=0.0, le=10.0, description="CGPA on 10-point scale")
    technical_skills: List[str] = Field(default_factory=list)
    aptitude_score: float = Field(..., ge=0.0, le=100.0, description="Aptitude test score 0-100")
    projects_count: int = Field(default=2, ge=0)
    internships_count: int = Field(default=0, ge=0)
    communication_rating: float = Field(default=3.5, ge=1.0, le=5.0, description="Rating 1-5")
    certifications_count: Optional[int] = 1

class PlacementPredictionResponse(BaseModel):
    readiness_score: float  # 0-100
    readiness_band: str    # "High Placement Readiness", "Moderate Placement Readiness", "Foundation Building"
    dimensions: List[DimensionRating]
    strengths: List[str]
    critical_improvements: List[str]
    actionable_prep_strategy: List[str]
    disclaimer: str

# --- Milestone 2: Recruiter Multi-Resume Ranking Schemas ---
class CandidateInput(BaseModel):
    candidate_id: Optional[str] = None
    name: str
    resume_text: str = Field(..., min_length=10)
    experience_years: Optional[float] = 0.0

class RecruiterRankingRequest(BaseModel):
    job_title: str = "Software Development Engineer"
    job_description: str = Field(..., min_length=20)
    candidates: List[CandidateInput]

class CandidateRankResult(BaseModel):
    rank: int
    candidate_id: str
    name: str
    match_score: float
    match_tier: str  # "Strong Match", "Good Match", "Moderate Match"
    matched_skills: List[str]
    missing_skills: List[str]
    total_detected_skills: int
    hiring_rationale: str

class RecruiterRankingResponse(BaseModel):
    job_title: str
    total_evaluated: int
    required_skills: List[str]
    ranked_candidates: List[CandidateRankResult]

# --- Milestone 2: Opportunity Intelligence Schemas ---
class OpportunityItem(BaseModel):
    id: str
    company: str
    role: str
    job_type: str  # "Full-Time", "Internship"
    min_cgpa: float
    eligible_branches: List[str]
    registration_deadline: str
    test_date: Optional[str] = None
    interview_date: Optional[str] = None
    location_or_mode: str
    required_skills: List[str]
    revision_topics: List[str]
    package_lpa: Optional[str] = None
    is_active: bool = True

class OpportunityEligibilityRequest(BaseModel):
    cgpa: float
    branch: str
    skills: List[str] = Field(default_factory=list)

class OpportunityEligibilityResult(BaseModel):
    opportunity: OpportunityItem
    is_eligible: bool
    cgpa_eligible: bool
    branch_eligible: bool
    skill_match_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]
    urgency_status: str  # "Urgent Deadline", "Assessment Soon", "Registration Open"
    recommendation: str

class OpportunityListResponse(BaseModel):
    total_opportunities: int
    eligible_count: int
    opportunities: List[OpportunityEligibilityResult]

class InterviewPrepGuideResponse(BaseModel):
    company: str
    role: str
    test_date: Optional[str]
    core_technical_topics: List[str]
    sample_coding_questions: List[str]
    hr_behavioral_tips: List[str]
    revision_schedule_48h: List[str]

# --- Milestone 2: AI Career Assistant Chatbot Schemas ---
class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    context_skills: Optional[List[str]] = Field(default_factory=list)
    context_cgpa: Optional[float] = None
    context_target_job: Optional[str] = None

class ChatMessageResponse(BaseModel):
    reply: str
    suggestions: List[str] = Field(default_factory=list)

