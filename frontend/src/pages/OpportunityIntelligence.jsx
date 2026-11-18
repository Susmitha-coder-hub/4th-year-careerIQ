import React, { useState, useEffect } from 'react';
import { 
  Bell, 
  Calendar, 
  Clock, 
  CheckCircle2, 
  AlertTriangle, 
  Briefcase, 
  MapPin, 
  GraduationCap, 
  ChevronRight, 
  BookOpen, 
  Sparkles, 
  ShieldCheck,
  X,
  Loader2
} from 'lucide-react';
import { fetchOpportunities, checkOpportunityEligibility, fetchInterviewPrepGuide } from '../api/client';

export default function OpportunityIntelligence({ resumeData, setActiveTab }) {
  const [cgpa, setCgpa] = useState(7.8);
  const [branch, setBranch] = useState('Computer Science and Engineering');
  const [filterType, setFilterType] = useState('all'); // 'all', 'eligible', 'urgent'
  
  const [opportunities, setOpportunities] = useState([]);
  const [eligibleCount, setEligibleCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Prep guide modal state
  const [activePrepModal, setActivePrepModal] = useState(null);
  const [prepGuide, setPrepGuide] = useState(null);
  const [loadingPrep, setLoadingPrep] = useState(false);

  const loadOpportunities = async () => {
    setLoading(true);
    setError(null);
    try {
      const skills = resumeData?.extracted_skills || ['python', 'sql', 'git'];
      const res = await checkOpportunityEligibility({
        cgpa: parseFloat(cgpa),
        branch,
        skills
      });
      setOpportunities(res.opportunities || []);
      setEligibleCount(res.eligible_count || 0);
    } catch (err) {
      setError(err.message || 'Failed to load opportunities');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOpportunities();
  }, [cgpa, branch]);

  const handleOpenPrepModal = async (oppId) => {
    setActivePrepModal(oppId);
    setLoadingPrep(true);
    setPrepGuide(null);
    try {
      const guide = await fetchInterviewPrepGuide(oppId);
      setPrepGuide(guide);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingPrep(false);
    }
  };

  const filteredOpps = opportunities.filter((item) => {
    if (filterType === 'eligible') return item.is_eligible;
    if (filterType === 'urgent') return item.urgency_status.includes('Urgent') || item.urgency_status.includes('Assessment');
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
            Milestone 2 • Points 11–14
          </span>
          <span className="text-xs text-slate-400">|</span>
          <span className="text-xs text-slate-500 font-medium">Opportunity Intelligence & Reminders</span>
        </div>
        <h2 className="text-xl font-bold text-slate-900 mt-1">Placement Drives & Proactive Opportunity Intelligence</h2>
        <p className="text-xs text-slate-600 mt-1">
          Detect active campus drives, verify academic eligibility, track test & interview deadlines, and generate 48-hour revision guides.
        </p>
      </div>

      {/* Top Profile Eligibility Filter Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <div className="flex items-center space-x-1.5 text-xs text-slate-700">
            <GraduationCap size={16} className="text-indigo-600" />
            <span className="font-semibold">Your Profile:</span>
          </div>

          <div className="flex items-center space-x-1 bg-slate-50 px-2 py-1 rounded-lg border border-slate-200 text-xs">
            <span className="text-slate-500">CGPA:</span>
            <input 
              type="number" 
              step="0.1" 
              min="0" 
              max="10" 
              value={cgpa} 
              onChange={(e) => setCgpa(e.target.value)}
              className="w-14 font-bold text-indigo-600 bg-transparent focus:outline-none"
            />
          </div>

          <div className="flex items-center space-x-1 bg-slate-50 px-2 py-1 rounded-lg border border-slate-200 text-xs">
            <span className="text-slate-500">Branch:</span>
            <select 
              value={branch} 
              onChange={(e) => setBranch(e.target.value)}
              className="text-xs font-semibold text-slate-800 bg-transparent focus:outline-none"
            >
              <option value="Computer Science and Engineering">CSE</option>
              <option value="Information Technology">IT</option>
              <option value="Electronics and Communication">ECE</option>
              <option value="Electrical">EEE</option>
              <option value="Mechanical">Mechanical</option>
            </select>
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center space-x-1.5 self-end md:self-auto">
          <button
            onClick={() => setFilterType('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              filterType === 'all' 
                ? 'bg-slate-900 text-white' 
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            All ({opportunities.length})
          </button>
          <button
            onClick={() => setFilterType('eligible')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              filterType === 'eligible' 
                ? 'bg-emerald-600 text-white' 
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            Eligible Only ({eligibleCount})
          </button>
          <button
            onClick={() => setFilterType('urgent')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              filterType === 'urgent' 
                ? 'bg-amber-600 text-white' 
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            Urgent Deadlines
          </button>
        </div>
      </div>

      {/* Opportunity Cards List */}
      {loading ? (
        <div className="p-12 text-center text-slate-500 bg-white rounded-xl border border-slate-200 space-y-2">
          <Loader2 size={24} className="animate-spin mx-auto text-indigo-600" />
          <p className="text-xs">Evaluating placement intelligence & deadlines...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredOpps.map((item) => {
            const opp = item.opportunity;
            const isEligible = item.is_eligible;
            const isUrgent = item.urgency_status.includes('Urgent');
            const isTest = item.urgency_status.includes('Assessment');

            return (
              <div 
                key={opp.id} 
                className={`bg-white rounded-xl border p-5 shadow-sm space-y-4 transition-all hover:shadow-md ${
                  isEligible ? 'border-slate-200' : 'border-slate-200 opacity-75'
                }`}
              >
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div className="space-y-0.5">
                    <div className="flex items-center space-x-2">
                      <span className="text-base font-bold text-slate-900">{opp.company}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-slate-100 text-slate-700">
                        {opp.job_type}
                      </span>
                    </div>
                    <div className="text-xs text-indigo-600 font-semibold">{opp.role}</div>
                  </div>

                  {/* Urgency Badge */}
                  <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-bold ${
                    isUrgent ? 'bg-red-100 text-red-800 border border-red-300 animate-pulse' :
                    isTest ? 'bg-amber-100 text-amber-800 border border-amber-300' :
                    'bg-emerald-100 text-emerald-800 border border-emerald-300'
                  }`}>
                    {item.urgency_status}
                  </span>
                </div>

                {/* Deadlines & Criteria Details */}
                <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-3 rounded-lg border border-slate-100">
                  <div className="flex items-center space-x-1.5 text-slate-600">
                    <Calendar size={13} className="text-slate-400 shrink-0" />
                    <span><strong>Deadline:</strong> {opp.registration_deadline}</span>
                  </div>
                  {opp.test_date && (
                    <div className="flex items-center space-x-1.5 text-slate-600">
                      <Clock size={13} className="text-slate-400 shrink-0" />
                      <span><strong>Test:</strong> {opp.test_date}</span>
                    </div>
                  )}
                  <div className="flex items-center space-x-1.5 text-slate-600">
                    <GraduationCap size={13} className="text-slate-400 shrink-0" />
                    <span><strong>Min CGPA:</strong> {opp.min_cgpa}</span>
                  </div>
                  {opp.package_lpa && (
                    <div className="flex items-center space-x-1.5 text-slate-600">
                      <Briefcase size={13} className="text-slate-400 shrink-0" />
                      <span><strong>Package:</strong> {opp.package_lpa}</span>
                    </div>
                  )}
                </div>

                {/* Skills Overlap */}
                <div className="space-y-1">
                  <div className="flex justify-between items-center text-[11px]">
                    <span className="text-slate-500 font-medium">Skill Alignment</span>
                    <span className="font-bold text-indigo-600">{item.skill_match_percentage}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                    <div 
                      className="bg-indigo-600 h-1.5 rounded-full" 
                      style={{ width: `${item.skill_match_percentage}%` }}
                    />
                  </div>
                </div>

                {/* Recommendation Alert Box */}
                <div className={`p-2.5 rounded-lg text-xs leading-relaxed ${
                  isEligible ? 'bg-emerald-50 text-emerald-900 border border-emerald-200' : 'bg-red-50 text-red-800 border border-red-200'
                }`}>
                  {item.recommendation}
                </div>

                {/* Action Button: Detect -> Alert -> Explain -> Prepare */}
                <button
                  onClick={() => handleOpenPrepModal(opp.id)}
                  className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors"
                >
                  <BookOpen size={14} />
                  <span>Prepare for Assessment & Interview</span>
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* 48-Hour Interview & Assessment Preparation Guide Modal */}
      {activePrepModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-xl space-y-5 my-8">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center space-x-2">
                <Sparkles size={18} className="text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900">
                  {prepGuide ? `${prepGuide.company} — 48-Hour Assessment Prep Pack` : 'Generating Revision Guide...'}
                </h3>
              </div>
              <button 
                onClick={() => setActivePrepModal(null)}
                className="text-slate-400 hover:text-slate-700"
              >
                <X size={20} />
              </button>
            </div>

            {loadingPrep || !prepGuide ? (
              <div className="py-12 text-center text-slate-500 space-y-2">
                <Loader2 size={24} className="animate-spin mx-auto text-indigo-600" />
                <p className="text-xs">Compiling high-yield revision topics and coding patterns...</p>
              </div>
            ) : (
              <div className="space-y-4 text-xs max-h-[70vh] overflow-y-auto pr-1">
                {/* 1. Core Technical Focus Areas */}
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                  <span className="font-bold text-slate-800 block">📌 Core Technical Topics to Revise:</span>
                  <ul className="space-y-1 text-slate-600 list-disc list-inside">
                    {prepGuide.core_technical_topics.map((t, i) => (
                      <li key={i}>{t}</li>
                    ))}
                  </ul>
                </div>

                {/* 2. Sample Coding Patterns */}
                <div className="p-3 bg-indigo-50/50 rounded-xl border border-indigo-100 space-y-1.5">
                  <span className="font-bold text-indigo-950 block">💻 High-Probability Coding Problems:</span>
                  <ul className="space-y-1 text-slate-700 list-disc list-inside">
                    {prepGuide.sample_coding_questions.map((q, i) => (
                      <li key={i}>{q}</li>
                    ))}
                  </ul>
                </div>

                {/* 3. 48-Hour Schedule */}
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                  <span className="font-bold text-slate-800 block">⏱️ 48-Hour Hourly Revision Schedule:</span>
                  <div className="space-y-1 text-slate-600">
                    {prepGuide.revision_schedule_48h.map((s, i) => (
                      <div key={i} className="p-1.5 bg-white rounded border border-slate-100 text-[11px]">
                        {s}
                      </div>
                    ))}
                  </div>
                </div>

                {/* 4. Behavioral Tips */}
                <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 space-y-1">
                  <span className="font-bold text-amber-900 block">🤝 Panel & Behavioral Tips:</span>
                  <ul className="space-y-1 text-amber-800 list-disc list-inside">
                    {prepGuide.hr_behavioral_tips.map((h, i) => (
                      <li key={i}>{h}</li>
                    ))}
                  </ul>
                </div>

                <button
                  onClick={() => setActivePrepModal(null)}
                  className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold text-xs transition-colors"
                >
                  Done, Let's Revise!
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
