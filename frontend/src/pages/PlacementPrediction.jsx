import React, { useState, useEffect } from 'react';
import { 
  Award, 
  CheckCircle2, 
  AlertCircle, 
  TrendingUp, 
  BookOpen, 
  Sparkles, 
  Compass, 
  Briefcase, 
  FileCheck,
  ShieldCheck,
  Loader2
} from 'lucide-react';
import { predictPlacementReadiness } from '../api/client';

export default function PlacementPrediction({ resumeData, setActiveTab }) {
  const [formData, setFormData] = useState({
    name: 'Student Candidate',
    branch: 'Computer Science and Engineering',
    cgpa: 7.8,
    aptitude_score: 72,
    projects_count: 2,
    internships_count: 0,
    communication_rating: 3.5,
    certifications_count: 1,
  });

  const [skillsList, setSkillsList] = useState([]);
  const [skillInput, setSkillInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Auto-populate detected skills if available from resume analysis
  useEffect(() => {
    if (resumeData && resumeData.extracted_skills && resumeData.extracted_skills.length > 0) {
      setSkillsList(resumeData.extracted_skills);
      if (resumeData.contact_info?.email) {
        setFormData(prev => ({ ...prev, name: 'Alex Rivera' }));
      }
    } else {
      setSkillsList(['python', 'sql', 'git', 'fastapi', 'javascript']);
    }
  }, [resumeData]);

  const handleAddSkill = (e) => {
    e.preventDefault();
    if (skillInput.trim() && !skillsList.includes(skillInput.trim().toLowerCase())) {
      setSkillsList([...skillsList, skillInput.trim().toLowerCase()]);
      setSkillInput('');
    }
  };

  const handleRemoveSkill = (skill) => {
    setSkillsList(skillsList.filter(s => s !== skill));
  };

  const handleRunPrediction = async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        name: formData.name,
        branch: formData.branch,
        cgpa: parseFloat(formData.cgpa),
        technical_skills: skillsList,
        aptitude_score: parseFloat(formData.aptitude_score),
        projects_count: parseInt(formData.projects_count, 10),
        internships_count: parseInt(formData.internships_count, 10),
        communication_rating: parseFloat(formData.communication_rating),
        certifications_count: parseInt(formData.certifications_count, 10),
      };
      const res = await predictPlacementReadiness(payload);
      setResult(res);
    } catch (err) {
      setError(err.message || 'Failed to calculate placement readiness');
    } finally {
      setLoading(false);
    }
  };

  // Run automatically on first mount
  useEffect(() => {
    handleRunPrediction();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
            Milestone 2 • Points 4 & 10
          </span>
          <span className="text-xs text-slate-400">|</span>
          <span className="text-xs text-slate-500 font-medium">Predictive Intelligence</span>
        </div>
        <h2 className="text-xl font-bold text-slate-900 mt-1">Placement Readiness & Profile Estimation</h2>
        <p className="text-xs text-slate-600 mt-1">
          Multi-dimensional AI assessment evaluating academics, technical toolkit, aptitude, projects, and interview articulation.
        </p>
      </div>

      {/* Main Grid: Form Inputs + Results */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Profile Controls */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
            <h3 className="text-xs font-bold uppercase text-slate-500 tracking-wider flex items-center space-x-2">
              <Compass size={15} className="text-indigo-600" />
              <span>Candidate Placement Parameters</span>
            </h3>

            {/* CGPA Slider */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <label className="font-semibold text-slate-700">Cumulative GPA (CGPA)</label>
                <span className="font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                  {formData.cgpa} / 10.0
                </span>
              </div>
              <input 
                type="range" 
                min="5.0" 
                max="10.0" 
                step="0.1" 
                value={formData.cgpa} 
                onChange={(e) => setFormData({ ...formData, cgpa: e.target.value })}
                className="w-full accent-indigo-600 cursor-pointer"
              />
            </div>

            {/* Aptitude Score */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <label className="font-semibold text-slate-700">Online Aptitude Score (%)</label>
                <span className="font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                  {formData.aptitude_score}%
                </span>
              </div>
              <input 
                type="range" 
                min="20" 
                max="100" 
                step="1" 
                value={formData.aptitude_score} 
                onChange={(e) => setFormData({ ...formData, aptitude_score: e.target.value })}
                className="w-full accent-indigo-600 cursor-pointer"
              />
            </div>

            {/* Projects & Internships in 2 cols */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Completed Projects</label>
                <select 
                  value={formData.projects_count} 
                  onChange={(e) => setFormData({ ...formData, projects_count: e.target.value })}
                  className="w-full text-xs border border-slate-300 rounded-lg p-2 bg-slate-50 focus:bg-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="0">0 Projects</option>
                  <option value="1">1 Project</option>
                  <option value="2">2 Projects</option>
                  <option value="3">3+ Projects</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Industry Internships</label>
                <select 
                  value={formData.internships_count} 
                  onChange={(e) => setFormData({ ...formData, internships_count: e.target.value })}
                  className="w-full text-xs border border-slate-300 rounded-lg p-2 bg-slate-50 focus:bg-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="0">None</option>
                  <option value="1">1 Internship</option>
                  <option value="2">2+ Internships</option>
                </select>
              </div>
            </div>

            {/* Communication Rating */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <label className="font-semibold text-slate-700">Communication Rating</label>
                <span className="font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                  {formData.communication_rating} / 5.0
                </span>
              </div>
              <input 
                type="range" 
                min="1.0" 
                max="5.0" 
                step="0.5" 
                value={formData.communication_rating} 
                onChange={(e) => setFormData({ ...formData, communication_rating: e.target.value })}
                className="w-full accent-indigo-600 cursor-pointer"
              />
            </div>

            {/* Technical Skills Tags */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Technical Skills ({skillsList.length} registered)
              </label>
              <div className="flex flex-wrap gap-1.5 mb-2 max-h-28 overflow-y-auto p-1.5 bg-slate-50 rounded-lg border border-slate-200">
                {skillsList.map((skill) => (
                  <span key={skill} className="inline-flex items-center space-x-1 bg-white text-slate-800 border border-slate-300 px-2 py-0.5 rounded text-[11px]">
                    <span>{skill}</span>
                    <button 
                      type="button" 
                      onClick={() => handleRemoveSkill(skill)}
                      className="text-slate-400 hover:text-red-500 ml-1 text-xs"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
              <form onSubmit={handleAddSkill} className="flex space-x-2">
                <input 
                  type="text" 
                  value={skillInput} 
                  onChange={(e) => setSkillInput(e.target.value)} 
                  placeholder="Add skill (e.g., docker, aws)..." 
                  className="flex-1 text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
                <button 
                  type="submit" 
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-medium"
                >
                  Add
                </button>
              </form>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleRunPrediction}
              disabled={loading}
              className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold shadow-sm transition-all flex items-center justify-center space-x-2 disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  <span>Computing Multi-Factor Readiness...</span>
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  <span>Recalculate Readiness Estimation</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Column: Prediction Score Cards & Dimensions */}
        <div className="lg:col-span-7 space-y-4">
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 flex items-center space-x-2">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          {result && (
            <>
              {/* Score Gauge Banner */}
              <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-xl p-6 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-6">
                <div className="space-y-1 text-center sm:text-left">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-300">
                    Overall Placement Readiness
                  </span>
                  <div className="text-3xl font-extrabold flex items-baseline space-x-2 justify-center sm:justify-start">
                    <span>{result.readiness_score}%</span>
                    <span className="text-sm font-medium text-slate-400">estimated index</span>
                  </div>
                  <div className="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-500/30 text-indigo-200 border border-indigo-400/30">
                    {result.readiness_band}
                  </div>
                </div>

                {/* Circular Gauge Visual */}
                <div className="relative w-28 h-28 flex items-center justify-center shrink-0">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="40" stroke="currentColor" strokeWidth="10" className="text-slate-800" fill="transparent" />
                    <circle 
                      cx="50" 
                      cy="50" 
                      r="40" 
                      stroke="currentColor" 
                      strokeWidth="10" 
                      strokeDasharray="251.2"
                      strokeDashoffset={251.2 - (251.2 * result.readiness_score) / 100}
                      strokeLinecap="round"
                      className="text-indigo-400 transition-all duration-700" 
                      fill="transparent" 
                    />
                  </svg>
                  <span className="absolute font-extrabold text-lg text-white">
                    {result.readiness_score}%
                  </span>
                </div>
              </div>

              {/* 6 Dimension Status Cards */}
              <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <h3 className="text-xs font-bold uppercase text-slate-500 tracking-wider flex items-center space-x-2">
                  <Award size={15} className="text-indigo-600" />
                  <span>Dimensional Readiness Breakdown</span>
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {result.dimensions.map((dim, idx) => {
                    const isGood = dim.status === 'Good';
                    const isMod = dim.status === 'Moderate';
                    return (
                      <div key={idx} className="p-3 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-semibold text-slate-800">{dim.category}</span>
                          <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                            isGood ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' :
                            isMod ? 'bg-amber-100 text-amber-800 border border-amber-300' :
                            'bg-red-100 text-red-800 border border-red-300'
                          }`}>
                            {dim.status}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-600 leading-snug">
                          {dim.details}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Strengths & Action Plan */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Strengths */}
                <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-2">
                  <h4 className="text-xs font-bold uppercase text-emerald-700 tracking-wider flex items-center space-x-1.5">
                    <CheckCircle2 size={15} className="text-emerald-600" />
                    <span>Identified Strengths</span>
                  </h4>
                  <ul className="space-y-1.5 text-xs text-slate-700 list-disc list-inside">
                    {result.strengths.map((str, i) => (
                      <li key={i}>{str}</li>
                    ))}
                  </ul>
                </div>

                {/* 30-Day Strategy */}
                <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-2">
                  <h4 className="text-xs font-bold uppercase text-indigo-700 tracking-wider flex items-center space-x-1.5">
                    <TrendingUp size={15} className="text-indigo-600" />
                    <span>30-Day Prep Strategy</span>
                  </h4>
                  <ul className="space-y-1.5 text-xs text-slate-700 list-disc list-inside">
                    {result.actionable_prep_strategy.map((act, i) => (
                      <li key={i}>{act}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Ethical Disclaimer */}
              <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-start space-x-2">
                <ShieldCheck size={16} className="shrink-0 text-amber-600 mt-0.5" />
                <p className="leading-relaxed">
                  <strong>Academic Disclaimer:</strong> {result.disclaimer}
                </p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
