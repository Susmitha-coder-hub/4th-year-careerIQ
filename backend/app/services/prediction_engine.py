"""
backend/app/services/prediction_engine.py
Placement-Related Readiness Prediction Engine (Milestone 2 - Points 4 & 10)

Evaluates student profiles across 6 critical placement dimensions:
1. Academic Standing (CGPA)
2. Technical Skills Breadth
3. Aptitude & Problem Solving
4. Project Portfolio
5. Communication Ability
6. Practical Experience (Internships & Certifications)

Outputs a calibrated readiness score (0-100), categorical dimensional ratings,
key strengths, critical improvements, and actionable 30-day prep strategy.
"""

from typing import List, Dict, Any
from backend.app.models.schemas import (
    PlacementPredictionRequest,
    PlacementPredictionResponse,
    DimensionRating
)

def evaluate_placement_readiness(profile: PlacementPredictionRequest) -> PlacementPredictionResponse:
    """
    Evaluates a candidate profile and computes comprehensive placement readiness estimation.
    """
    dimensions: List[DimensionRating] = []
    strengths: List[str] = []
    critical_improvements: List[str] = []
    action_plan: List[str] = []

    # 1. Academic Performance (CGPA) - Weight 20%
    cgpa = profile.cgpa
    if cgpa >= 8.5:
        cgpa_score = 100.0
        cgpa_status = "Good"
        cgpa_details = f"Strong academic record ({cgpa:.2f}/10). Clears top-tier cutoff (usually ≥8.0)."
        strengths.append(f"High CGPA ({cgpa:.2f}) satisfies virtually all campus placement eligibility criteria.")
    elif cgpa >= 7.0:
        cgpa_score = 75.0
        cgpa_status = "Moderate"
        cgpa_details = f"Moderate CGPA ({cgpa:.2f}/10). Clears standard eligibility (≥6.5–7.0)."
    else:
        cgpa_score = 45.0
        cgpa_status = "Needs Improvement"
        cgpa_details = f"CGPA ({cgpa:.2f}/10) may fall below threshold for some tier-1 companies."
        critical_improvements.append(f"Prioritize academic exams to elevate CGPA above 7.0 to unlock broader company shortlists.")

    dimensions.append(DimensionRating(
        category="Academic Standing (CGPA)",
        score=cgpa_score,
        status=cgpa_status,
        details=cgpa_details
    ))

    # 2. Technical Skills Breadth - Weight 25%
    tech_count = len(profile.technical_skills)
    if tech_count >= 7:
        tech_score = 95.0
        tech_status = "Good"
        tech_details = f"Broad technical toolkit ({tech_count} identified skills)."
        strengths.append(f"Demonstrated multi-disciplinary tech stack ({', '.join(profile.technical_skills[:4])}...).")
    elif tech_count >= 4:
        tech_score = 75.0
        tech_status = "Moderate"
        tech_details = f"Moderate technical breadth ({tech_count} skills). Add 2-3 modern frameworks or tools."
    else:
        tech_score = 40.0
        tech_status = "Needs Improvement"
        tech_details = f"Narrow skill profile ({tech_count} skills detected). Needs depth in core languages and tools."
        critical_improvements.append("Expand core technical skills: Learn at least one backend framework (FastAPI/Django) and Git/Docker.")

    dimensions.append(DimensionRating(
        category="Technical Skills",
        score=tech_score,
        status=tech_status,
        details=tech_details
    ))

    # 3. Aptitude & Reasoning - Weight 20%
    apt = profile.aptitude_score
    if apt >= 75.0:
        apt_score = 95.0
        apt_status = "Good"
        apt_details = f"High aptitude score ({apt:.1f}%). Solid speed and problem-solving accuracy."
        strengths.append(f"Strong analytical aptitude ({apt:.1f}%) enables clearing online round 1 filters.")
    elif apt >= 55.0:
        apt_score = 70.0
        apt_status = "Moderate"
        apt_details = f"Average aptitude score ({apt:.1f}%). Revise quantitative speed techniques."
        action_plan.append("Practice 20 timed quantitative aptitude questions daily (Time & Work, Permutations, Probability).")
    else:
        apt_score = 35.0
        apt_status = "Needs Improvement"
        apt_details = f"Low aptitude score ({apt:.1f}%). Aptitude tests eliminate 60%+ applicants in Round 1."
        critical_improvements.append(f"Urgent: Boost aptitude practice ({apt:.1f}% currently) to clear initial assessment cutoffs.")

    dimensions.append(DimensionRating(
        category="Aptitude & Reasoning",
        score=apt_score,
        status=apt_status,
        details=apt_details
    ))

    # 4. Project Portfolio - Weight 15%
    proj = profile.projects_count
    if proj >= 3:
        proj_score = 95.0
        proj_status = "Good"
        proj_details = f"Solid project portfolio ({proj} practical projects)."
        strengths.append(f"Strong practical experience with {proj} documented software projects.")
    elif proj >= 2:
        proj_score = 75.0
        proj_status = "Moderate"
        proj_details = f"Good baseline ({proj} projects). Consider adding a full-stack or deployed cloud project."
    else:
        proj_score = 40.0
        proj_status = "Needs Improvement"
        proj_details = f"Insufficient project evidence ({proj} projects). Real-world applications are critical."
        critical_improvements.append("Build and deploy at least 2 end-to-end projects with public GitHub repositories.")

    dimensions.append(DimensionRating(
        category="Projects Portfolio",
        score=proj_score,
        status=proj_status,
        details=proj_details
    ))

    # 5. Communication & Behavioral - Weight 10%
    comm = profile.communication_rating
    if comm >= 4.0:
        comm_score = 90.0
        comm_status = "Good"
        comm_details = f"Strong verbal and interview articulation ({comm:.1f}/5.0)."
        strengths.append("High communication rating gives a competitive edge in HR and technical panel discussions.")
    elif comm >= 3.0:
        comm_score = 70.0
        comm_status = "Moderate"
        comm_details = f"Acceptable communication ({comm:.1f}/5.0). Practice STAR method for behavioral rounds."
    else:
        comm_score = 40.0
        comm_status = "Needs Improvement"
        comm_details = f"Communication needs polish ({comm:.1f}/5.0). Practice mock peer interviews."
        critical_improvements.append("Participate in mock technical interviews focusing on clear architectural explanations.")

    dimensions.append(DimensionRating(
        category="Communication",
        score=comm_score,
        status=comm_status,
        details=comm_details
    ))

    # 6. Practical Experience (Internship & Certifications) - Weight 10%
    intern = profile.internships_count
    certs = profile.certifications_count or 0
    if intern >= 1:
        exp_score = 95.0
        exp_status = "Good"
        exp_details = f"Verified industry exposure with {intern} internship(s)."
        strengths.append("Real-world internship experience directly demonstrates workplace readiness.")
    elif certs >= 1:
        exp_score = 70.0
        exp_status = "Moderate"
        exp_details = f"No corporate internship yet, but verified certifications ({certs}) show proactive learning."
    else:
        exp_score = 45.0
        exp_status = "Needs Improvement"
        exp_details = "No internships or certifications recorded yet."
        action_plan.append("Pursue remote open-source contributions or summer internships to bridge industry exposure.")

    dimensions.append(DimensionRating(
        category="Internships & Certifications",
        score=exp_score,
        status=exp_status,
        details=exp_details
    ))

    # Compute Weighted Overall Readiness Score
    # Weights: CGPA 20%, Tech 25%, Aptitude 20%, Projects 15%, Comm 10%, Exp 10%
    readiness_score = round(
        (cgpa_score * 0.20) +
        (tech_score * 0.25) +
        (apt_score * 0.20) +
        (proj_score * 0.15) +
        (comm_score * 0.10) +
        (exp_score * 0.10),
        1
    )

    if readiness_score >= 80.0:
        readiness_band = "High Placement Readiness"
        action_plan.insert(0, "Refine core system design and live LeetCode/DSA problem solving under timed conditions.")
        action_plan.insert(1, "Conduct 2 mock technical interviews with peers or mentors.")
    elif readiness_score >= 60.0:
        readiness_band = "Moderate Placement Readiness"
        action_plan.insert(0, "Dedicate 2 hours daily to Data Structures & Algorithms (Arrays, HashMaps, Trees, Graphs).")
        action_plan.insert(1, "Deep-dive into 1 marquee project so you can defend every architectural decision.")
    else:
        readiness_band = "Foundation Building Phase"
        action_plan.insert(0, "Focus heavily on foundational fundamentals: OOP, DBMS, SQL, and core language mastery.")
        action_plan.insert(1, "Complete 1 full-stack CRUD application and document it clearly.")

    if not critical_improvements:
        critical_improvements.append("Maintain consistent problem solving practice and stay updated on system architecture.")

    return PlacementPredictionResponse(
        readiness_score=readiness_score,
        readiness_band=readiness_band,
        dimensions=dimensions,
        strengths=strengths,
        critical_improvements=critical_improvements,
        actionable_prep_strategy=action_plan[:4],
        disclaimer="Placement readiness estimation is an advisory diagnostic based on academic & profile metrics. It provides targeted guidance and does not guarantee specific corporate placement offers."
    )
