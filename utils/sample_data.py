"""
utils/sample_data.py
Sample Resumes and Job Descriptions for instant testing, evaluation, and viva demonstration.
Also includes a helper to generate test PDF files automatically using ReportLab.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SAMPLE_JOB_DESCRIPTIONS = {
    "Backend Software Engineer (Python/Java)": """
Role: Junior Software Development Engineer (Backend)
Location: Bangalore / Hyderabad / Hybrid

Job Requirements & Responsibilities:
- Strong programming skills in Python or Java with understanding of OOP concepts.
- Solid foundation in Data Structures, Algorithms (DSA), and time/space complexity analysis.
- Experience building RESTful APIs using Django, Flask, or FastAPI.
- Knowledge of relational databases like PostgreSQL, MySQL, and writing optimized SQL queries.
- Familiarity with version control using Git and GitHub.
- Basic understanding of Docker, Linux environments, and CI/CD pipelines.
- Good communication and teamwork skills in an Agile environment.
""",
    "Data Scientist / AI Engineer": """
Role: Associate Data Scientist
Location: Pune / Bangalore

Job Requirements:
- Hands-on experience with Python for data manipulation (pandas, numpy, scipy).
- Experience with Machine Learning algorithms using scikit-learn (classification, regression, clustering).
- Knowledge of Deep Learning fundamentals, PyTorch or TensorFlow, and Natural Language Processing (NLP).
- Proficiency in SQL for extracting and aggregating complex datasets.
- Experience with data visualization tools such as Matplotlib, Seaborn, Tableau, or Power BI.
- Strong analytical and problem-solving mindset.
""",
    "Full-Stack Web Developer": """
Role: Full-Stack Web Developer
Location: Chennai / Remote

Job Requirements:
- Proficiency in JavaScript and TypeScript.
- Hands-on experience building frontend web applications with React, HTML, CSS, and Tailwind CSS.
- Backend server experience using Node.js and Express.
- Experience working with MongoDB or PostgreSQL databases.
- Familiarity with REST APIs, authentication (JWT), and Git.
"""
}

SAMPLE_RESUME_TEXTS = {
    "Alex_Rivera_SDE": """Alex Rivera
Email: alex.rivera@example.com | Phone: +91 9876543210
LinkedIn: https://linkedin.com/in/alexrivera-dev | GitHub: https://github.com/alexrivera

EDUCATION
Bachelor of Technology in Computer Science and Engineering
CGPA: 8.4 / 10.0 | Expected Graduation: 2026

TECHNICAL SKILLS
- Programming Languages: Python, Java, C++, SQL, JavaScript
- Frameworks & Libraries: Django, Flask, FastAPI, React, Node.js
- Databases: PostgreSQL, MySQL, Redis, MongoDB
- Tools & DevOps: Git, GitHub, Docker, Linux, CI/CD, REST API
- Core Concepts: Data Structures, Algorithms, OOP, DBMS, Operating Systems

PROJECTS
1. Distributed E-Commerce Microservices Platform
- Built scalable backend microservices using Python, FastAPI, and Docker.
- Implemented Redis caching, reducing database read latency by 42%.
- Designed relational schemas in PostgreSQL and integrated JWT token authentication.

2. Real-Time Collaborative Code Editor
- Developed web-based code workspace using React, Node.js, and WebSockets.
- Supported simultaneous editing for 100+ concurrent users with sub-50ms sync speed.

EXPERIENCE & INTERNSHIPS
Software Engineering Intern | TechNova Labs (June 2025 - August 2025)
- Automated deployment workflows using GitHub Actions and Docker.
- Optimized 15+ database SQL queries, reducing API response times by 30%.

CERTIFICATIONS
- AWS Certified Cloud Practitioner
- Meta Backend Developer Professional Certificate
""",

    "Priya_Sharma_DataScience": """Priya Sharma
Email: priya.sharma@example.com | Phone: +91 9123456789
LinkedIn: https://linkedin.com/in/priyasharma-ds | GitHub: https://github.com/priyads

EDUCATION
B.E. in Artificial Intelligence and Data Science
CGPA: 8.8 / 10.0 | Graduating: 2026

TECHNICAL SKILLS
- Languages: Python, R, SQL
- Machine Learning & AI: Machine Learning, Deep Learning, NLP, Scikit-Learn, TensorFlow, Pandas, NumPy
- Visualization & BI: Matplotlib, Seaborn, Power BI, Tableau
- Developer Tools: Git, Linux, Jupyter Notebook, Flask

PROJECTS
1. Customer Churn Prediction Engine
- Trained Random Forest and XGBoost classifiers on 10,000+ customer records.
- Achieved 89% accuracy and 0.85 F1-score with hyperparameter tuning in Scikit-Learn.
- Visualized feature importances and key attrition factors using Seaborn.

2. Biomedical Text Summarization using NLP
- Extracted medical research insights using Natural Language Processing and Hugging Face transformers.
- Deployed lightweight interactive web dashboard using Flask and Docker.

INTERNSHIPS
Data Science Intern | AnalyticsCorp (Jan 2026 - April 2026)
- Cleaned and transformed 500k+ transactional rows using Pandas and SQL.
- Created interactive Power BI dashboards monitored weekly by executive leadership.

CERTIFICATIONS
- Deep Learning Specialization (Coursera)
- Python for Data Science and Machine Learning (Udemy)
"""
}


def generate_sample_pdfs(output_dir: str = "data/sample_resumes"):
    """Generate real sample PDF files for easy testing and demonstration."""
    os.makedirs(output_dir, exist_ok=True)
    pdf_paths = {}

    for name, content in SAMPLE_RESUME_TEXTS.items():
        pdf_path = os.path.join(output_dir, f"{name}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        y = height - 50
        lines = content.strip().split("\n")
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, lines[0])  # Candidate name
        y -= 20

        c.setFont("Helvetica", 9)
        for line in lines[1:]:
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 9)

            if line.isupper() and len(line) < 30:
                y -= 8
                c.setFont("Helvetica-Bold", 11)
                c.drawString(50, y, line)
                y -= 14
                c.setFont("Helvetica", 9)
            elif line.startswith("-") or line.startswith("1.") or line.startswith("2."):
                c.drawString(65, y, line[:95])
                y -= 13
            elif line.strip() == "":
                y -= 6
            else:
                c.drawString(50, y, line[:100])
                y -= 13

        c.save()
        pdf_paths[name] = pdf_path

    return pdf_paths
