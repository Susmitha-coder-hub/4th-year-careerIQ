import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import ResumeAnalyzer from './pages/ResumeAnalyzer';
import JobMatching from './pages/JobMatching';
import SkillGapAnalysis from './pages/SkillGapAnalysis';
import AnalysisHistory from './pages/AnalysisHistory';
import AboutCareerFit from './pages/AboutCareerFit';
import { checkBackendHealth } from './api/client';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileOpen, setMobileOpen] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking');

  // Shared session states across modules
  const [resumeData, setResumeData] = useState(null);
  const [matchingResult, setMatchingResult] = useState(null);

  useEffect(() => {
    async function verifyBackend() {
      const res = await checkBackendHealth();
      if (res.status === 'healthy') {
        setBackendStatus('online');
      } else {
        setBackendStatus('offline');
      }
    }
    verifyBackend();
    const interval = setInterval(verifyBackend, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar Navigation */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        mobileOpen={mobileOpen} 
        setMobileOpen={setMobileOpen} 
      />

      {/* Main Content Area */}
      <div className="flex-1 md:pl-64 flex flex-col min-h-screen">
        <Header 
          setMobileOpen={setMobileOpen} 
          backendStatus={backendStatus} 
        />

        <main className="flex-1 p-6 sm:p-8 max-w-7xl w-full mx-auto">
          {activeTab === 'dashboard' && (
            <Dashboard setActiveTab={setActiveTab} />
          )}

          {activeTab === 'resume' && (
            <ResumeAnalyzer 
              resumeData={resumeData} 
              setResumeData={setResumeData} 
              setActiveTab={setActiveTab}
            />
          )}

          {activeTab === 'matching' && (
            <JobMatching 
              resumeData={resumeData} 
              matchingResult={matchingResult} 
              setMatchingResult={setMatchingResult} 
              setActiveTab={setActiveTab}
            />
          )}

          {activeTab === 'skillgap' && (
            <SkillGapAnalysis 
              matchingResult={matchingResult} 
              setActiveTab={setActiveTab}
            />
          )}

          {activeTab === 'history' && (
            <AnalysisHistory />
          )}

          {activeTab === 'about' && (
            <AboutCareerFit />
          )}
        </main>
      </div>
    </div>
  );
}
