import React from 'react';
import {
  LayoutDashboard,
  FileText,
  Target,
  GitCompare,
  History,
  Info,
  Award,
  Users,
  Bell,
  Bot,
  X
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, mobileOpen, setMobileOpen }) {
  const studentItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'resume', label: 'Resume Analyzer', icon: FileText, badge: 'Mod 1' },
    { id: 'matching', label: 'Job Matching', icon: Target, badge: 'Mod 2' },
    { id: 'skillgap', label: 'Skill Gap & Pathways', icon: GitCompare, badge: 'Mod 3' },
    { id: 'prediction', label: 'Placement Readiness', icon: Award, badge: 'New' },
    { id: 'opportunities', label: 'Opportunity Alerts', icon: Bell, badge: 'New' },
    { id: 'chatbot', label: 'AI Career Assistant', icon: Bot, badge: 'AI' },
  ];

  const recruiterItems = [
    { id: 'recruiter', label: 'Recruiter Candidate Rank', icon: Users, badge: 'New' },
  ];

  const systemItems = [
    { id: 'history', label: 'Analysis History', icon: History },
    { id: 'about', label: 'Scope & Project Spec', icon: Info },
  ];

  const renderNavGroup = (title, items) => (
    <div className="space-y-1 mb-4">
      <div className="px-3 pb-1 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
        {title}
      </div>
      {items.map((item) => {
        const Icon = item.icon;
        const isActive = activeTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => {
              setActiveTab(item.id);
              setMobileOpen(false);
            }}
            className={`
              w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition-colors
              ${isActive
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'}
            `}
          >
            <div className="flex items-center space-x-2.5">
              <Icon size={16} />
              <span>{item.label}</span>
            </div>
            {item.badge && (
              <span className={`text-[9px] px-1.5 py-0.5 rounded font-bold ${isActive
                  ? 'bg-indigo-700 text-indigo-100'
                  : item.badge === 'New'
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : item.badge === 'AI'
                      ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                      : 'bg-slate-800 text-slate-400'
                }`}>
                {item.badge}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );

  return (
    <>
      {/* Mobile backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-40 md:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside className={`
        fixed top-0 bottom-0 left-0 z-50 w-64 bg-slate-900 text-white flex flex-col transition-transform duration-200 ease-in-out
        md:translate-x-0 ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {/* Brand Header */}
        <div className="h-16 px-6 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow">
              CF
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight">CareerFit</span>
              <span className="block text-xs text-slate-400">AI Career Intelligence</span>
            </div>
          </div>
          <button
            className="md:hidden text-slate-400 hover:text-white"
            onClick={() => setMobileOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        {/* Navigation items */}
        <nav className="flex-1 px-3 py-3 overflow-y-auto">
          {renderNavGroup('Student Intelligence', studentItems)}
          {renderNavGroup('Recruiter Intelligence', recruiterItems)}
          {renderNavGroup('System & Documentation', systemItems)}
        </nav>

        {/* Footer info */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/40 text-xs text-slate-400">
          <div className="flex items-center justify-between">
            <span>Status:</span>
            <span className="text-emerald-400 font-medium">● Local Demo Mode</span>
          </div>
          <div className="mt-1 text-[11px] text-indigo-400 font-semibold">
            Scope: Milestone 2 (~50-60% Planned Scope)
          </div>
        </div>
      </aside>
    </>
  );
}
