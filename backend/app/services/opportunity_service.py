"""
backend/app/services/opportunity_service.py
Opportunity Intelligence & Placement Alert Engine (Milestone 2 - Points 11-14)

Provides:
1. Automated Opportunity Registry (Campus Drives, Off-campus Hiring, Hackathons)
2. Student Eligibility & Skill Alignment Engine
3. Proactive Urgent Deadline & Assessment Alerts
4. 48-Hour Interview & Coding Assessment Prep Pack (Detect -> Alert -> Explain -> Prepare)
"""

from typing import List, Dict, Any, Optional
from backend.app.models.schemas import (
    OpportunityItem,
    OpportunityEligibilityRequest,
    OpportunityEligibilityResult,
    OpportunityListResponse,
    InterviewPrepGuideResponse
)

# Active Placement Opportunities Catalogue (Simulated placement cell & company drive notifications)
CAMPUS_OPPORTUNITIES: List[Dict[str, Any]] = [
    {
        "id": "opp_01",
        "company": "Amazon",
        "role": "Software Development Engineer - Intern / Full-Time",
        "job_type": "Full-Time",
        "min_cgpa": 7.5,
        "eligible_branches": ["Computer Science and Engineering", "Information Technology", "Electronics and Communication"],
        "registration_deadline": "2026-11-25",
        "test_date": "2026-11-28",
        "interview_date": "2026-12-05",
        "location_or_mode": "Hyderabad / Bangalore (Hybrid)",
        "required_skills": ["Python", "Java", "Data Structures", "Algorithms", "SQL", "System Design"],
        "revision_topics": ["Binary Trees", "Dynamic Programming", "SQL Joins", "OS Threading", "OOP Principles"],
        "package_lpa": "18 - 24 LPA",
        "is_active": True
    },
    {
        "id": "opp_02",
        "company": "Microsoft",
        "role": "Software Engineer (Campus Hiring)",
        "job_type": "Full-Time",
        "min_cgpa": 8.0,
        "eligible_branches": ["Computer Science and Engineering", "Information Technology"],
        "registration_deadline": "2026-11-22",
        "test_date": "2026-11-24",
        "interview_date": "2026-12-01",
        "location_or_mode": "Hyderabad (On-site)",
        "required_skills": ["C++", "Python", "Data Structures", "Algorithms", "Git", "Cloud Fundamentals"],
        "revision_topics": ["Graph Traversals", "Sliding Window", "Distributed Basics", "REST APIs"],
        "package_lpa": "22 - 28 LPA",
        "is_active": True
    },
    {
        "id": "opp_03",
        "company": "TCS Digital",
        "role": "Systems Engineer & Full-Stack Developer",
        "job_type": "Full-Time",
        "min_cgpa": 6.8,
        "eligible_branches": ["Computer Science and Engineering", "Information Technology", "Electrical", "Mechanical"],
        "registration_deadline": "2026-11-30",
        "test_date": "2026-12-03",
        "interview_date": "2026-12-10",
        "location_or_mode": "Pan India",
        "required_skills": ["Java", "Python", "SQL", "HTML", "CSS", "JavaScript"],
        "revision_topics": ["Quantitative Aptitude", "Advanced Coding", "DBMS Normalization", "OOP Basics"],
        "package_lpa": "7.5 - 9.0 LPA",
        "is_active": True
    },
    {
        "id": "opp_04",
        "company": "Accenture",
        "role": "Advanced Associate Software Engineer",
        "job_type": "Full-Time",
        "min_cgpa": 6.5,
        "eligible_branches": ["All Engineering Branches"],
        "registration_deadline": "2026-12-02",
        "test_date": "2026-12-06",
        "interview_date": "2026-12-14",
        "location_or_mode": "Bangalore / Chennai / Pune",
        "required_skills": ["Python", "Java", "SQL", "Cloud", "Agile"],
        "revision_topics": ["Logical Reasoning", "Pseudocode Debugging", "Cloud Fundamentals", "Communication"],
        "package_lpa": "6.5 - 8.5 LPA",
        "is_active": True
    },
    {
        "id": "opp_05",
        "company": "Zomato",
        "role": "Backend Engineering Intern",
        "job_type": "Internship",
        "min_cgpa": 7.0,
        "eligible_branches": ["Computer Science and Engineering", "Information Technology"],
        "registration_deadline": "2026-11-20",
        "test_date": "2026-11-23",
        "interview_date": "2026-11-27",
        "location_or_mode": "Gurugram (On-site)",
        "required_skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "Redis"],
        "revision_topics": ["RESTful API Architecture", "Database Indexing", "Caching Strategies", "Concurrency"],
        "package_lpa": "60,000 / month Stipend",
        "is_active": True
    }
]

