import React from 'react';
import { Menu, Database, ShieldCheck, Cpu } from 'lucide-react';

export default function Header({ setMobileOpen, backendStatus }) {
  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center space-x-3">
        <button
          className="md:hidden p-1.5 text-slate-600 hover:bg-slate-100 rounded-lg"
          onClick={() => setMobileOpen(true)}
        >
          <Menu size={22} />
        </button>
        <div>
          <h1 className="text-base font-semibold text-slate-800">Final Year Academic Demonstration</h1>
          <p className="text-xs text-slate-500 hidden sm:block">AI-Based Career Intelligence & Job Matching System</p>
        </div>
      </div>

      <div className="flex items-center space-x-3 text-xs">
        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
          <Database size={13} className="text-indigo-600" />
          <span>SQLite Store</span>
        </div>

        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
          <Cpu size={13} className="text-indigo-600" />
          <span>TF-IDF + pypdf</span>
        </div>

        <div className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-full border ${
          backendStatus === 'online' 
            ? 'bg-emerald-50 text-emerald-700 border-emerald-200' 
            : 'bg-amber-50 text-amber-700 border-amber-200'
        }`}>
          <span className={`w-2 h-2 rounded-full ${backendStatus === 'online' ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`} />
          <span className="font-medium">{backendStatus === 'online' ? 'FastAPI Online' : 'Connecting...'}</span>
        </div>
      </div>
    </header>
  );
}
