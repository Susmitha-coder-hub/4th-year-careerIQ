"""
modules/placement_predictor.py
Module 3: Placement Intelligence
- Machine Learning models for campus placement readiness prediction
- Compares Logistic Regression and Random Forest Classifiers
- Computes formal evaluation metrics (Accuracy, Precision, Recall, F1-Score)
- Interprets feature importances and transparently outlines model limitations
- Delivers targeted skill uplift and curriculum/course recommendations
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.preprocessing import StandardScaler

MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "placement_model.pkl")
DATASET_FILE = "data/placement_dataset.csv"

# Recommended courses based on student gaps
RECOMMENDED_RESOURCES = {
    "Technical Skills": [
        {"title": "Data Structures & Algorithms Masterclass", "platform": "LeetCode / Coursera", "duration": "6 weeks"},
        {"title": "Full-Stack Web Development Bootcamp", "platform": "freeCodeCamp / Udemy", "duration": "8 weeks"},
        {"title": "Applied Machine Learning in Python", "platform": "Coursera (Univ. of Michigan)", "duration": "5 weeks"},
    ],
    "Aptitude & Problem Solving": [
        {"title": "Quantitative Aptitude & Logical Reasoning for Placements", "platform": "IndiaBIX / GeeksforGeeks", "duration": "4 weeks"},
        {"title": "Fast Math & Verbal Ability for Campus Drives", "platform": "PrepInsta / Unacademy", "duration": "3 weeks"},
    ],
    "Communication & Soft Skills": [
        {"title": "Effective Communication & Group Discussion (GD) Prep", "platform": "Coursera / LinkedIn Learning", "duration": "2 weeks"},
        {"title": "Technical Interview Speaking & Behavioral STAR Method", "platform": "Interviewing.io / YouTube", "duration": "2 weeks"},
    ],
    "Projects & Internships": [
        {"title": "Build & Deploy a Production MERN/Django Cloud App", "platform": "GitHub Projects / YouTube", "duration": "4 weeks"},
        {"title": "Open Source Contribution Guide for Students", "platform": "Google Summer of Code Archive", "duration": "Self-paced"},
    ]
}


def load_or_train_model() -> Tuple[Any, Any, Dict[str, Any]]:
    """
    Load pre-trained model and scaler or train from data/placement_dataset.csv.
    Returns: (trained_model, scaler, evaluation_metrics)
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    if os.path.exists(MODEL_FILE):
        try:
            saved_data = joblib.load(MODEL_FILE)
            return saved_data["model"], saved_data["scaler"], saved_data["metrics"]
        except Exception:
            pass  # Retrain if corrupted
            
    # If dataset doesn't exist, create it
    if not os.path.exists(DATASET_FILE):
        from scripts.generate_placement_data import generate_dataset
        generate_dataset(output_path=DATASET_FILE)
        
    df = pd.read_csv(DATASET_FILE)
    
    feature_cols = [
        "CGPA", "Technical_Score", "Communication_Score",
        "Internships", "Projects", "Aptitude_Test_Score", "Coding_Problems_Solved"
    ]
    
    X = df[feature_cols]
    y = df["Placed"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    
    # Train Logistic Regression baseline for comparison
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    
    y_pred_rf = rf_model.predict(X_test_scaled)
    y_pred_lr = lr_model.predict(X_test_scaled)
    
    metrics = {
        "RandomForest": {
            "accuracy": round(float(accuracy_score(y_test, y_pred_rf)), 4),
            "precision": round(float(precision_score(y_test, y_pred_rf, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, y_pred_rf, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, y_pred_rf, zero_division=0)), 4),
        },
        "LogisticRegression": {
            "accuracy": round(float(accuracy_score(y_test, y_pred_lr)), 4),
            "precision": round(float(precision_score(y_test, y_pred_lr, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, y_pred_lr, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, y_pred_lr, zero_division=0)), 4),
        },
        "feature_importances": dict(zip(feature_cols, [round(float(v), 3) for v in rf_model.feature_importances_])),
        "sample_count": len(df),
        "test_size": len(y_test),
        "feature_cols": feature_cols
    }
    
    # Save the Random Forest as the primary production model
    joblib.dump({"model": rf_model, "scaler": scaler, "metrics": metrics}, MODEL_FILE)
    return rf_model, scaler, metrics


def predict_placement_readiness(
    cgpa: float,
    tech_score: float,
    comm_score: float,
    internships: int,
    projects: int,
    aptitude_score: float,
    coding_problems: int
) -> Dict[str, Any]:
    """
    Run student profile through the trained ML model.
    Returns probability of placement, readiness badge, feature gap analysis, and tailored courses.
    """
    model, scaler, metrics = load_or_train_model()
    
    input_df = pd.DataFrame([[
        cgpa, tech_score, comm_score, internships, projects, aptitude_score, coding_problems
    ]], columns=metrics["feature_cols"])
    
    scaled_input = scaler.transform(input_df)
    placement_prob = float(model.predict_proba(scaled_input)[0][1])
    is_ready = bool(placement_prob >= 0.50)
    readiness_percentage = round(placement_prob * 100, 1)
    
    # Identify specific gaps
    gap_recommendations = []
    if cgpa < 7.0:
        gap_recommendations.append("CGPA is below standard tier-1 MNC cutoffs (typically 7.0 or 7.5). Target remaining semesters to lift aggregate.")
    if tech_score < 6.5:
        gap_recommendations.append("Technical competency rating is in the development zone. Deepen understanding of core DSA and system fundamentals.")
    if aptitude_score < 65.0:
        gap_recommendations.append("Aptitude score is under standard first-round clearance threshold (~65%). Practice speed math and logical reasoning daily.")
    if comm_score < 6.5:
        gap_recommendations.append("Communication score could pose risk during Group Discussions and HR screening. Engage in mock interviews and presentation practice.")
    if internships == 0:
        gap_recommendations.append("No industry internship on record. Build 2 high-quality production projects with live URLs or open-source PRs to compensate.")
    if coding_problems < 100:
        gap_recommendations.append(f"Only ~{coding_problems} coding problems solved. Aim for at least 150-200 DSA problems on platforms like LeetCode or HackerRank.")

    # Select recommended learning paths
    curated_courses = []
    if tech_score < 7.0 or coding_problems < 150:
        curated_courses.extend(RECOMMENDED_RESOURCES["Technical Skills"])
    if aptitude_score < 70.0:
        curated_courses.extend(RECOMMENDED_RESOURCES["Aptitude & Problem Solving"])
    if comm_score < 7.0:
        curated_courses.extend(RECOMMENDED_RESOURCES["Communication & Soft Skills"])
    if internships == 0 or projects < 2:
        curated_courses.extend(RECOMMENDED_RESOURCES["Projects & Internships"])

    # Readiness tier
    if readiness_percentage >= 75:
        tier = "High Readiness (Campus Drive Ready)"
        tier_color = "green"
    elif readiness_percentage >= 50:
        tier = "Moderate Readiness (Needs Targeted Refinement)"
        tier_color = "orange"
    else:
        tier = "Critical Readiness Gap (Intensive Preparation Required)"
        tier_color = "red"

    return {
        "readiness_percentage": readiness_percentage,
        "is_ready": is_ready,
        "readiness_tier": tier,
        "tier_color": tier_color,
        "gap_recommendations": gap_recommendations,
        "curated_courses": curated_courses[:6],  # top 6
        "model_metrics": metrics
    }
