"""
app.py
CareerIQ – AI-Based Career Intelligence and Opportunity Assistant
Single-page comprehensive Streamlit dashboard integrating all 5 core modules:
- Module 1: Resume Intelligence (PDF Extraction, ATS Scoring, Suggestions)
- Module 2: Job Intelligence (Skill Extraction, TF-IDF Semantic Matching, Gap Analysis)
- Module 3: Placement Intelligence (Machine Learning Readiness Prediction & Metrics)
- Module 4: Opportunity Intelligence (Placement Email Parsing & Timeline Reminders)
- Module 5: Conversational AI (Context-Grounded Career Advisor)
"""

import os
import streamlit as st
import pandas as pd
from typing import Dict, Any

# Local Modules
from modules.resume_parser import analyze_resume, extract_text_from_pdf
from modules.job_matcher import match_resume_to_job, recommend_jobs_for_resume, BENCHMARK_JOB_ROLES
from modules.placement_predictor import predict_placement_readiness, load_or_train_model
from modules.opportunity_tracker import parse_inbox_opportunities, generate_ics_calendar_reminder
from modules.career_chatbot import generate_context_grounded_response
from utils.sample_data import SAMPLE_JOB_DESCRIPTIONS, SAMPLE_RESUME_TEXTS, generate_sample_pdfs
from utils.exporter import export_analysis_to_json, export_analysis_to_markdown_report

# Page Configuration
st.set_page_config(
    page_title="CareerIQ – AI Career Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished dashboard presentation
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #e9ecef;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .score-badge {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    .skill-tag {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 14px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .skill-matched {
        display: inline-block;
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 14px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .skill-missing {
        display: inline-block;
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 14px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None
if "current_job_match" not in st.session_state:
    st.session_state.current_job_match = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hello! I am your **CareerIQ Assistant**. Upload your resume or ask me any question about ATS scoring, skill gaps, placement readiness, or interview prep!"}
    ]
if "placement_result" not in st.session_state:
    st.session_state.placement_result = None

# Ensure sample files exist
generate_sample_pdfs()


# ==========================================
# SIDEBAR: Candidate Profile & Controls
# ==========================================
with st.sidebar:
    st.title("🎓 CareerIQ")
    st.caption("AI-Powered Career & Placement Assistant")
    st.divider()

    st.subheader("📁 Upload Resume (PDF)")
    uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])

    st.write("— OR Quick Load Demo Resumes —")
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        if st.button("SDE Profile", use_container_width=True):
            sde_pdf_path = "data/sample_resumes/Alex_Rivera_SDE.pdf"
            if os.path.exists(sde_pdf_path):
                st.session_state.resume_data = analyze_resume(sde_pdf_path)
                st.success("Loaded Alex Rivera (SDE)")
    with col_demo2:
        if st.button("Data Science", use_container_width=True):
            ds_pdf_path = "data/sample_resumes/Priya_Sharma_DataScience.pdf"
            if os.path.exists(ds_pdf_path):
                st.session_state.resume_data = analyze_resume(ds_pdf_path)
                st.success("Loaded Priya Sharma (DS)")

    if uploaded_file is not None:
        try:
            with st.spinner("Analyzing resume structure and skills..."):
                st.session_state.resume_data = analyze_resume(uploaded_file)
            st.success("Resume parsed successfully!")
        except Exception as e:
            st.error(f"Error parsing uploaded PDF: {str(e)}")

    st.divider()
    
    # Export Section
    if st.session_state.resume_data:
        st.subheader("📥 Export Audit Report")
        export_payload = {
            **st.session_state.resume_data,
            "job_match": st.session_state.current_job_match,
            "placement_readiness": st.session_state.placement_result
        }
        
        md_report = export_analysis_to_markdown_report(export_payload)
        st.download_button(
            label="Download Markdown Report",
            data=md_report,
            file_name="CareerIQ_Audit_Report.md",
            mime="text/markdown",
            use_container_width=True
        )
        
        json_report = export_analysis_to_json(export_payload)
        st.download_button(
            label="Download JSON Data",
            data=json_report,
            file_name="CareerIQ_Data.json",
            mime="application/json",
            use_container_width=True
        )

    st.caption("System Status: **All 5 Modules Operational**")


