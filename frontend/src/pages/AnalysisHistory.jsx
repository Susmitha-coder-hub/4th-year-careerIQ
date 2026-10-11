import React, { useEffect, useState } from 'react';
import { 
  History, 
  Trash2, 
  Clock, 
  FileText, 
  AlertCircle, 
  RefreshCw 
} from 'lucide-react';
import { fetchAnalysisHistory, deleteAnalysisRecord } from '../api/client';

export default function AnalysisHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchAnalysisHistory();
      setHistory(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm(`Are you sure you want to delete analysis record #${id}?`)) {
      return;
    }

    try {
      setDeletingId(id);
      await deleteAnalysisRecord(id);
      setHistory(history.filter((h) => h.id !== id));
    } catch (err) {
      alert(`Error deleting record: ${err.message}`);
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Analysis History & Persistence</h2>
          <p className="text-xs text-slate-600 mt-1">
            Persisted analysis records stored in the local SQLite database.
          </p>
        </div>
        <button
          onClick={loadHistory}
          disabled={loading}
          className="flex items-center space-x-1 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
        >
          <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
          <span>Refresh</span>
        </button>
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-700 flex items-center space-x-2">
          <AlertCircle size={15} />
          <span>{error}</span>
        </div>
      )}

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-xs text-slate-400">Loading analysis records...</div>
        ) : history.length === 0 ? (
          <div className="p-12 text-center">
            <History size={40} className="mx-auto text-slate-300 mb-3" />
            <h4 className="text-sm font-semibold text-slate-700">No History Records Found</h4>
            <p className="text-xs text-slate-400 mt-1">
              Runs conducted in Module 2 with "Save to history" enabled will automatically log here.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                <tr>
                  <th className="py-3 px-4 font-semibold">ID</th>
                  <th className="py-3 px-4 font-semibold">Timestamp</th>
                  <th className="py-3 px-4 font-semibold">Resume Filename</th>
                  <th className="py-3 px-4 font-semibold">Target Job Role</th>
                  <th className="py-3 px-4 font-semibold">Baseline Score</th>
                  <th className="py-3 px-4 font-semibold">Matched Skills</th>
                  <th className="py-3 px-4 font-semibold">Missing Gaps</th>
                  <th className="py-3 px-4 font-semibold text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {history.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3 px-4 font-bold text-slate-500">#{item.id}</td>
                    <td className="py-3 px-4 text-slate-500 whitespace-nowrap">{item.timestamp}</td>
                    <td className="py-3 px-4 font-medium text-slate-800">{item.resume_filename}</td>
                    <td className="py-3 px-4 text-slate-700">{item.job_title}</td>
                    <td className="py-3 px-4">
                      <span className="font-bold text-indigo-700 bg-indigo-50 border border-indigo-200 px-2 py-0.5 rounded">
                        {item.similarity_score}%
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-emerald-700 font-semibold">{item.matched_skills.length}</span>
                      <span className="text-[11px] text-slate-400 block truncate max-w-[150px]">
                        {item.matched_skills.slice(0, 3).join(', ')}{item.matched_skills.length > 3 ? '...' : ''}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-amber-700 font-semibold">{item.missing_skills.length}</span>
                      <span className="text-[11px] text-slate-400 block truncate max-w-[150px]">
                        {item.missing_skills.slice(0, 3).join(', ')}{item.missing_skills.length > 3 ? '...' : ''}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleDelete(item.id)}
                        disabled={deletingId === item.id}
                        title="Delete Record"
                        className="text-slate-400 hover:text-red-600 p-1 rounded hover:bg-red-50 transition-colors"
                      >
                        <Trash2 size={15} />
                      </button>
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
