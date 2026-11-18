"""
backend/app/services/chatbot_service.py
Universal CareerFit AI Assistant Engine (Milestone 2 - Points 16 & 17)

Provides platform-independent conversational career guidance:
- Live opportunity lookups and deadline summaries
- Role compatibility and skill alignment explanations
- 48-hour interview & online assessment preparation advice
- Resume enhancement & ATS optimization suggestions
"""

from typing import List, Dict, Any, Optional
from backend.app.models.schemas import ChatMessageRequest, ChatMessageResponse
from backend.app.services.opportunity_service import CAMPUS_OPPORTUNITIES

def handle_chat_query(req: ChatMessageRequest) -> ChatMessageResponse:
    """
    Processes user conversational input with dynamic context from analyzed resume and opportunities.
    """
    user_msg = req.message.lower().strip()
    skills = req.context_skills or []
    cgpa = req.context_cgpa or 7.5
    target_job = req.context_target_job or "Software Development Engineer"

    # 1. Opportunities & Deadlines queries
    if any(k in user_msg for k in ["opportunity", "opportunities", "deadline", "drive", "campus", "this week"]):
        active_opps = [o for o in CAMPUS_OPPORTUNITIES if o.get("is_active")]
        summary = "\n".join([
            f"• **{o['company']}** ({o['role']}): Deadline **{o['registration_deadline']}**, Test **{o.get('test_date', 'TBD')}** (Min CGPA: {o['min_cgpa']})"
            for o in active_opps[:4]
        ])
        reply = (
            f"Here are the active placement opportunities and upcoming deadlines tracked in CareerFit:\n\n"
            f"{summary}\n\n"
            f"💡 **Tip:** Go to the **Opportunity Intelligence** tab to verify your eligibility and generate an interview revision guide."
        )
        suggestions = [
            "Am I eligible for Amazon?",
            "What should I prepare for the upcoming test?",
            "How do I improve my ATS score?"
        ]

    # 2. Preparation & Interview Revision queries
    elif any(k in user_msg for k in ["prepare", "preparation", "interview", "test", "assessment", "revise"]):
        reply = (
            f"For your upcoming technical assessments in roles like **{target_job}**, follow this high-yield 3-step preparation formula:\n\n"
            f"1. **Core Problem Solving (DSA):** Practice 2 questions each in Arrays/Sliding Window, Binary Trees, and HashMaps.\n"
            f"2. **Computer Science Fundamentals:** Revise SQL Joins & Group By, OS Process Scheduling & Deadlocks, and OOP Concepts (Polymorphism, Inheritance).\n"
            f"3. **Resume Project Defense:** Be prepared to explain 1 key architectural decision, trade-off, or concurrency challenge in your listed projects.\n\n"
            f"Would you like sample coding questions or behavioral tips for a specific company?"
        )
        suggestions = [
            "Give me sample coding questions",
            "Why is Amazon suitable for me?",
            "How can I improve my resume?"
        ]

    # 3. Role suitability & Match explanation queries
    elif any(k in user_msg for k in ["why is", "suitable", "fit", "match", "align", "good for me"]):
        known_skills_str = ", ".join(skills[:5]) if skills else "Python, SQL, Git"
        reply = (
            f"Based on your profile with detected skills in **{known_skills_str}** and CGPA of **{cgpa:.1f}**:\n\n"
            f"• **Strengths:** Your core programming background aligns well with software engineering roles requiring backend development and database logic.\n"
            f"• **Growth Areas:** Many top employers also look for cloud fundamentals (AWS/Docker) and REST API system design. Adding a containerized full-stack project will boost your match score above 85%."
        )
        suggestions = [
            "What skills am I missing?",
            "How do I boost my placement readiness?",
            "Show active opportunities"
        ]

    # 4. ATS & Resume Improvement queries
    elif any(k in user_msg for k in ["ats", "resume", "score", "format", "improve"]):
        reply = (
            f"To maximize your resume's ATS score and reviewer impact:\n\n"
            f"1. **Quantify Bullet Points:** Use the Google XYZ formula: *'Accomplished [X] as measured by [Y], by doing [Z]'* (e.g., 'Reduced query latency by 35% by implementing Redis caching').\n"
            f"2. **Clean Standard Headings:** Use unambiguous headings: *Education*, *Technical Skills*, *Projects*, *Work Experience*, *Certifications*.\n"
            f"3. **Eliminate Multi-column Grids:** Complex multi-column templates confuse standard ATS text stream extractors.\n"
            f"4. **Exact Skill Phrasing:** Match job description terminology directly (e.g. write 'FastAPI' instead of just 'Python web framework')."
        )
        suggestions = [
            "Check my placement readiness",
            "What opportunities do I have this week?",
            "Give me sample interview questions"
        ]

    # 5. Fallback general assistant
    else:
        reply = (
            f"Hello! I am your **CareerFit Personal AI Assistant**. I can help you:\n\n"
            f"• **Track Placement Deadlines:** Remind you of upcoming registration and test dates.\n"
            f"• **Explain Skill Gaps:** Tell you what technical competencies a job requires.\n"
            f"• **Prepare for Interviews:** Offer structured 48-hour revision schedules and topics.\n"
            f"• **Enhance Your Resume:** Provide ATS scoring insights and bullet point refinement.\n\n"
            f"What would you like assistance with today?"
        )
        suggestions = [
            "What opportunities do I have this week?",
            "What should I prepare for my interview?",
            "How do I improve my ATS score?",
            "Why is Software Engineer suitable for me?"
        ]

    return ChatMessageResponse(
        reply=reply,
        suggestions=suggestions
    )
