import React from 'react';
import { 
  GitCompare, 
  CheckCircle2, 
  AlertCircle, 
  Lightbulb, 
  ShieldAlert, 
  ArrowRight,
  TrendingUp,
  Bookmark
} from 'lucide-react';

export default function SkillGapAnalysis({ matchingResult, setActiveTab }) {
  if (!matchingResult) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Module 3 — Skill Gap Analysis</h2>
          <p className="text-xs text-slate-600 mt-1">
            Analyze skill alignment between resume credentials and target job demands.
          </p>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-12 text-center shadow-sm max-w-xl mx-auto">
          <GitCompare size={40} className="mx-auto text-slate-300 mb-3" />
          <h4 className="text-sm font-semibold text-slate-700">No Match Data Available</h4>
          <p className="text-xs text-slate-400 mt-1">
            Skill gap analysis requires an active comparison. Run a match in Module 2 to populate these actionable insights.
          </p>
          <button
            onClick={() => setActiveTab('matching')}
            className="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold shadow-sm transition-all"
          >
            Go to Job Matching
          </button>
        </div>
      </div>
    );
  }

  const gapData = matchingResult.gap_analysis || {};
  const summary = gapData.summary || {};
  const suggestions = gapData.actionable_suggestions || [];
  const categorizedMissing = gapData.categorized_missing || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Module 3 — Skill Gap Analysis</h2>
        <p className="text-xs text-slate-600 mt-1">
          Detailed diagnosis of profile qualifications versus target job requirements with ethical upskilling recommendations.
        </p>
      </div>

      {/* 4 Summary Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm text-center">
          <span className="text-[11px] font-semibold uppercase text-slate-500">Job Demanded Skills</span>
          <div className="mt-1 text-2xl font-bold text-slate-800">
            {summary.total_job_skills ?? matchingResult.job_skills.length}
          </div>
          <span className="text-[10px] text-slate-400">Total requirements</span>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm text-center">
          <span className="text-[11px] font-semibold uppercase text-slate-500">Verified Matched</span>
          <div className="mt-1 text-2xl font-bold text-emerald-600">
            {summary.matched_count ?? matchingResult.matched_skills.length}
          </div>
          <span className="text-[10px] text-slate-400">Found in resume text</span>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm text-center">
          <span className="text-[11px] font-semibold uppercase text-slate-500">Identified Gaps</span>
          <div className="mt-1 text-2xl font-bold text-amber-600">
            {summary.missing_count ?? matchingResult.missing_skills.length}
          </div>
          <span className="text-[10px] text-slate-400">Skills not detected</span>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm text-center">
          <span className="text-[11px] font-semibold uppercase text-slate-500">Coverage Percentage</span>
          <div className="mt-1 text-2xl font-bold text-indigo-600">
            {summary.coverage_percentage ?? matchingResult.skill_coverage_percentage}%
          </div>
          <span className="text-[10px] text-slate-400">Qualification overlap</span>
        </div>
      </div>

      {/* Categorized Gap Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Missing Skills by Category */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
          <h3 className="text-xs font-bold uppercase text-slate-500 tracking-wider flex items-center space-x-2">
            <AlertCircle size={15} className="text-amber-600" />
            <span>Missing Skills Grouped by Domain</span>
          </h3>

          {Object.keys(categorizedMissing).length === 0 ? (
            <p className="text-xs text-emerald-600 font-medium py-3">
              🎉 Excellent alignment! No missing skills recognized against this target job description.
            </p>
          ) : (
            <div className="space-y-3">
              {Object.entries(categorizedMissing).map(([cat, skills]) => (
                <div key={cat} className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-slate-800 block mb-1.5">{cat}</span>
                  <div className="flex flex-wrap gap-1.5">
                    {skills.map((s) => (
                      <span key={s} className="bg-amber-100/70 text-amber-900 border border-amber-200 px-2 py-0.5 rounded text-[11px] font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Ethical Academic Disclaimer Card */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold uppercase text-slate-500 tracking-wider flex items-center space-x-2 mb-2">
              <ShieldAlert size={15} className="text-indigo-600" />
              <span>Ethical Guidance Policy</span>
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              CareerFit strictly enforces academic integrity standards:
            </p>
            <ul className="mt-2 space-y-1.5 text-xs text-slate-600 list-disc list-inside">
              <li><strong>Do not fabricate:</strong> Never insert tools into your resume unless you have genuine hands-on competence.</li>
              <li><strong>Missing vs Undetected:</strong> A missing skill only indicates that the specific keyword was not located in your uploaded PDF text.</li>
              <li><strong>Targeted Bridging:</strong> Allocate 1–3 weeks to implement small sample projects demonstrating the tools before adding them.</li>
            </ul>
          </div>

          <div className="p-3 bg-indigo-50 border border-indigo-200 rounded-lg text-xs text-indigo-900 font-medium">
            💡 Pro-Tip: When preparing for viva questions, emphasize that CareerFit recommends project-based upskilling rather than misleading keyword stuffing.
          </div>
        </div>
      </div>

      {/* Practical Actionable Suggestions */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
          <Lightbulb size={16} className="text-amber-500" />
          <span>Practical Action Plan for Identified Gaps</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {suggestions.map((sug, idx) => (
            <div key={idx} className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800">{sug.skill}</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">
                  {sug.type}
                </span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                {sug.action || sug.message}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
