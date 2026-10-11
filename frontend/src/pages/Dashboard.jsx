import React, { useEffect, useState } from 'react';
import { 
  FileText, 
  Target, 
  GitCompare, 
  ArrowRight, 
  Activity, 
  CheckCircle2, 
  Clock, 
  Database 
} from 'lucide-react';
import { fetchDashboardStats } from '../api/client';

export default function Dashboard({ setActiveTab }) {
  const [stats, setStats] = useState({
    total_analyses: 0,
    average_similarity_score: 0.0,
    recent_analyses: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  async function loadStats() {
    try {
      setLoading(true);
      const data = await fetchDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="max-w-3xl">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-200 mb-3">
            Milestone 1 — Real Functionality MVP
          </span>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            Welcome to CareerFit
          </h2>
          <p className="mt-2 text-sm text-slate-600 leading-relaxed">
            CareerFit is an AI-based career intelligence platform engineered for final-year project demonstration.
            This initial ~30% milestone implements genuine <strong>PDF resume parsing with pypdf</strong>, 
            <strong>rule-based skill extraction</strong>, <strong>TF-IDF cosine similarity job matching</strong>, and 
            <strong>transparent skill gap analysis</strong> backed by SQLite persistence.
          </p>
        </div>
      </div>

      {/* Real Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Analyses Completed</span>
            <div className="w-9 h-9 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <Database size={18} />
            </div>
          </div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '...' : stats.total_analyses}
          </div>
          <p className="mt-1 text-xs text-slate-500">Persisted in local SQLite database</p>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Avg Baseline Similarity</span>
            <div className="w-9 h-9 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <Activity size={18} />
            </div>
          </div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '...' : `${stats.average_similarity_score}%`}
          </div>
          <p className="mt-1 text-xs text-slate-500">TF-IDF Cosine Similarity index</p>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Operational Modules</span>
            <div className="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <CheckCircle2 size={18} />
            </div>
          </div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            3 / 3
          </div>
          <p className="mt-1 text-xs text-slate-500">Resume, Matching, & Skill Gap active</p>
        </div>
      </div>

      {/* Prioritized 3 Modules Navigation Grid */}
      <div>
        <h3 className="text-base font-bold text-slate-900 mb-3">Core Modules for Review Demonstration</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* Module 1 */}
          <div 
            onClick={() => setActiveTab('resume')}
            className="group bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
          >
            <div>
              <div className="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
                <FileText size={20} />
              </div>
              <h4 className="font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors">
                1. Resume Analyzer
              </h4>
              <p className="mt-1 text-xs text-slate-600 leading-relaxed">
                Upload candidate PDF. Validates format and size, extracts selectable text via pypdf, and previews detected skills.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 flex items-center text-xs font-medium text-indigo-600">
              <span>Open Analyzer</span>
              <ArrowRight size={14} className="ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Module 2 */}
          <div 
            onClick={() => setActiveTab('matching')}
            className="group bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
          >
            <div>
              <div className="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
                <Target size={20} />
              </div>
              <h4 className="font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors">
                2. Job Matching
              </h4>
              <p className="mt-1 text-xs text-slate-600 leading-relaxed">
                Paste job description. Calculates TF-IDF cosine similarity baseline score (0-100) and displays matched overlapping skills.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 flex items-center text-xs font-medium text-indigo-600">
              <span>Run Job Match</span>
              <ArrowRight size={14} className="ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Module 3 */}
          <div 
            onClick={() => setActiveTab('skillgap')}
            className="group bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
          >
            <div>
              <div className="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
                <GitCompare size={20} />
              </div>
              <h4 className="font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors">
                3. Skill Gap Analysis
              </h4>
              <p className="mt-1 text-xs text-slate-600 leading-relaxed">
                Highlights potential missing skills required by the job. Delivers practical, ethical upskilling advice without fabricating experience.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 flex items-center text-xs font-medium text-indigo-600">
              <span>Inspect Skill Gaps</span>
              <ArrowRight size={14} className="ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity Table (Real SQLite Data) */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Clock size={16} className="text-slate-500" />
            <h3 className="text-sm font-bold text-slate-900">Recent SQLite Activity</h3>
          </div>
          <button
            onClick={() => setActiveTab('history')}
            className="text-xs font-medium text-indigo-600 hover:underline"
          >
            View full history →
          </button>
        </div>

        {loading ? (
          <div className="py-6 text-center text-sm text-slate-400">Loading activity...</div>
        ) : stats.recent_analyses.length === 0 ? (
          <div className="py-8 text-center text-slate-500 text-xs">
            No analyses recorded yet. Upload a resume and run a match to generate real database entries.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500">
                  <th className="py-2.5 font-medium">Timestamp</th>
                  <th className="py-2.5 font-medium">Resume File</th>
                  <th className="py-2.5 font-medium">Target Role</th>
                  <th className="py-2.5 font-medium">Baseline Score</th>
                  <th className="py-2.5 font-medium">Matched / Missing</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {stats.recent_analyses.map((rec) => (
                  <tr key={rec.id} className="hover:bg-slate-50">
                    <td className="py-2.5 text-slate-500">{rec.timestamp}</td>
                    <td className="py-2.5 font-medium text-slate-800">{rec.resume_filename}</td>
                    <td className="py-2.5 text-slate-600">{rec.job_title}</td>
                    <td className="py-2.5">
                      <span className="font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                        {rec.similarity_score}%
                      </span>
                    </td>
                    <td className="py-2.5 text-slate-600">
                      <span className="text-emerald-700">{rec.matched_count} matched</span> • <span className="text-amber-700">{rec.missing_count} missing</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