def get_active_opportunities(student_profile: Optional[OpportunityEligibilityRequest] = None) -> OpportunityListResponse:
    """
    Returns list of opportunities evaluated against student profile eligibility and urgency.
    """
    evaluated_results: List[OpportunityEligibilityResult] = []
    eligible_count = 0

    student_cgpa = student_profile.cgpa if student_profile else 7.5
    student_branch = student_profile.branch if student_profile else "Computer Science and Engineering"
    student_skills_set = set(s.lower() for s in (student_profile.skills if student_profile else []))

    for opp_data in CAMPUS_OPPORTUNITIES:
        opp = OpportunityItem(**opp_data)

        # Check CGPA eligibility
        cgpa_ok = student_cgpa >= opp.min_cgpa

        # Check branch eligibility
        branch_ok = (
            "All Engineering Branches" in opp.eligible_branches or
            any(student_branch.lower() in b.lower() or b.lower() in student_branch.lower() for b in opp.eligible_branches)
        )

        is_eligible = cgpa_ok and branch_ok
        if is_eligible:
            eligible_count += 1

        # Calculate skill match
        opp_skills = opp.required_skills
        matched = [s for s in opp_skills if s.lower() in student_skills_set]
        missing = [s for s in opp_skills if s.lower() not in student_skills_set]

        if opp_skills:
            skill_match_pct = round((len(matched) / len(opp_skills)) * 100.0, 1)
        else:
            skill_match_pct = 50.0

        # Determine Urgency Status
        if "2026-11-20" in opp.registration_deadline or "2026-11-22" in opp.registration_deadline:
            urgency = "Urgent Deadline (Closing Soon)"
        elif opp.test_date and ("2026-11-23" in opp.test_date or "2026-11-24" in opp.test_date):
            urgency = "Assessment Scheduled"
        else:
            urgency = "Registration Open"

        # Formulate Recommendation Message
        if is_eligible and skill_match_pct >= 60.0:
            rec = f"Strong fit ({skill_match_pct}% skill match). Your CGPA ({student_cgpa:.1f}) qualifies for {opp.company}. Apply before deadline."
        elif is_eligible:
            rec = f"Eligible by CGPA ({student_cgpa:.1f} >= {opp.min_cgpa}), but brush up on {', '.join(missing[:2])} for the technical round."
        else:
            rec = f"Ineligible: Requirement requires min CGPA of {opp.min_cgpa} (Your CGPA: {student_cgpa:.1f})."

        evaluated_results.append(OpportunityEligibilityResult(
            opportunity=opp,
            is_eligible=is_eligible,
            cgpa_eligible=cgpa_ok,
            branch_eligible=branch_ok,
            skill_match_percentage=skill_match_pct,
            matched_skills=matched,
            missing_skills=missing,
            urgency_status=urgency,
            recommendation=rec
        ))

    return OpportunityListResponse(
        total_opportunities=len(evaluated_results),
        eligible_count=eligible_count,
        opportunities=evaluated_results
    )

def generate_interview_prep_guide(opportunity_id: str) -> InterviewPrepGuideResponse:
    """
    Generates a 48-Hour Interview & Assessment Preparation Pack for an opportunity.
    Fulfills the 'Detect -> Alert -> Explain -> Prepare' workflow (Point 14).
    """
    matched_opp = next((o for o in CAMPUS_OPPORTUNITIES if o["id"] == opportunity_id), None)
    if not matched_opp:
        matched_opp = CAMPUS_OPPORTUNITIES[0]

    company = matched_opp["company"]
    role = matched_opp["role"]

    return InterviewPrepGuideResponse(
        company=company,
        role=role,
        test_date=matched_opp.get("test_date"),
        core_technical_topics=[
            f"Core Language Fundamentals ({', '.join(matched_opp['required_skills'][:2])})",
            "Data Structures: Two-pointer technique, Sliding Window, Tree Traversals",
            "Database Systems: SQL Aggregations, Indexing, ACID Properties",
            "Operating Systems: Concurrency, Deadlocks, Virtual Memory"
        ],
        sample_coding_questions=[
            "Find the lowest common ancestor in a Binary Search Tree.",
            "Implement LRU Cache using HashMap and Doubly Linked List.",
            "Find the contiguous subarray with maximum sum (Kadane's Algorithm).",
            "Write a SQL query to find the 2nd highest salary in each department."
        ],
        hr_behavioral_tips=[
            f"Research {company}'s recent engineering blogs and core leadership principles.",
            "Prepare 2 stories using the STAR method (Situation, Task, Action, Result).",
            "Have an honest explanation ready for any gap or technical challenge faced in projects."
        ],
        revision_schedule_48h=[
            "Day 1 Morning (09:00 - 12:00): Revise Data Structures & solve 4 Medium LeetCode problems.",
            "Day 1 Afternoon (14:00 - 17:00): Core CS Theory (DBMS SQL queries + OS Process Synchronization).",
            "Day 1 Evening (18:00 - 20:00): Project walk-through: Be ready to explain your system architecture.",
            "Day 2 (Morning): Mock timed assessment & 30-minute self-introduction practice."
        ]
    )
