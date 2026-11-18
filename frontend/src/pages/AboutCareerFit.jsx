import React from 'react';
import { 
  CheckCircle2, 
  CircleDashed, 
  ShieldCheck, 
  Cpu, 
  Layers, 
  AlertTriangle 
} from 'lucide-react';

export default function AboutCareerFit() {
  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2 className="text-xl font-bold text-slate-900">About CareerFit & Implementation Progress</h2>
        <p className="text-xs text-slate-600 mt-1">
          Academic project specification, implementation status, and technical architecture for CSE final-year review.
        </p>
      </div>

      {/* Progress Breakdown Card */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
            <Layers size={16} className="text-indigo-600" />
            <span>Scope Status: Milestone 2 (~50-60% Planned Scope Completed)</span>
          </h3>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Verified & 16 Pytests Passing
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* Implemented */}
          <div className="p-4 bg-emerald-50/50 rounded-xl border border-emerald-100 space-y-2">
            <span className="font-bold text-emerald-900 flex items-center space-x-1.5">
              <CheckCircle2 size={15} className="text-emerald-600" />
              <span>Implemented & Tested (Milestones 1 & 2)</span>
            </span>
            <ul className="space-y-1.5 text-slate-700 list-disc list-inside">
              <li><strong>Module 1:</strong> PDF upload & validation (pypdf, size limit, error handling).</li>
              <li><strong>Module 2:</strong> Job description parser with configurable skill ontology.</li>
              <li><strong>Module 3:</strong> TF-IDF n-gram vectorization & Cosine Similarity (0-100 score).</li>
              <li><strong>Module 4:</strong> Skill Gap Analysis with curated courses & hands-on project roadmaps (Point 15).</li>
              <li><strong>Module 5:</strong> SQLite persistence and record deletion via FastAPI REST endpoints.</li>
              <li><strong>Module 6:</strong> Placement Readiness Prediction Engine (Points 4 & 10) evaluating 6 dimensions.</li>
              <li><strong>Module 7:</strong> Recruiter Multi-Resume Comparison & Leaderboard Ranking (Point 9).</li>
              <li><strong>Module 8:</strong> Opportunity Intelligence, eligibility check, & 48-Hour Prep Guides (Points 11–14).</li>
              <li><strong>Module 9:</strong> Universal AI Career Assistant Chatbot (Points 16 & 17).</li>
            </ul>
          </div>

          {/* Out of Scope */}
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="font-bold text-slate-700 flex items-center space-x-1.5">
              <CircleDashed size={15} className="text-slate-400" />
              <span>Remaining Scope (Milestone 3 / Final Viva)</span>
            </span>
            <ul className="space-y-1.5 text-slate-500 list-disc list-inside">
              <li>Live Gmail OAuth2 IMAP daemon integration (simulated via Opportunity Intelligence).</li>
              <li>External live job board scrapers (LinkedIn/Naukri).</li>
              <li>Fine-tuned BERT dual-encoder checkpoint integration.</li>
              <li>Multi-tenant enterprise role-based access control (RBAC).</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Methodology & Limitations */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
          <AlertTriangle size={16} className="text-amber-500" />
          <span>Technical Methodology & Known Limitations</span>
        </h3>

        <div className="space-y-3 text-xs text-slate-600 leading-relaxed">
          <p>
            <strong>1. Selectable Text vs Scanned Images:</strong> Resume text extraction relies on <code>pypdf</code> to parse standard selectable text streams. Image-based or flat-scanned PDFs will trigger a clear validation alert informing the user that OCR is not supported in this first milestone.
          </p>
          <p>
            <strong>2. Baseline TF-IDF vs Deep Semantic Understanding:</strong> The matching score evaluates statistical n-gram term frequencies and cosine distance. While reliable for detecting exact terminology, it does not infer complex semantic synonyms (e.g. recognizing that "Golang" is identical to "Go" unless configured in the taxonomy).
          </p>
          <p>
            <strong>3. Privacy by Design:</strong> CareerFit does not log or persist raw full resume text to SQLite. Only computed metadata, detected skills, matched status, and similarity scores are archived.
          </p>
        </div>
      </div>
    </div>
  );
}
