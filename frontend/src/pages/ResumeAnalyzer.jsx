import React, { useState } from 'react';
import { 
  Upload, 
  FileCheck, 
  AlertCircle, 
  User, 
  Mail, 
  Phone, 
  Globe, 
  Code, 
  Layers, 
  FileText,
  Sparkles
} from 'lucide-react';
import { uploadAndParseResume } from '../api/client';

export default function ResumeAnalyzer({ resumeData, setResumeData, setActiveTab }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Synthetic demo resumes for immediate evaluator testing
  const SYNTHETIC_DEMO_RESUMES = {
    sde: {
      name: "Alex Rivera (Backend Software Engineer)",
      text: `Alex Rivera
Email: alex.rivera@example.com | Phone: +91 9876543210
LinkedIn: https://linkedin.com/in/alexrivera-dev | GitHub: https://github.com/alexrivera

EDUCATION
B.Tech in Computer Science and Engineering, CGPA: 8.4

TECHNICAL SKILLS
Languages: Python, Java, C++, SQL, JavaScript
Frameworks: FastAPI, Django, Flask, React, Node.js
Databases: PostgreSQL, MySQL, Redis, MongoDB
DevOps & Tools: Docker, Linux, Git, GitHub, REST API, CI/CD
Core CS: Data Structures, Algorithms, OOP, DBMS, Operating Systems

PROJECTS
Distributed Microservices Backend
- Architected modular REST APIs using Python, FastAPI, and Docker.
- Implemented Redis caching, optimizing database query response latency by 40%.
- Designed relational schemas in PostgreSQL and integrated JWT token authentication.

Real-Time Code Collaboration Tool
- Developed web backend using Node.js, Express, and WebSocket connections.
- Handled concurrent state synchronization across multiple connected sessions.`,
      filename: "Alex_Rivera_SDE.pdf",
      contact_info: {
        email: "alex.rivera@example.com",
        phone: "+91 9876543210",
        linkedin: "https://linkedin.com/in/alexrivera-dev",
        github: "https://github.com/alexrivera"
      },
      page_count: 1,
      word_count: 145,
      extracted_skills: ["python", "java", "c++", "sql", "javascript", "fastapi", "django", "flask", "react", "node.js", "postgresql", "mysql", "redis", "mongodb", "docker", "linux", "git", "rest api", "ci/cd", "data structures", "algorithms", "oop", "dbms", "operating systems"],
      categorized_skills: {
        "Programming Languages": ["python", "java", "c++", "sql", "javascript"],
        "Web & Backend Frameworks": ["fastapi", "django", "flask", "react", "node.js", "rest api"],
        "Databases & Storage": ["postgresql", "mysql", "redis", "mongodb"],
        "Cloud & DevOps": ["docker", "linux", "git", "ci/cd"],
        "Core Computer Science": ["data structures", "algorithms", "oop", "dbms", "operating systems"]
      }
    },
    ds: {
      name: "Priya Sharma (Data Science & ML)",
      text: `Priya Sharma
Email: priya.sharma@example.com | Phone: +91 9123456789
LinkedIn: https://linkedin.com/in/priyasharma-ds | GitHub: https://github.com/priyads

EDUCATION
B.E. in Artificial Intelligence and Data Science, CGPA: 8.8

TECHNICAL SKILLS
Languages: Python, R, SQL
Machine Learning: Machine Learning, Deep Learning, NLP, Scikit-Learn, TensorFlow, Pandas, NumPy
Visualization: Matplotlib, Seaborn, Tableau, Power BI
Tools: Git, Linux, Docker, Flask

PROJECTS
Predictive Customer Churn Model
- Trained Random Forest and XGBoost classifiers on 10,000+ customer records.
- Evaluated performance with Scikit-Learn achieving 88% precision and 0.84 F1-score.
- Conducted exploratory data analysis and feature correlation with Pandas and Seaborn.`,
      filename: "Priya_Sharma_DataScience.pdf",
      contact_info: {
        email: "priya.sharma@example.com",
        phone: "+91 9123456789",
        linkedin: "https://linkedin.com/in/priyasharma-ds",
        github: "https://github.com/priyads"
      },
      page_count: 1,
      word_count: 130,
      extracted_skills: ["python", "r", "sql", "machine learning", "deep learning", "nlp", "scikit-learn", "tensorflow", "pandas", "numpy", "matplotlib", "seaborn", "tableau", "power bi", "git", "linux", "docker", "flask"],
      categorized_skills: {
        "Programming Languages": ["python", "r", "sql"],
        "Data Science & AI/ML": ["machine learning", "deep learning", "nlp", "scikit-learn", "tensorflow", "pandas", "numpy", "matplotlib", "seaborn", "tableau", "power bi"],
        "Cloud & DevOps": ["git", "linux", "docker"],
        "Web & Backend Frameworks": ["flask"]
      }
    }
  };

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      if (!selected.name.toLowerCase().endsWith('.pdf')) {
        setError('Invalid file format. Please upload a standard PDF (.pdf) document.');
        setFile(null);
        return;
      }
      if (selected.size > 5 * 1024 * 1024) {
        setError('File size exceeds the 5 MB limit.');
        setFile(null);
        return;
      }
      setFile(selected);
      setError(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF file to upload.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await uploadAndParseResume(file);
      setResumeData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadSyntheticDemo = (key) => {
    setError(null);
    const demo = SYNTHETIC_DEMO_RESUMES[key];
    setResumeData({
      filename: demo.filename,
      page_count: demo.page_count,
      word_count: demo.word_count,
      text: demo.text,
      text_preview: demo.text.substring(0, 450) + "...",
      contact_info: demo.contact_info,
      extracted_skills: demo.extracted_skills,
      categorized_skills: demo.categorized_skills,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Module 1 — Resume Analyzer</h2>
        <p className="text-xs text-slate-600 mt-1">
          Upload a PDF resume to extract selectable text using <strong>pypdf</strong> and detect technical skills using transparent rule-based matching.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload Form Card */}
        <div className="lg:col-span-1 bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
            <Upload size={16} className="text-indigo-600" />
            <span>Upload Candidate Resume</span>
          </h3>

          <form onSubmit={handleUpload} className="space-y-4">
            <div className="border-2 border-dashed border-slate-200 rounded-lg p-5 text-center hover:border-indigo-400 transition-colors">
              <input
                type="file"
                id="resume-file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
              />
              <label htmlFor="resume-file" className="cursor-pointer flex flex-col items-center">
                <FileText size={32} className="text-slate-400 mb-2" />
                <span className="text-xs font-medium text-slate-700">
                  {file ? file.name : "Click to select PDF resume"}
                </span>
                <span className="text-[11px] text-slate-400 mt-1">PDF format only (Max 5 MB)</span>
              </label>
            </div>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-2 text-xs text-red-700">
                <AlertCircle size={15} className="shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !file}
              className={`w-full py-2.5 px-4 rounded-lg text-xs font-semibold text-white shadow-sm transition-all ${
                loading || !file 
                  ? 'bg-slate-300 cursor-not-allowed' 
                  : 'bg-indigo-600 hover:bg-indigo-700 active:scale-[0.99]'
              }`}
            >
              {loading ? 'Parsing with pypdf...' : 'Parse Resume'}
            </button>
          </form>

          {/* Quick Demo Previews */}
          <div className="pt-3 border-t border-slate-100">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
              Or Load Synthetic Demo Resume
            </span>
            <div className="space-y-2">
              <button
                type="button"
                onClick={() => loadSyntheticDemo('sde')}
                className="w-full text-left p-2 rounded-lg border border-slate-200 text-xs text-slate-700 hover:bg-indigo-50 hover:border-indigo-300 transition-colors flex items-center justify-between"
              >
                <span>Alex Rivera (SDE Profile)</span>
                <Sparkles size={13} className="text-indigo-600" />
              </button>
              <button
                type="button"
                onClick={() => loadSyntheticDemo('ds')}
                className="w-full text-left p-2 rounded-lg border border-slate-200 text-xs text-slate-700 hover:bg-indigo-50 hover:border-indigo-300 transition-colors flex items-center justify-between"
              >
                <span>Priya Sharma (Data Science)</span>
                <Sparkles size={13} className="text-indigo-600" />
              </button>
            </div>
          </div>

          <div className="text-[11px] text-slate-400 bg-slate-50 p-2.5 rounded border border-slate-100">
            ℹ️ Scanned/image-only PDFs require OCR which is scheduled for subsequent milestones. This module validates and parses selectable text streams.
          </div>
        </div>

        {/* Parsed Result Display */}
        <div className="lg:col-span-2 space-y-5">
          {!resumeData ? (
            <div className="bg-white rounded-xl border border-slate-200 p-12 text-center shadow-sm">
              <FileCheck size={40} className="mx-auto text-slate-300 mb-3" />
              <h4 className="text-sm font-semibold text-slate-700">No Resume Parsed Yet</h4>
              <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
                Upload a PDF on the left or select a synthetic profile to inspect extracted text and detected skill tags.
              </p>
            </div>
          ) : (
            <>
              {/* Summary Metrics */}
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm text-center">
                  <span className="text-[11px] font-semibold uppercase text-slate-500">Document File</span>
                  <div className="mt-1 text-sm font-bold text-slate-800 truncate" title={resumeData.filename}>
                    {resumeData.filename}
                  </div>
                  <span className="text-[10px] text-slate-400">{resumeData.page_count} page(s)</span>
                </div>

                <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm text-center">
                  <span className="text-[11px] font-semibold uppercase text-slate-500">Word Count</span>
                  <div className="mt-1 text-lg font-bold text-indigo-700">
                    {resumeData.word_count}
                  </div>
                  <span className="text-[10px] text-slate-400">Selectable tokens</span>
                </div>

                <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm text-center">
                  <span className="text-[11px] font-semibold uppercase text-slate-500">Detected Skills</span>
                  <div className="mt-1 text-lg font-bold text-emerald-700">
                    {resumeData.extracted_skills?.length || 0}
                  </div>
                  <span className="text-[10px] text-slate-400">Rule-based matches</span>
                </div>
              </div>

              {/* Contact Info Card */}
              <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
                <h4 className="text-xs font-bold uppercase text-slate-500 tracking-wider mb-3">
                  Detected Contact Information
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="flex items-center space-x-2 text-slate-700">
                    <Mail size={14} className="text-indigo-600 shrink-0" />
                    <span>Email: <strong>{resumeData.contact_info?.email || 'Not detected'}</strong></span>
                  </div>
                  <div className="flex items-center space-x-2 text-slate-700">
                    <Phone size={14} className="text-indigo-600 shrink-0" />
                    <span>Phone: <strong>{resumeData.contact_info?.phone || 'Not detected'}</strong></span>
                  </div>
                  <div className="flex items-center space-x-2 text-slate-700">
                    <Globe size={14} className="text-indigo-600 shrink-0" />
                    <span className="truncate">LinkedIn: <strong>{resumeData.contact_info?.linkedin || 'Not detected'}</strong></span>
                  </div>
                  <div className="flex items-center space-x-2 text-slate-700">
                    <Code size={14} className="text-indigo-600 shrink-0" />
                    <span className="truncate">GitHub: <strong>{resumeData.contact_info?.github || 'Not detected'}</strong></span>
                  </div>
                </div>
              </div>

              {/* Categorized Skills */}
              <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-xs font-bold uppercase text-slate-500 tracking-wider flex items-center space-x-1.5">
                    <Layers size={14} className="text-indigo-600" />
                    <span>Categorized Technical Skills ({resumeData.extracted_skills?.length || 0})</span>
                  </h4>
                  <button
                    onClick={() => setActiveTab('matching')}
                    className="text-xs font-semibold text-indigo-600 hover:underline"
                  >
                    Proceed to Job Match →
                  </button>
                </div>

                <div className="space-y-3">
                  {Object.entries(resumeData.categorized_skills || {}).map(([cat, skills]) => (
                    <div key={cat} className="text-xs">
                      <span className="font-semibold text-slate-700 block mb-1">{cat}:</span>
                      <div className="flex flex-wrap gap-1.5">
                        {skills.map((s) => (
                          <span 
                            key={s} 
                            className="bg-slate-100 text-slate-800 border border-slate-200 px-2 py-0.5 rounded text-[11px] font-medium"
                          >
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Text Preview */}
              <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
                <h4 className="text-xs font-bold uppercase text-slate-500 tracking-wider mb-2">
                  Selectable Text Preview (First 500 chars)
                </h4>
                <pre className="text-[11px] text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-200 whitespace-pre-wrap font-mono max-h-40 overflow-y-auto">
                  {resumeData.text_preview || resumeData.text}
                </pre>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
