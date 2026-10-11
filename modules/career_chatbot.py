"""
modules/career_chatbot.py
Module 5: Conversational AI
- CareerIQ AI Career Assistant
- Grounded on actual session context (Candidate's resume analysis, ATS score, missing skills, target role)
- Answers queries on:
  1. Resume optimization & ATS improvements
  2. Technical interview questions tailored to candidate's skills
  3. Actionable preparation roadmap for missing job skills
  4. Placement readiness strategy & GPA compensation
  5. Mock behavioral (STAR) questions
"""

import re
from typing import Dict, List, Any


def generate_context_grounded_response(
    query: str,
    context: Dict[str, Any]
) -> str:
    """
    Generate accurate, context-grounded response using candidate's actual data.
    If no resume is uploaded yet, provides structured general career guidance.
    """
    q_lower = query.lower()
    
    resume_skills = context.get("skills", [])
    ats_score = context.get("ats_score", {}).get("total_score", "N/A")
    missing_skills = context.get("missing_skills", [])
    target_role = context.get("target_role", "Software / Tech Roles")
    readiness = context.get("readiness_percentage", "N/A")

    # 1. Questions about Resume Score or ATS
    if any(k in q_lower for k in ["score", "ats", "resume", "cv", "rate"]):
        if not resume_skills:
            return (
                "**CareerIQ Advisor:** You haven't uploaded a resume yet!\n\n"
                "Once you upload your resume in the **Resume Intelligence** tab, I will analyze your ATS compatibility, "
                "section breakdown, and give you concrete suggestions without inventing experience."
            )
        suggestions = context.get("suggestions", [])
        top_suggs = "\n".join([f"- **{s['category']}**: {s['message']}" for s in suggestions[:3]])
        return (
            f"**Resume Analysis Insights:**\n\n"
            f"- **Current ATS Score:** `{ats_score}/100`\n"
            f"- **Detected Skills ({len(resume_skills)}):** {', '.join(resume_skills[:8])}...\n\n"
            f"**Key Priority Improvements:**\n{top_suggs}\n\n"
            f"💡 *Pro-tip:* Ensure each bullet in your projects starts with a strong action verb (e.g., 'Engineered', 'Optimized') and includes measurable impact (e.g., '% speedup' or 'user count')."
        )

    # 2. Questions about Missing Skills or Skill Gaps
    elif any(k in q_lower for k in ["gap", "missing", "learn", "study", "what should i prepare", "upskill"]):
        if missing_skills:
            skills_str = ", ".join([f"`{s}`" for s in missing_skills])
            return (
                f"**Skill Gap Analysis for {target_role}:**\n\n"
                f"Based on your target job match, here are the critical skills you are currently missing:\n"
                f"{skills_str}\n\n"
                f"**Recommended 4-Week Action Plan:**\n"
                f"1. **Week 1-2:** Build a small standalone project using `{missing_skills[0] if missing_skills else 'the core missing tool'}`.\n"
                f"2. **Week 3:** Integrate it into an existing GitHub repository and document it in your README.\n"
                f"3. **Week 4:** Add the project bullets to your resume and practice answering design tradeoffs."
            )
        else:
            return (
                "**CareerIQ Advisor:** To get a personalized skill gap roadmap, enter or select a job description in the "
                "**Job Intelligence** tab. I will compare your detected skills against the exact job requirements!"
            )

    # 3. Questions about Interview Prep or Mock Questions
    elif any(k in q_lower for k in ["interview", "questions", "technical round", "mock", "prepare"]):
        skills_sample = resume_skills[:4] if resume_skills else ["Python", "DSA", "DBMS", "Operating Systems"]
        return (
            f"**Custom Interview Questions based on your Profile:**\n\n"
            f"Here are targeted technical questions tailored to your background ({', '.join(skills_sample)}):\n\n"
            f"1. **Data Structures:** *How would you choose between an Array, Hash Map, and Binary Search Tree when designing a low-latency cache?*\n"
            f"2. **Core Domain ({skills_sample[0]}):** *Can you explain internal memory management and concurrency handling in your primary language?*\n"
            f"3. **System Design & DBMS:** *Explain the differences between SQL and NoSQL indexing, and when you would denormalize data for read scalability.*\n"
            f"4. **Behavioral (STAR Method):** *Describe a challenging bug you encountered in one of your projects. How did you diagnose and resolve it under deadline pressure?*\n\n"
            f"Would you like to practice answering one of these questions?"
        )

    # 4. Questions about Placement Readiness / Eligibility / CGPA
    elif any(k in q_lower for k in ["placement", "ready", "cgpa", "criteria", "eligibility"]):
        return (
            f"**Placement Readiness Assessment:**\n\n"
            f"- **Estimated Readiness:** `{readiness}%`\n"
            f"- **College Placement Baseline:** Most Tier-1 tech recruiters require:\n"
            f"  * Minimum CGPA cutoff: `7.0 - 7.5`\n"
            f"  * At least 150+ solved Data Structures & Algorithms problems\n"
            f"  * At least 2 full-stack or ML projects hosted with live links\n"
            f"  * Clear, confident verbal articulation of architectural choices\n\n"
            f"Check the **Placement Intelligence** tab to adjust your CGPA, Aptitude, and Internship numbers to simulate your exact placement probability!"
        )

    # 5. Default Fallback / General Guidance
    else:
        return (
            f"**CareerIQ Advisor:**\n\n"
            f"I am here to guide your placement and career preparation! You can ask me:\n"
            f"- *'How can I improve my ATS resume score?'*\n"
            f"- *'What are my missing skills for the backend role?'*\n"
            f"- *'Give me technical interview questions based on my resume.'*\n"
            f"- *'How can I prepare for campus placement online tests?'*\n\n"
            f"Current Profile: `{len(resume_skills)} skills detected`, Target: `{target_role}`."
        )
