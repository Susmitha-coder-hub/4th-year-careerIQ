"""
utils/exporter.py
Provides export functions to download analysis results as JSON and structured text reports.
"""

import json
from datetime import datetime
from typing import Dict, Any

def export_analysis_to_json(analysis_results: Dict[str, Any]) -> str:
    """Serialize full analysis session to clean JSON format."""
    clean_dict = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "contact_info": analysis_results.get("contact_info", {}),
        "ats_score": analysis_results.get("ats_score", {}),
        "detected_skills": analysis_results.get("skills", []),
        "categorized_skills": analysis_results.get("categorized_skills", {}),
        "suggestions": analysis_results.get("suggestions", []),
        "job_match": analysis_results.get("job_match", {}),
        "placement_readiness": analysis_results.get("placement_readiness", {})
    }
    return json.dumps(clean_dict, indent=2)


def export_analysis_to_markdown_report(analysis_results: Dict[str, Any]) -> str:
    """Format full analysis into a human-readable text / markdown report."""
    ats = analysis_results.get("ats_score", {})
    skills = analysis_results.get("skills", [])
    suggestions = analysis_results.get("suggestions", [])
    job_match = analysis_results.get("job_match", {})
    placement = analysis_results.get("placement_readiness", {})
    
    report = f"""=======================================================
           CAREERIQ INTELLIGENCE AUDIT REPORT
=======================================================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

1. RESUME ATS ASSESSMENT
-------------------------------------------------------
Total ATS Score: {ats.get('total_score', 'N/A')} / 100
Word Count: {ats.get('word_count', 'N/A')} words
Total Skills Detected: {len(skills)}

Score Breakdown:
"""
    for cat, item in ats.get("breakdown", {}).items():
        report += f"  - {cat}: {item['score']} / {item['max']}\n"

    report += f"""
Detected Skills:
{", ".join(skills) if skills else "None detected"}

2. ACTIONABLE IMPROVEMENT SUGGESTIONS
-------------------------------------------------------
"""
    for i, s in enumerate(suggestions, 1):
        report += f"{i}. [{s['category']}] {s['message']}\n"

    if job_match:
        report += f"""
3. JOB MATCHING & SKILL GAP ANALYSIS
-------------------------------------------------------
Composite Match Score: {job_match.get('composite_score', 'N/A')}%
Skill Coverage: {job_match.get('skill_coverage_score', 'N/A')}%
Semantic TF-IDF Alignment: {job_match.get('tfidf_score', 'N/A')}%
Fit Assessment: {job_match.get('fit_status', 'N/A')}

Matched Skills ({len(job_match.get('matched_skills', []))}):
  {", ".join(job_match.get('matched_skills', []))}

Missing Skills ({len(job_match.get('missing_skills', []))}):
  {", ".join(job_match.get('missing_skills', []))}
"""

    if placement:
        report += f"""
4. PLACEMENT READINESS PREDICTION (ML Model)
-------------------------------------------------------
Estimated Placement Readiness: {placement.get('readiness_percentage', 'N/A')}%
Readiness Tier: {placement.get('readiness_tier', 'N/A')}

Gap Action Items:
"""
        for gap in placement.get('gap_recommendations', []):
            report += f"  - {gap}\n"

    report += """
=======================================================
CareerIQ - AI-Based Career Intelligence System
=======================================================
"""
    return report
