import React, { useState } from 'react';
import { 
  Target, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  Info, 
  ArrowRight,
  Sparkles,
  BarChart3
} from 'lucide-react';
import { computeMatching, analyzeJobDescription } from '../api/client';

export default function JobMatching({ resumeData, matchingResult, setMatchingResult, setActiveTab }) {
  const [jobTitle, setJobTitle] = useState('Backend Software Engineer');
  const [jobDescription, setJobDescription] = useState(
`Role: Backend Software Engineer (Python/FastAPI)
Responsibilities:
- Build high-performance RESTful APIs using Python, FastAPI, and PostgreSQL.
- Architect microservices and containerize applications with Docker and Linux.
- Implement Redis caching for low-latency session and data management.
- Collaborate with frontend teams utilizing Git and CI/CD pipelines.
- Solid understanding of Data Structures, Algorithms, and Object-Oriented Design.`
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const SAMPLE_PRESETS = [
    {
      title: "Backend Software Engineer",
      text: `Role: Backend Software Engineer (Python/FastAPI)
Responsibilities:
- Build high-performance RESTful APIs using Python, FastAPI, and PostgreSQL.
- Architect microservices and containerize applications with Docker and Linux.
- Implement Redis caching for low-latency session and data management.
- Collaborate with frontend teams utilizing Git and CI/CD pipelines.
- Solid understanding of Data Structures, Algorithms, and Object-Oriented Design.`
    },
    {
      title: "Data Scientist / ML Engineer",
      text: `Role: Data Scientist / ML Engineer
Requirements:
- Strong proficiency in Python for data analysis using Pandas, NumPy, and Scikit-Learn.
- Experience training Machine Learning and Deep Learning models with TensorFlow or PyTorch.
- Knowledge of Natural Language Processing (NLP) techniques and SQL database querying.
- Ability to create analytical dashboards with Power BI or Tableau.
- Containerization with Docker and version control using Git.`
    },
    {
      title: "Full-Stack Web Developer",
      text: `Role: Junior Full-Stack Developer
Requirements:
- Hands-on experience developing web applications with JavaScript, TypeScript, and React.
- Backend server experience using Node.js, Express, and REST APIs.
- Experience with databases like MongoDB or PostgreSQL.
- Understanding of HTML, CSS, Tailwind CSS, and Git version control.`
    }
  ];

  const handleMatch = async (e) => {
    e.preventDefault();
    if (!resumeData || !resumeData.text) {
      setError('Please upload or select a resume in the Resume Analyzer module first.');
      return;
    }
    if (!jobDescription || jobDescription.trim().split(/\s+/).length < 5) {
      setError('Please enter a descriptive job description (at least 1-2 paragraphs).');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await computeMatching({
        resumeText: resumeData.text,
        jobText: jobDescription,
        resumeFilename: resumeData.filename || 'Resume.pdf',
        jobTitle: jobTitle || 'Target Role',
        resumeSkills: resumeData.extracted_skills || [],
        saveToHistory: true,
      });
      setMatchingResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const applyPreset = (preset) => {
    setJobTitle(preset.title);
    setJobDescription(preset.text);
    setError(null);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Module 2 — Job Matching</h2>
        <p className="text-xs text-slate-600 mt-1">
          Compute baseline text similarity using <strong>TF-IDF n-gram vectorization</strong> and <strong>Cosine Similarity</strong>.
          Evaluates direct vocabulary overlap against job description requirements.
        </p>
      </div>

      {!resumeData && (
        <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl flex items-center justify-between text-xs text-amber-800">
          <div className="flex items-center space-x-2">
            <AlertTriangle size={16} className="text-amber-600 shrink-0" />
            <span>No active resume loaded. Please upload or load a resume in Module 1 before running matching.</span>
          </div>
          <button
            onClick={() => setActiveTab('resume')}
            className="font-semibold text-indigo-600 hover:underline shrink-0 ml-4"
          >
            Go to Resume Analyzer →
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Job Input Card */}
        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
              <Target size={16} className="text-indigo-600" />
              <span>Target Job Description</span>
            </h3>
            <span className="text-[11px] text-slate-400">Word count: {jobDescription.trim().split(/\s+/).filter(Boolean).length}</span>
          </div>

          {/* Quick presets */}
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">
              Load Preset Role:
            </span>
            <div className="flex flex-wrap gap-1.5">
              {SAMPLE_PRESETS.map((p) => (
                <button
                  key={p.title}
                  type="button"
                  onClick={() => applyPreset(p)}
                  className="px-2.5 py-1 rounded text-xs border border-slate-200 bg-slate-50 text-slate-700 hover:bg-indigo-50 hover:border-indigo-300 transition-colors"
                >
                  {p.title}
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleMatch} className="space-y-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Target Job Title</label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Senior Software Engineer"
                className="w-full text-xs px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Job Description Requirements</label>
              <textarea
                rows={9}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description and requirements here..."
                className="w-full text-xs p-3 border border-slate-200 rounded-lg font-mono focus:outline-none focus:ring-2 focus:ring-indigo-500 leading-relaxed"
              />
            </div>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-700">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !resumeData}
              className={`w-full py-2.5 px-4 rounded-lg text-xs font-semibold text-white shadow-sm transition-all ${
                loading || !resumeData
                  ? 'bg-slate-300 cursor-not-allowed'
                  : 'bg-indigo-600 hover:bg-indigo-700 active:scale-[0.99]'
              }`}
            >
              {loading ? 'Computing TF-IDF Vector Similarity...' : 'Calculate Similarity & Match Skills'}
            </button>
          </form>

          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-[11px] text-slate-500 space-y-1">
            <div className="font-semibold text-slate-700 flex items-center space-x-1">
              <Info size={12} className="text-indigo-600" />
              <span>Scientific Caveat:</span>
            </div>
            <p>
              This algorithm computes mathematical TF-IDF cosine vector similarity between both texts. It represents a baseline text-similarity metric and should not be confused with human hiring decisions.
            </p>
          </div>
        </div>

        {/* Results Card */}
        <div className="lg:col-span-7 space-y-5">
          {!matchingResult ? (
            <div className="bg-white rounded-xl border border-slate-200 p-12 text-center shadow-sm">
              <BarChart3 size={40} className="mx-auto text-slate-300 mb-3" />
              <h4 className="text-sm font-semibold text-slate-700">No Matching Computed Yet</h4>
              <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
                Submit a job description on the left to calculate similarity score and inspect overlapping and missing skill tags.
              </p>
            </div>
          ) : (
            <>
              {/* Score Display Card */}
              <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div>
                    <span className="text-xs font-semibold uppercase text-slate-500 tracking-wider">
                      Baseline Similarity Score
                    </span>
                    <div className="flex items-baseline space-x-2 mt-1">
                      <span className="text-4xl font-extrabold text-indigo-700">
                        {matchingResult.similarity_score}%
                      </span>
                      <span className="text-xs text-slate-500 font-medium">TF-IDF Cosine Baseline</span>
                    </div>
                    <p className="text-xs text-slate-500 mt-1">
                      Skill coverage ratio: <strong>{matchingResult.skill_coverage_percentage}%</strong> of requirements detected
                    </p>
                  </div>

                  <button
                    onClick={() => setActiveTab('skillgap')}
                    className="flex items-center space-x-1 px-3 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-lg text-xs font-semibold transition-colors shrink-0"
                  >
                    <span>View Gap Analysis</span>
                    <ArrowRight size={13} />
                  </button>
                </div>

                {/* Progress bar */}
                <div className="mt-4 w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div 
                    className="bg-indigo-600 h-full rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(100, matchingResult.similarity_score)}%` }}
                  />
                </div>
              </div>

              {/* Skills Overlap Breakdown */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Matched Skills */}
                <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-emerald-800 flex items-center space-x-1.5">
                      <CheckCircle2 size={14} className="text-emerald-600" />
                      <span>Matched Skills ({matchingResult.matched_skills.length})</span>
                    </span>
                  </div>
                  {matchingResult.matched_skills.length === 0 ? (
                    <p className="text-xs text-slate-400 italic">No direct overlap detected.</p>
                  ) : (
                    <div className="flex flex-wrap gap-1.5">
                      {matchingResult.matched_skills.map((s) => (
                        <span key={s} className="bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded text-[11px] font-semibold">
                          ✓ {s}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Missing Skills */}
                <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-amber-800 flex items-center space-x-1.5">
                      <XCircle size={14} className="text-amber-600" />
                      <span>Missing from Resume ({matchingResult.missing_skills.length})</span>
                    </span>
                  </div>
                  {matchingResult.missing_skills.length === 0 ? (
                    <p className="text-xs text-emerald-600 font-medium">All job skills present in resume!</p>
                  ) : (
                    <div className="flex flex-wrap gap-1.5">
                      {matchingResult.missing_skills.map((s) => (
                        <span key={s} className="bg-amber-50 text-amber-800 border border-amber-200 px-2 py-0.5 rounded text-[11px] font-semibold">
                          ✕ {s}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Additional Resume Skills */}
              <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
                <span className="text-xs font-bold text-slate-700 block mb-2">
                  Additional Profile Skills Not Requested by Job ({matchingResult.additional_skills.length})
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {matchingResult.additional_skills.slice(0, 15).map((s) => (
                    <span key={s} className="bg-slate-100 text-slate-700 border border-slate-200 px-2 py-0.5 rounded text-[11px]">
                      {s}
                    </span>
                  ))}
                  {matchingResult.additional_skills.length > 15 && (
                    <span className="text-[11px] text-slate-400 self-center">
                      +{matchingResult.additional_skills.length - 15} more
                    </span>
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
