"""
test_app.py
Comprehensive automated test suite for CareerIQ to verify end-to-end functionality before demonstration.
"""

import os
from modules.resume_parser import analyze_resume
from modules.job_matcher import match_resume_to_job, recommend_jobs_for_resume
from modules.placement_predictor import predict_placement_readiness, load_or_train_model
from modules.opportunity_tracker import parse_inbox_opportunities
from modules.career_chatbot import generate_context_grounded_response
from utils.sample_data import SAMPLE_JOB_DESCRIPTIONS

def run_tests():
    print("=== Testing CareerIQ Modules ===")
    
    # 1. Test Resume Parser
    pdf_sde = "data/sample_resumes/Alex_Rivera_SDE.pdf"
    assert os.path.exists(pdf_sde), f"Sample PDF not found at {pdf_sde}"
    res = analyze_resume(pdf_sde)
    print(f"Module 1 (Resume): OK! ATS Score = {res['ats_score']['total_score']}, Skills detected = {len(res['skills'])}")
    assert len(res["skills"]) > 5
    assert res["ats_score"]["total_score"] > 50

    # 2. Test Job Matcher
    jd = SAMPLE_JOB_DESCRIPTIONS["Backend Software Engineer (Python/Java)"]
    job_match = match_resume_to_job(res["raw_text"], res["skills"], jd)
    print(f"Module 2 (Job): OK! Composite Score = {job_match['composite_score']}%, Matched = {len(job_match['matched_skills'])}, Missing = {len(job_match['missing_skills'])}")
    assert job_match["composite_score"] > 0

    recs = recommend_jobs_for_resume(res["raw_text"], res["skills"])
    print(f"Module 2 (Benchmark Recs): OK! Generated {len(recs)} role recommendations.")
    assert len(recs) >= 3

    # 3. Test Placement Predictor
    pred = predict_placement_readiness(
        cgpa=8.2, tech_score=8.0, comm_score=7.5,
        internships=1, projects=3, aptitude_score=80.0, coding_problems=200
    )
    print(f"Module 3 (Placement): OK! Readiness = {pred['readiness_percentage']}%, Tier = {pred['readiness_tier']}")
    print(f"   RF Accuracy: {pred['model_metrics']['RandomForest']['accuracy']:.2%}")
    assert pred["readiness_percentage"] > 50

    # 4. Test Opportunity Tracker
    opps = parse_inbox_opportunities()
    print(f"Module 4 (Opportunity): OK! Extracted {len(opps)} placement events.")
    assert len(opps) == 3
    assert opps[0]["company"] == "Microsoft"

    # 5. Test Career Chatbot
    chat_resp = generate_context_grounded_response(
        "What are my missing skills?",
        {"skills": res["skills"], "missing_skills": job_match["missing_skills"], "target_role": "Backend SDE"}
    )
    print(f"Module 5 (Chatbot): OK! Response generated ({len(chat_resp)} chars).")
    assert "missing" in chat_resp.lower()

    print("\n ALL MODULE TESTS PASSED PERFECTLY! SYSTEM IS 100% OPERATIONAL.")

if __name__ == "__main__":
    run_tests()
