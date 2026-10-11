"""
scripts/generate_placement_data.py
Generates a realistic campus placement training dataset for Module 3.
Features:
- CGPA (float 4.0 - 10.0)
- Technical_Score (1-10 rating)
- Communication_Score (1-10 rating)
- Internships (0-4 count)
- Projects (0-6 count)
- Aptitude_Test_Score (0-100 score)
- Coding_Problems_Solved (0-500 count)
- Placed (0 or 1 target)
"""

import os
import random
import pandas as pd
import numpy as np

def generate_dataset(n_samples=600, output_path="data/placement_dataset.csv"):
    np.random.seed(42)
    random.seed(42)

    cgpa = np.clip(np.random.normal(7.4, 1.1, n_samples), 5.0, 9.9)
    tech_score = np.clip(np.random.normal(6.5, 1.8, n_samples), 1.0, 10.0)
    comm_score = np.clip(np.random.normal(6.8, 1.6, n_samples), 1.0, 10.0)
    internships = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.35, 0.40, 0.20, 0.05])
    projects = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.15, 0.35, 0.30, 0.15, 0.05])
    aptitude = np.clip(np.random.normal(68, 15, n_samples), 25, 99)
    coding_problems = np.clip(np.random.poisson(120, n_samples), 10, 480)

    # Realistic logistic latent score
    # CGPA weight: 0.35, Aptitude: 0.25, Tech: 0.20, Comm: 0.10, Internships: 0.10
    latent_score = (
        (cgpa - 5.0) / 5.0 * 3.5 +
        (aptitude / 100.0) * 2.5 +
        (tech_score / 10.0) * 2.0 +
        (comm_score / 10.0) * 1.5 +
        (internships / 3.0) * 1.5 +
        (projects / 5.0) * 1.0 +
        np.random.normal(0, 0.8, n_samples)
    )

    # Threshold for placement
    placed = (latent_score > 6.0).astype(int)

    df = pd.DataFrame({
        "CGPA": np.round(cgpa, 2),
        "Technical_Score": np.round(tech_score, 1),
        "Communication_Score": np.round(comm_score, 1),
        "Internships": internships,
        "Projects": projects,
        "Aptitude_Test_Score": np.round(aptitude, 1),
        "Coding_Problems_Solved": coding_problems,
        "Placed": placed
    })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} samples saved to {output_path}. Placement rate: {df['Placed'].mean():.2%}")
    return df

if __name__ == "__main__":
    generate_dataset()
