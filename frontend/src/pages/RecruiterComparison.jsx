import React, { useState } from 'react';
import { 
  Users, 
  Trophy, 
  CheckCircle2, 
  AlertCircle, 
  FileText, 
  Sparkles, 
  Briefcase, 
  Filter, 
  ArrowUpDown,
  Loader2,
  ChevronRight
} from 'lucide-react';
import { rankCandidatesAgainstJD } from '../api/client';

export default function RecruiterComparison() {
  const [jobTitle, setJobTitle] = useState('Full Stack Software Engineer');
  const [jobDescription, setJobDescription] = useState(
    'Seeking an experienced Full Stack Software Engineer to build scalable microservices. Must have strong proficiency in Python, FastAPI, React, SQL databases, Docker containerization, Git version control, and RESTful API architecture.'
  );

  const [candidates, setCandidates] = useState([
    {
      name: 'Alex Rivera',
      resume_text: 'Experienced Software Engineer proficient in Python, FastAPI, React, SQL, PostgreSQL, Docker, Git, and Linux. Built high-concurrency microservices and REST APIs.',
      experience_years: 3.0
    },
    {
      name: 'Priya Sharma',
      resume_text: 'Data Scientist and Python programmer with experience in Machine Learning, Pandas, Scikit-Learn, SQL, and Git. Some exposure to basic FastAPI web services.',
      experience_years: 2.0
    },
    {
      name: 'Jordan Lee',
      resume_text: 'Frontend specialist experienced in HTML, CSS, JavaScript, React, and Tailwind CSS. Limited familiarity with backend SQL or Docker containers.',
      experience_years: 1.5
    }
  ]);

  const [newCandName, setNewCandName] = useState('');
  const [newCandText, setNewCandText] = useState('');
  const [loading, setLoading] = useState(false);
  const [rankingResult, setRankingResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAddCandidate = (e) => {
    e.preventDefault();
    if (!newCandName.trim() || !newCandText.trim()) return;
    setCandidates([
      ...candidates,
      {
        name: newCandName.trim(),
        resume_text: newCandText.trim(),
        experience_years: 1.0
      }
    ]);
    setNewCandName('');
    setNewCandText('');
  };

  const handleRemoveCandidate = (index) => {
    setCandidates(candidates.filter((_, i) => i !== index));
  };

  const handleRunRanking = async () => {
    if (candidates.length === 0) {
      setError('Please add at least one candidate to rank.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await rankCandidatesAgainstJD({
        jobTitle,
        jobDescription,
        candidates
      });
      setRankingResult(res);
    } catch (err) {
      setError(err.message || 'Failed to rank candidates');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
            Milestone 2 • Point 9
          </span>
          <span className="text-xs text-slate-400">|</span>
          <span className="text-xs text-slate-500 font-medium">Recruiter Intelligence</span>
        </div>
        <h2 className="text-xl font-bold text-slate-900 mt-1">Multi-Resume Comparison & Candidate Ranking</h2>
        <p className="text-xs text-slate-600 mt-1">
          Evaluate multiple applicant resumes in batch against a single target job specification with algorithmic match tiers and hiring rationale.
        </p>
      </div>

      {/* 2-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Job Spec & Candidates */}
        <div className="lg:col-span-5 space-y-4">
          {/* Job Description Card */}
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
            <h3 className="text-xs font-bold uppercase text-slate-500 tracking-wider flex items-center space-x-2">
              <Briefcase size={15} className="text-indigo-600" />
              <span>Target Job Specification</span>
            </h3>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Role Title</label>
              <input 
                type="text" 
                value={jobTitle} 
                onChange={(e) => setJobTitle(e.target.value)} 
                className="w-full text-xs border border-slate-300 rounded-lg p-2 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Job Description Requirements</label>
              <textarea 
                rows="4" 
                value={jobDescription} 
                onChange={(e) => setJobDescription(e.target.value)}
                className="w-full text-xs border border-slate-300 rounded-lg p-2.5 font-mono focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>

          {/* Candidate Pool */}
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase text-slate-500 tracking-wider flex items-center space-x-2">
                <Users size={15} className="text-indigo-600" />
                <span>Candidate Pool ({candidates.length})</span>
              </h3>
            </div>

            <div className="space-y-2 max-h-56 overflow-y-auto">
              {candidates.map((cand, idx) => (
                <div key={idx} className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-start justify-between">
                  <div className="space-y-1">
                    <span className="text-xs font-bold text-slate-800">{cand.name}</span>
                    <p className="text-[11px] text-slate-500 line-clamp-2">
                      {cand.resume_text}
                    </p>
                  </div>
                  <button 
                    onClick={() => handleRemoveCandidate(idx)}
                    className="text-slate-400 hover:text-red-500 text-xs ml-2"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>

            {/* Quick Add Form */}
            <form onSubmit={handleAddCandidate} className="pt-2 border-t border-slate-100 space-y-2">
              <input 
                type="text" 
                placeholder="Candidate Full Name..." 
                value={newCandName} 
                onChange={(e) => setNewCandName(e.target.value)}
                className="w-full text-xs border border-slate-300 rounded-lg p-2 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
              <textarea 
                rows="2" 
                placeholder="Resume text / key skills..." 
                value={newCandText} 
                onChange={(e) => setNewCandText(e.target.value)}
                className="w-full text-xs border border-slate-300 rounded-lg p-2 font-mono focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
              <button 
                type="submit" 
                className="w-full py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold"
              >
                + Add Candidate to Batch
              </button>
            </form>

            <button
              onClick={handleRunRanking}
              disabled={loading}
              className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold shadow-sm transition-all flex items-center justify-center space-x-2 disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  <span>Evaluating Candidates in Parallel...</span>
                </>
              ) : (
                <>
                  <Trophy size={16} />
                  <span>Run Candidate Comparison & Ranking</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Column: Ranked Leaderboard */}
        <div className="lg:col-span-7 space-y-4">
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 flex items-center space-x-2">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          {!rankingResult && !error && (
            <div className="bg-white rounded-xl border border-slate-200 p-12 text-center shadow-sm">
              <Trophy size={40} className="mx-auto text-slate-300 mb-3" />
              <h4 className="text-sm font-semibold text-slate-700">No Ranking Computed Yet</h4>
              <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
                Click "Run Candidate Comparison & Ranking" to benchmark all candidates against the target JD requirements.
              </p>
            </div>
          )}

          {rankingResult && (
            <div className="space-y-4">
              {/* Leaderboard Summary Banner */}
              <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm flex items-center justify-between">
                <div>
                  <span className="text-[11px] font-bold uppercase text-slate-500">Target Role</span>
                  <div className="text-sm font-bold text-slate-900">{rankingResult.job_title}</div>
                </div>
                <div className="text-right">
                  <span className="text-[11px] font-bold uppercase text-slate-500">Total Evaluated</span>
                  <div className="text-sm font-bold text-indigo-600">{rankingResult.total_evaluated} Candidates</div>
                </div>
              </div>

              {/* Ranked Candidate Cards */}
              <div className="space-y-3">
                {rankingResult.ranked_candidates.map((cand) => {
                  const isTop = cand.rank === 1;
                  const isStrong = cand.match_tier === 'Strong Match';
                  const isGood = cand.match_tier === 'Good Match';
                  return (
                    <div 
                      key={cand.candidate_id} 
                      className={`bg-white rounded-xl border p-5 shadow-sm space-y-3 transition-all ${
                        isTop ? 'border-indigo-400 ring-2 ring-indigo-100' : 'border-slate-200'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center font-extrabold text-xs ${
                            isTop ? 'bg-amber-400 text-slate-900 shadow' : 'bg-slate-100 text-slate-700'
                          }`}>
                            #{cand.rank}
                          </div>
                          <div>
                            <span className="text-sm font-bold text-slate-900">{cand.name}</span>
                            <div className="text-[11px] text-slate-400">
                              {cand.total_detected_skills} detected competencies
                            </div>
                          </div>
                        </div>

                        <div className="text-right">
                          <div className="text-lg font-extrabold text-slate-900">{cand.match_score}%</div>
                          <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                            isStrong ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' :
                            isGood ? 'bg-indigo-100 text-indigo-800 border border-indigo-300' :
                            'bg-slate-100 text-slate-700 border border-slate-300'
                          }`}>
                            {cand.match_tier}
                          </span>
                        </div>
                      </div>

                      {/* Skills Tags */}
                      <div className="pt-2 border-t border-slate-100 grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-[11px] font-semibold text-emerald-700 block mb-1">
                            Matched Required Skills ({cand.matched_skills.length})
                          </span>
                          <div className="flex flex-wrap gap-1">
                            {cand.matched_skills.map((s) => (
                              <span key={s} className="bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.5 rounded text-[10px] font-medium">
                                {s}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div>
                          <span className="text-[11px] font-semibold text-amber-700 block mb-1">
                            Missing Skills ({cand.missing_skills.length})
                          </span>
                          <div className="flex flex-wrap gap-1">
                            {cand.missing_skills.length > 0 ? (
                              cand.missing_skills.map((s) => (
                                <span key={s} className="bg-amber-50 text-amber-800 border border-amber-200 px-1.5 py-0.5 rounded text-[10px] font-medium">
                                  {s}
                                </span>
                              ))
                            ) : (
                              <span className="text-[11px] text-slate-400">None missing</span>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Hiring Rationale */}
                      <div className="p-2.5 bg-slate-50 rounded-lg text-xs text-slate-700 leading-relaxed border border-slate-100">
                        <strong>Hiring Rationale:</strong> {cand.hiring_rationale}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