# ==========================================
# MAIN INTERFACE TABS
# ==========================================
tab_resume, tab_job, tab_placement, tab_opportunity, tab_chat = st.tabs([
    "📄 Module 1: Resume Intelligence",
    "🎯 Module 2: Job Intelligence",
    "📊 Module 3: Placement Intelligence",
    "📬 Module 4: Opportunity Intelligence",
    "💬 Module 5: Conversational AI"
])


# ----------------------------------------------------
# TAB 1: RESUME INTELLIGENCE
# ----------------------------------------------------
with tab_resume:
    st.header("📄 Resume Intelligence & ATS Scoring")
    st.write("Extract resume contents, evaluate ATS compatibility, categorize technical skills, and inspect transparent improvement tips.")

    if not st.session_state.resume_data:
        st.info("👆 Please upload a PDF resume or click one of the demo profile buttons in the sidebar to begin analysis.")
    else:
        res = st.session_state.resume_data
        ats = res["ats_score"]
        contact = res["contact_info"]

        # Top Metric Cards
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #64748b;">Overall ATS Score</div>
                <div class="score-badge">{ats['total_score']}<span style="font-size:1.2rem; color:#94a3b8;">/100</span></div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #64748b;">Detected Skills</div>
                <div class="score-badge">{len(res['skills'])}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #64748b;">Word Count</div>
                <div class="score-badge">{ats['word_count']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #64748b;">Sections Found</div>
                <div class="score-badge">{sum(1 for v in res['sections'].values() if v)}<span style="font-size:1.2rem; color:#94a3b8;">/5</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        
        # Detailed Breakdown & Contact
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.subheader("📊 Transparent ATS Breakdown")
            for category, item in ats["breakdown"].items():
                ratio = item["score"] / item["max"]
                st.write(f"**{category}** ({item['score']} / {item['max']} pts)")
                st.progress(ratio)

        with col_c2:
            st.subheader("🔍 Contact & Section Detection")
            st.write(f"- **Email:** `{contact.get('email') or 'Not Found'}`")
            st.write(f"- **Phone:** `{contact.get('phone') or 'Not Found'}`")
            st.write(f"- **LinkedIn:** `{contact.get('linkedin') or 'Not Found'}`")
            st.write(f"- **GitHub:** `{contact.get('github') or 'Not Found'}`")
            
            st.write("**Section Headings Recognized:**")
            sec_cols = st.columns(5)
            for idx, (sec_name, present) in enumerate(res["sections"].items()):
                with sec_cols[idx]:
                    st.write(f"{'✅' if present else '❌'} {sec_name.capitalize()}")

        st.divider()

        # Categorized Skills
        st.subheader("🛠️ Extracted Technical Skills (Categorized)")
        if res["categorized_skills"]:
            for category, skills in res["categorized_skills"].items():
                st.markdown(f"**{category}:**")
                tags_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
                st.markdown(tags_html, unsafe_allow_html=True)
                st.write("")
        else:
            st.warning("No categorized skills detected. Consider listing specific technologies clearly.")

        st.divider()

        # Improvement Recommendations
        st.subheader("💡 Fact-Grounded Improvement Suggestions")
        if res["suggestions"]:
            for s in res["suggestions"]:
                with st.expander(f"📌 [{s['category']}] {s['type']}"):
                    st.write(s["message"])
        else:
            st.success("Great job! Your resume satisfies core structural ATS guidelines.")


# ----------------------------------------------------
# TAB 2: JOB INTELLIGENCE
# ----------------------------------------------------
with tab_job:
    st.header("🎯 Job Intelligence & Semantic Matching")
    st.write("Compare resume against job requirements using skill gap analysis and TF-IDF semantic vector similarity.")

    col_jd_sel, col_jd_custom = st.columns([1, 2])
    with col_jd_sel:
        st.subheader("Presets")
        selected_preset = st.selectbox(
            "Load Sample Job Description",
            list(SAMPLE_JOB_DESCRIPTIONS.keys())
        )
        if st.button("Apply Selected Preset"):
            st.session_state.jd_input = SAMPLE_JOB_DESCRIPTIONS[selected_preset]

    with col_jd_custom:
        st.subheader("Job Description Input")
        default_jd_text = st.session_state.get("jd_input", SAMPLE_JOB_DESCRIPTIONS["Backend Software Engineer (Python/Java)"])
        jd_text = st.text_area(
            "Paste target job description:",
            value=default_jd_text,
            height=200
        )

    if st.button("🚀 Run Job Match Analysis", type="primary"):
        if not st.session_state.resume_data:
            st.error("Please upload or load a resume in the sidebar first!")
        elif not jd_text.strip():
            st.error("Please provide a valid job description.")
        else:
            resume_text = st.session_state.resume_data["raw_text"]
            resume_skills = st.session_state.resume_data["skills"]
            match_res = match_resume_to_job(resume_text, resume_skills, jd_text)
            st.session_state.current_job_match = match_res

    if st.session_state.current_job_match:
        m = st.session_state.current_job_match
        st.divider()

        col_score1, col_score2, col_score3 = st.columns(3)
        with col_score1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #64748b;">Composite Match Score</div>
                <div class="score-badge">{m['composite_score']}%</div>
                <div style="font-size:0.85rem; font-weight:600; color:{m['badge_color']};">{m['fit_status']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_score2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #64748b;">Skill Coverage Score</div>
                <div class="score-badge">{m['skill_coverage_score']}%</div>
                <div style="font-size:0.85rem; color:#64748b;">{m['total_matched_skills']} of {m['total_required_skills']} skills matched</div>
            </div>
            """, unsafe_allow_html=True)
        with col_score3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #64748b;">Semantic TF-IDF Alignment</div>
                <div class="score-badge">{m['tfidf_score']}%</div>
                <div style="font-size:0.85rem; color:#64748b;">Cosine similarity of n-grams</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.subheader("🔍 Skill Gap Breakdown")
        col_sk1, col_sk2, col_sk3 = st.columns(3)

        with col_sk1:
            st.markdown(f"**✅ Matched Skills ({len(m['matched_skills'])}):**")
            if m["matched_skills"]:
                st.markdown("".join([f'<span class="skill-matched">{s}</span>' for s in m["matched_skills"]]), unsafe_allow_html=True)
            else:
                st.write("None")

        with col_sk2:
            st.markdown(f"**❌ Missing Skills ({len(m['missing_skills'])}):**")
            if m["missing_skills"]:
                st.markdown("".join([f'<span class="skill-missing">{s}</span>' for s in m["missing_skills"]]), unsafe_allow_html=True)
            else:
                st.success("All specified skills met!")

        with col_sk3:
            st.markdown(f"**➕ Additional Profile Skills ({len(m['additional_skills'])}):**")
            if m["additional_skills"]:
                st.markdown("".join([f'<span class="skill-tag">{s}</span>' for s in m["additional_skills"][:10]]), unsafe_allow_html=True)
            else:
                st.write("None")

    # Campus Benchmark Job Roles Table
    st.divider()
    st.subheader("📋 Campus Role Benchmark Recommendations")
    st.write("Automated comparison of candidate resume across common campus placement role profiles:")
    if st.session_state.resume_data:
        rec_list = recommend_jobs_for_resume(
            st.session_state.resume_data["raw_text"],
            st.session_state.resume_data["skills"]
        )
        rec_df = pd.DataFrame([{
            "Role": r["role"],
            "Domain": r["category"],
            "Min CGPA": r["min_cgpa"],
            "Skill Coverage": f"{r['skill_coverage']}%",
            "Composite Score": f"{r['composite_score']}%",
            "Missing Skills Count": len(r["missing_skills"])
        } for r in rec_list])
        st.dataframe(rec_df, use_container_width=True)
    else:
        st.info("Upload a resume to see benchmark role recommendations.")


# ----------------------------------------------------
# TAB 3: PLACEMENT INTELLIGENCE
# ----------------------------------------------------
with tab_placement:
    st.header("📊 Placement Intelligence & ML Prediction")
    st.write("Estimate placement readiness using trained Machine Learning models (Random Forest vs Logistic Regression) on student academic & aptitude data.")

    # Student Profile Input Controls
    st.subheader("🎓 Student Assessment Parameters")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        input_cgpa = st.slider("Cumulative GPA (CGPA)", min_value=5.0, max_value=10.0, value=7.8, step=0.1)
        input_tech = st.slider("Technical Skill Rating (1-10)", min_value=1.0, max_value=10.0, value=7.5, step=0.5)
    with col_p2:
        input_comm = st.slider("Communication Skill Rating (1-10)", min_value=1.0, max_value=10.0, value=7.0, step=0.5)
        input_aptitude = st.slider("Aptitude Test Score (0-100)", min_value=30.0, max_value=100.0, value=75.0, step=1.0)
    with col_p3:
        input_internships = st.number_input("Completed Internships", min_value=0, max_value=5, value=1)
        input_projects = st.number_input("Major Projects Built", min_value=0, max_value=8, value=3)
        input_problems = st.number_input("Coding Problems Solved (LeetCode / DSA)", min_value=0, max_value=800, value=150)

    if st.button("📈 Compute Placement Readiness Estimate", type="primary"):
        with st.spinner("Executing ML inference pipeline..."):
            pred = predict_placement_readiness(
                cgpa=input_cgpa,
                tech_score=input_tech,
                comm_score=input_comm,
                internships=input_internships,
                projects=input_projects,
                aptitude_score=input_aptitude,
                coding_problems=input_problems
            )
            st.session_state.placement_result = pred

    if st.session_state.placement_result:
        res_p = st.session_state.placement_result
        st.divider()

        col_res1, col_res2 = st.columns([1, 2])
        with col_res1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #64748b;">Placement Readiness Probability</div>
                <div class="score-badge">{res_p['readiness_percentage']}%</div>
                <div style="font-size:0.95rem; font-weight:700; color:{res_p['tier_color']};">{res_p['readiness_tier']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            st.progress(res_p["readiness_percentage"] / 100.0)

        with col_res2:
            st.subheader("🎯 Identified Preparation Gaps")
            if res_p["gap_recommendations"]:
                for gap in res_p["gap_recommendations"]:
                    st.write(f"- ⚠️ {gap}")
            else:
                st.success("Candidate satisfies baseline eligibility across all key indicators!")

        # Curated Learning Courses
        st.subheader("📚 Recommended Upskilling Courses & Resources")
        if res_p["curated_courses"]:
            c_cols = st.columns(2)
            for i, course in enumerate(res_p["curated_courses"]):
                with c_cols[i % 2]:
                    with st.expander(f"📖 {course['title']}"):
                        st.write(f"**Platform:** {course['platform']}")
                        st.write(f"**Estimated Duration:** {course['duration']}")

        # Transparent Academic ML Evaluation Section
        st.divider()
        st.subheader("🔬 Machine Learning Model Evaluation & Limitations (Academic Rigor)")
        st.write("CareerIQ evaluates multiple classifiers on a standardized 20% holdout test set to ensure transparent, reproducible metrics:")

        metrics = res_p["model_metrics"]
        eval_df = pd.DataFrame({
            "Metric": ["Accuracy", "Precision", "Recall", "F1-Score"],
            "Random Forest (Trained)": [
                f"{metrics['RandomForest']['accuracy']:.2%}",
                f"{metrics['RandomForest']['precision']:.2%}",
                f"{metrics['RandomForest']['recall']:.2%}",
                f"{metrics['RandomForest']['f1_score']:.2%}",
            ],
            "Logistic Regression (Baseline)": [
                f"{metrics['LogisticRegression']['accuracy']:.2%}",
                f"{metrics['LogisticRegression']['precision']:.2%}",
                f"{metrics['LogisticRegression']['recall']:.2%}",
                f"{metrics['LogisticRegression']['f1_score']:.2%}",
            ]
        })
        st.dataframe(eval_df, use_container_width=True)

        with st.expander("📌 Model Feature Importances & Known Limitations"):
            st.write("**Random Forest Feature Importances:**")
            fi_df = pd.DataFrame(
                list(metrics["feature_importances"].items()),
                columns=["Feature", "Importance Weight"]
            ).sort_values(by="Importance Weight", ascending=False)
            st.dataframe(fi_df, use_container_width=True)
            
            st.markdown("""
            **Transparent Limitations for Academic Review:**
            1. **Dataset Scope:** The dataset is synthetic and modeled upon typical Indian engineering campus placement cutoff policies (600 samples). In production, institutional datasets must account for branch-specific hiring quotas.
            2. **Soft Skill Quantification:** Communication and technical skills are represented on standardized numeric scales; real-world behavioral interviews introduce subjective human evaluator variance.
            3. **Static Model:** Model does not incorporate macroeconomic market demand shifts or industry hiring freezes in real-time.
            """)


# ----------------------------------------------------
# TAB 4: OPPORTUNITY INTELLIGENCE
# ----------------------------------------------------
with tab_opportunity:
    st.header("📬 Opportunity Intelligence & Placement Tracking")
    st.write("Extract critical campus placement events (deadlines, test dates, interview schedules, shortlist announcements) from university emails.")

    col_op1, col_op2 = st.columns([1, 1])
    with col_op1:
        st.subheader("Mode Selection")
        opp_mode = st.radio(
            "Select Integration Mode:",
            ["Campus Placement Simulation Mode (Offline Demo)", "Official Gmail API (OAuth Setup Guide)"],
            index=0
        )

    with col_op2:
        st.info("🔒 **Data Privacy Assurance:** CareerIQ processes only emails flagged with placement keywords (TPO, Campus Hiring, Assessment, Shortlist) and never accesses unrelated personal communications.")

    if "Simulation" in opp_mode:
        st.subheader("📬 Tracked Placement Notifications")
        opportunities = parse_inbox_opportunities()

        for opp in opportunities:
            with st.container():
                st.markdown(f"### 🏢 {opp['company']} — `{opp['role']}`")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Reg. Deadline", opp["registration_deadline"])
                c2.metric("Online Assessment", opp["test_date"])
                c3.metric("Interview Schedule", opp["interview_date"])
                c4.metric("Status / Alert", "🎉 Shortlist Out!" if opp["is_shortlist"] else "Active Drive")

                # ICS Calendar Export
                ics_data = generate_ics_calendar_reminder(opp)
                st.download_button(
                    label=f"📅 Add {opp['company']} Event to Calendar (.ics)",
                    data=ics_data,
                    file_name=f"{opp['company']}_placement_reminder.ics",
                    mime="text/calendar",
                    key=f"btn_{opp['email_id']}"
                )

                with st.expander("View Original Email Body"):
                    st.text(opp["raw_body"])
                st.divider()

    else:
        st.subheader("🔑 Official Gmail API Architecture Guide")
        st.markdown("""
        To connect to live Gmail accounts in compliance with Google Cloud API standards:
        
        1. **Create Google Cloud Project:** Enable the `Gmail API` via Google Cloud Console.
        2. **Configure OAuth Consent Screen:** Request restricted scope `https://www.googleapis.com/auth/gmail.readonly`.
        3. **Generate Credentials:** Download `credentials.json` and place in project root.
        4. **Scoped Fetch:** Query only matching messages using Gmail filter: `from:(placements OR tpo) OR subject:(hiring OR campus OR shortlist)`.
        
        *Code hook ready in `modules/opportunity_tracker.py`.*
        """)


# ----------------------------------------------------
# TAB 5: CONVERSATIONAL AI
# ----------------------------------------------------
with tab_chat:
    st.header("💬 Conversational AI Career Advisor")
    st.write("Context-aware assistant grounded in your resume results, target job description, and placement readiness.")

    # Context status banner
    skills_count = len(st.session_state.resume_data["skills"]) if st.session_state.resume_data else 0
    ats_display = st.session_state.resume_data["ats_score"]["total_score"] if st.session_state.resume_data else "None"
    st.caption(f"🧠 **Live Context Active:** {skills_count} resume skills detected | ATS Score: {ats_display} | Grounded Q&A Mode")

    # Quick prompt buttons
    st.write("**Quick Questions:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    if qc1.button("How can I improve my ATS score?"):
        quick_query = "How can I improve my ATS score?"
    if qc2.button("What are my missing skills?"):
        quick_query = "What are my missing skills?"
    if qc3.button("Give me technical interview questions"):
        quick_query = "Give me technical interview questions based on my skills"
    if qc4.button("How to increase placement readiness?"):
        quick_query = "How to increase placement readiness?"

    # Display Chat Messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    user_query = st.chat_input("Ask a question about your resume, missing skills, or interview preparation...")
    active_prompt = user_query or quick_query

    if active_prompt:
        st.session_state.chat_history.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        # Build context dictionary from session state
        chat_context = {}
        if st.session_state.resume_data:
            chat_context["skills"] = st.session_state.resume_data["skills"]
            chat_context["ats_score"] = st.session_state.resume_data["ats_score"]
            chat_context["suggestions"] = st.session_state.resume_data["suggestions"]
        if st.session_state.current_job_match:
            chat_context["missing_skills"] = st.session_state.current_job_match.get("missing_skills", [])
            chat_context["target_role"] = "Selected Job Description"
        if st.session_state.placement_result:
            chat_context["readiness_percentage"] = st.session_state.placement_result.get("readiness_percentage", "N/A")

        # Generate grounded response
        assistant_reply = generate_context_grounded_response(active_prompt, chat_context)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
