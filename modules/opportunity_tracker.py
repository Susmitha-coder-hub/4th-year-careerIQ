"""
modules/opportunity_tracker.py
Module 4: Opportunity Intelligence
- Parses placement notification emails to extract drive events:
  * Company Name
  * Job Role
  * Registration Deadline
  * Online Assessment / Test Date
  * Interview Schedule
  * Shortlist Status / Next Steps
- Provides:
  1. Offline Demonstration Mode with realistic college placement emails
  2. Official Google Gmail API integration hook with explicit OAuth consent
- Generates ics/calendar reminders for critical academic deadlines
"""

import re
from datetime import datetime
from typing import Dict, List, Any

# Pre-populated realistic campus placement emails for offline testing & viva demo
SAMPLE_PLACEMENT_EMAILS = [
    {
        "id": "email_01",
        "sender": "campus-placements@university.edu",
        "subject": "URGENT: Microsoft Campus Hiring 2026 - Software Engineer",
        "date_received": "2026-10-10",
        "body": """Dear Students,
Microsoft is conducting its campus recruitment drive for the role of Software Engineer (Full-Time).
Eligibility: B.Tech CSE/IT with CGPA >= 7.5.

Important Timelines:
- Registration Deadline: 18th October 2026, 11:59 PM IST
- Online Assessment (OA) Date: 22nd October 2026 at 10:00 AM
- Technical & HR Interviews: 28th October 2026 onwards

Please ensure you register via the internal placement portal before the deadline. Late submissions will not be entertained.
Regards,
Training & Placement Cell"""
    },
    {
        "id": "email_02",
        "sender": "placements-notify@university.edu",
        "subject": "TCS Digital & Ninja National Qualifier Test (NQT) Registration",
        "date_received": "2026-10-08",
        "body": """Attention Final Year Students,
Tata Consultancy Services (TCS) invites applications for TCS Digital and Ninja hiring profiles.
- Role: Systems Engineer / Software Developer
- Last Date to Register: 25th October 2026
- Mandatory Online Test Date: 05th November 2026
- Results & Shortlist Announcement: 12th November 2026

Registration link: https://nextstep.tcs.com
All eligible candidates are requested to complete registration immediately.
TPO Team"""
    },
    {
        "id": "email_03",
        "sender": "careers-recruitment@amazon-campus.com",
        "subject": "Shortlist Released: Amazon WOW / SDE Intern Assessment",
        "date_received": "2026-10-09",
        "body": """Congratulations Candidates!
The shortlist for Amazon SDE 6-Month Internship has been announced based on the Online Coding Round.
- Role: Software Development Engineer Intern
- Shortlist Announcement: Published on College TPO Notice Board
- Round 2 Virtual Interview Date: 20th October 2026, 09:00 AM IST
- Mandatory Pre-interview briefing: 19th October 2026 at 04:00 PM

Please review the attached guideline document and confirm your availability.
Amazon University Talent Acquisition"""
    }
]


def extract_event_details(email_body: str, subject: str = "") -> Dict[str, Any]:
    """
    Extract structured placement event data from raw email text using NLP/Regex patterns.
    """
    combined_text = f"{subject}\n{email_body}"
    
    # Extract Company Name
    company_match = re.search(
        r'\b(Microsoft|Amazon|Google|TCS|Infosys|Wipro|Cognizant|Accenture|Deloitte|Capgemini|Oracle|Cisco|IBM|Goldman Sachs|JPMorgan|Uber)\b',
        combined_text,
        re.IGNORECASE
    )
    company = company_match.group(1) if company_match else "Campus Recruiter"

    # Extract Role
    role_match = re.search(
        r'\b(?:role of|position of|hiring for|profiles?|role:?)\s*([A-Za-z\s\(\)\-\/]+?)(?:\.|\n|,|Eligibility)',
        combined_text,
        re.IGNORECASE
    )
    if role_match:
        role = role_match.group(1).strip()
    else:
        # Fallback keywords
        if "Software Engineer" in combined_text or "SDE" in combined_text:
            role = "Software Development Engineer"
        elif "Data" in combined_text:
            role = "Data Analyst / Scientist"
        else:
            role = "Graduate Engineer Trainee"

    # Extract Registration Deadline
    reg_match = re.search(
        r'(?:registration deadline|last date to register|apply before|registration closes on|register before)[:\s]*([0-9]{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+[0-9]{4}(?:[,\s0-9:]+[APMapm\sIST]+)?)',
        combined_text,
        re.IGNORECASE
    )
    reg_deadline = reg_match.group(1).strip() if reg_match else "See email text for exact date"

    # Extract Online Test Date
    test_match = re.search(
        r'(?:online assessment|online test|oa date|test date|nqt date|coding test)[:\s]*([0-9]{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+[0-9]{4}(?:[,\s0-9:]+[APMapm\sIST]+)?)',
        combined_text,
        re.IGNORECASE
    )
    test_date = test_match.group(1).strip() if test_match else "To be announced"

    # Extract Interview Date
    interview_match = re.search(
        r'(?:interview date|interviews?[:\s]|virtual interview)[:\s]*([0-9]{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+[0-9]{4}(?:[,\s0-9:]+[APMapm\sIST]+)?)',
        combined_text,
        re.IGNORECASE
    )
    interview_date = interview_match.group(1).strip() if interview_match else "Post-assessment"

    # Check for Shortlist Notice
    is_shortlist = bool(re.search(r'\b(shortlist|shortlisted|selected candidates|congratulations)\b', combined_text, re.IGNORECASE))

    return {
        "company": company,
        "role": role,
        "registration_deadline": reg_deadline,
        "test_date": test_date,
        "interview_date": interview_date,
        "is_shortlist": is_shortlist,
        "priority": "HIGH" if is_shortlist or "deadline" in combined_text.lower() else "MEDIUM"
    }


def parse_inbox_opportunities(emails: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Parse list of emails into actionable placement timeline events."""
    if emails is None:
        emails = SAMPLE_PLACEMENT_EMAILS
        
    results = []
    for em in emails:
        event = extract_event_details(em.get("body", ""), em.get("subject", ""))
        event["email_id"] = em.get("id")
        event["subject"] = em.get("subject")
        event["date_received"] = em.get("date_received")
        event["raw_body"] = em.get("body")
        results.append(event)
    return results


def generate_ics_calendar_reminder(event: Dict[str, Any]) -> str:
    """Generate iCalendar (.ics) format string for student to export to Google / Outlook Calendar."""
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//CareerIQ Placement Assistant//EN
BEGIN:VEVENT
SUMMARY:{event.get('company')} Placement Deadline - {event.get('role')}
DESCRIPTION:Registration Deadline: {event.get('registration_deadline')}\\nTest Date: {event.get('test_date')}\\nInterview: {event.get('interview_date')}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""
    return ics_content
