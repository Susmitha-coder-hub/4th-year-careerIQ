"""
backend/app/core/database.py
SQLite database management for CareerFit analysis history and real metrics.
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            resume_filename TEXT NOT NULL,
            job_title TEXT DEFAULT 'Target Role',
            similarity_score REAL NOT NULL,
            matched_skills TEXT NOT NULL,
            missing_skills TEXT NOT NULL,
            resume_skills TEXT NOT NULL,
            job_skills TEXT NOT NULL,
            notes TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

def save_analysis(
    resume_filename: str,
    job_title: str,
    similarity_score: float,
    matched_skills: List[str],
    missing_skills: List[str],
    resume_skills: List[str],
    job_skills: List[str],
    notes: str = ""
) -> int:
    """Save analysis record into SQLite and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses (
            resume_filename, job_title, similarity_score,
            matched_skills, missing_skills, resume_skills, job_skills, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        resume_filename,
        job_title or "Target Role",
        round(similarity_score, 1),
        json.dumps(matched_skills),
        json.dumps(missing_skills),
        json.dumps(resume_skills),
        json.dumps(job_skills),
        notes
    ))
    analysis_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return analysis_id

def get_all_analyses() -> List[Dict[str, Any]]:
    """Retrieve all analysis records sorted by most recent first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analyses ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "resume_filename": r["resume_filename"],
            "job_title": r["job_title"],
            "similarity_score": r["similarity_score"],
            "matched_skills": json.loads(r["matched_skills"]),
            "missing_skills": json.loads(r["missing_skills"]),
            "resume_skills": json.loads(r["resume_skills"]),
            "job_skills": json.loads(r["job_skills"]),
            "notes": r["notes"]
        })
    return results

def delete_analysis(analysis_id: int) -> bool:
    """Delete an analysis record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_dashboard_metrics() -> Dict[str, Any]:
    """Calculate real metrics from the SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM analyses")
    total_count = cursor.fetchone()["total"]
    
    cursor.execute("SELECT AVG(similarity_score) as avg_score FROM analyses")
    avg_row = cursor.fetchone()["avg_score"]
    avg_score = round(avg_row, 1) if avg_row is not None else 0.0

    cursor.execute("SELECT * FROM analyses ORDER BY timestamp DESC LIMIT 5")
    recent_rows = cursor.fetchall()
    conn.close()

    recent = []
    for r in recent_rows:
        recent.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "resume_filename": r["resume_filename"],
            "job_title": r["job_title"],
            "similarity_score": r["similarity_score"],
            "matched_count": len(json.loads(r["matched_skills"])),
            "missing_count": len(json.loads(r["missing_skills"]))
        })

    return {
        "total_analyses": total_count,
        "average_similarity_score": avg_score,
        "recent_analyses": recent
    }
