"""
backend/app/services/recruiter_ranker.py
Recruiter Multiple-Resume Comparison & Candidate Ranking Engine (Milestone 2 - Point 9)

Enables recruiters to evaluate multiple candidate resumes against a single target
Job Description (JD), producing:
1. Normalized Match Score (TF-IDF similarity + skill coverage overlap)
2. Categorical Match Tier ("Strong Match", "Good Match", "Moderate Match")
3. Matched vs Missing Skill Breakdown
4. Automated Comparative Hiring Rationale
5. Descending Leaderboard Ranking
"""

from typing import List
from backend.app.services.skill_extractor import extract_skills_from_text
from backend.app.services.matcher import compute_tfidf_similarity_score
from backend.app.models.schemas import (
    RecruiterRankingRequest,
    RecruiterRankingResponse,
    CandidateRankResult
)

def rank_candidates_against_jd(request: RecruiterRankingRequest) -> RecruiterRankingResponse:
    """
    Ranks multiple candidate resumes against a target job description.
    """
    jd_text = request.job_description
    required_skills = extract_skills_from_text(jd_text)
    required_set = set(s.lower() for s in required_skills)

    evaluated_candidates = []

    for idx, candidate in enumerate(request.candidates):
        cand_id = candidate.candidate_id or f"cand_{idx+1}"
        resume_text = candidate.resume_text
        cand_skills = extract_skills_from_text(resume_text)
        cand_set = set(s.lower() for s in cand_skills)

        # 1. Statistical TF-IDF Cosine Similarity (0-100)
        tfidf_score = compute_tfidf_similarity_score(resume_text, jd_text)

        # 2. Skill Coverage Percentage
        matched = [s for s in required_skills if s.lower() in cand_set]
        missing = [s for s in required_skills if s.lower() not in cand_set]

        if required_skills:
            skill_coverage = (len(matched) / len(required_skills)) * 100.0
        else:
            skill_coverage = tfidf_score

        # 3. Composite Final Match Score (40% TF-IDF Text Alignment + 60% Explicit Skill Coverage)
        composite_score = round((0.40 * tfidf_score) + (0.60 * skill_coverage), 1)

        # 4. Determine Match Tier
        if composite_score >= 75.0 or skill_coverage >= 90.0:
            tier = "Strong Match"
        elif composite_score >= 50.0 or skill_coverage >= 50.0:
            tier = "Good Match"
        else:
            tier = "Moderate Match"

        # 5. Formulate Hiring Rationale
        if tier == "Strong Match":
            rationale = (
                f"Exceptional alignment ({composite_score}%). Possesses key required competencies "
                f"({', '.join(matched[:3]) if matched else 'core stack'}). Recommended for technical screening."
            )
        elif tier == "Good Match":
            rationale = (
                f"Solid profile alignment ({composite_score}%). Matches {len(matched)} required competencies, "
                f"though lacks direct evidence for {', '.join(missing[:2]) if missing else 'secondary requirements'}."
            )
        else:
            rationale = (
                f"Moderate alignment ({composite_score}%). Missing key core competencies "
                f"({', '.join(missing[:3]) if missing else 'required tools'}). Profile may require upskilling."
            )

        evaluated_candidates.append({
            "candidate_id": cand_id,
            "name": candidate.name,
            "match_score": composite_score,
            "match_tier": tier,
            "matched_skills": matched,
            "missing_skills": missing,
            "total_detected_skills": len(cand_skills),
            "hiring_rationale": rationale
        })

    # Sort descending by composite match score
    evaluated_candidates.sort(key=lambda c: c["match_score"], reverse=True)

    ranked_results: List[CandidateRankResult] = []
    for rank_idx, cand in enumerate(evaluated_candidates, start=1):
        ranked_results.append(CandidateRankResult(
            rank=rank_idx,
            candidate_id=cand["candidate_id"],
            name=cand["name"],
            match_score=cand["match_score"],
            match_tier=cand["match_tier"],
            matched_skills=cand["matched_skills"],
            missing_skills=cand["missing_skills"],
            total_detected_skills=cand["total_detected_skills"],
            hiring_rationale=cand["hiring_rationale"]
        ))

    return RecruiterRankingResponse(
        job_title=request.job_title,
        total_evaluated=len(ranked_results),
        required_skills=required_skills,
        ranked_candidates=ranked_results
    )
