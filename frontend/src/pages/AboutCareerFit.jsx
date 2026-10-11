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
        <h2 className="text-xl font-bold text-slate-900">About CareerFit & Milestone 1 Progress</h2>
        <p className="text-xs text-slate-600 mt-1">
          Academic project specification, implementation status, and technical limitations for project review.
        </p>
      </div>

      {/* Progress Breakdown Card */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
            <Layers size={16} className="text-indigo-600" />
            <span>Scope Status: Milestone 1 (~30% Planned Scope)</span>
          </h3>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Demonstrable & Tested
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* Implemented */}
          <div className="p-4 bg-emerald-50/50 rounded-xl border border-emerald-100 space-y-2">
            <span className="font-bold text-emerald-900 flex items-center space-x-1.5">
              <CheckCircle2 size={15} className="text-emerald-600" />
              <span>Implemented & Tested (Milestone 1)</span>
            </span>
            <ul className="space-y-1.5 text-slate-700 list-disc list-inside">
              <li><strong>Module 1:</strong> PDF upload & validation (pypdf, size limit, error handling).</li>
              <li><strong>Module 2:</strong> Job description parser with configurable skill ontology.</li>
              <li><strong>Module 3:</strong> TF-IDF n-gram vectorization & Cosine Similarity (0-100 score).</li>
              <li><strong>Module 4:</strong> Skill Gap Analysis with categorized missing skills and upskilling advice.</li>
              <li><strong>Module 5:</strong> SQLite persistence and record deletion via FastAPI REST endpoints.</li>
              <li><strong>Testing:</strong> Automated pytest suite covering validation, bounds, and extraction.</li>
            </ul>
          </div>

          {/* Out of Scope */}
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="font-bold text-slate-700 flex items-center space-x-1.5">
              <CircleDashed size={15} className="text-slate-400" />
              <span>Out of Scope (Subsequent Milestones)</span>
            </span>
            <ul className="space-y-1.5 text-slate-500 list-disc list-inside">
              <li>Automated placement inbox monitoring & email polling.</li>
              <li>Campus placement readiness prediction model.</li>
              <li>Multi-resume recruiter ranking algorithms.</li>
              <li>Generative LLM resume re-writing or automated tailoring.</li>
              <li>External live web job board scrapers.</li>
              <li>Production user authentication (JWT/OAuth).</li>
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
