/**
 * frontend/src/api/client.js
 * Centralized API client for communicating with the CareerFit FastAPI backend.
 */

const API_BASE_URL = 'http://localhost:8000/api';

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) throw new Error('Backend unhealthy');
    return await res.json();
  } catch (err) {
    return { status: 'offline', error: err.message };
  }
}

export async function uploadAndParseResume(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE_URL}/resumes/parse`, {
    method: 'POST',
    body: formData,
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to parse resume');
  }
  return data;
}

export async function analyzeJobDescription(jobDescription, jobTitle = 'Target Role') {
  const res = await fetch(`${API_BASE_URL}/jobs/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      job_description: jobDescription,
      job_title: jobTitle,
    }),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to analyze job description');
  }
  return data;
}

export async function computeMatching({
  resumeText,
  jobText,
  resumeFilename = 'Resume.pdf',
  jobTitle = 'Target Role',
  resumeSkills = [],
  saveToHistory = true,
}) {
  const res = await fetch(`${API_BASE_URL}/matching/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_text: resumeText,
      job_text: jobText,
      resume_filename: resumeFilename,
      job_title: jobTitle,
      resume_skills: resumeSkills,
      save_to_history: saveToHistory,
    }),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to compute matching score');
  }
  return data;
}

export async function fetchAnalysisHistory() {
  const res = await fetch(`${API_BASE_URL}/history`);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to fetch history');
  }
  return data;
}

export async function deleteAnalysisRecord(id) {
  const res = await fetch(`${API_BASE_URL}/history/${id}`, {
    method: 'DELETE',
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to delete record');
  }
  return data;
}

export async function fetchDashboardStats() {
  const res = await fetch(`${API_BASE_URL}/dashboard/stats`);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to fetch stats');
  }
  return data;
}

// --- Milestone 2 API Methods ---

export async function predictPlacementReadiness(profile) {
  const res = await fetch(`${API_BASE_URL}/prediction/placement-readiness`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to evaluate placement readiness');
  }
  return data;
}

export async function rankCandidatesAgainstJD({ jobTitle, jobDescription, candidates }) {
  const res = await fetch(`${API_BASE_URL}/recruiter/rank-resumes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      job_title: jobTitle,
      job_description: jobDescription,
      candidates: candidates,
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to rank candidates');
  }
  return data;
}

export async function fetchOpportunities(cgpa = 7.5, branch = 'Computer Science and Engineering') {
  const res = await fetch(`${API_BASE_URL}/opportunities/?cgpa=${cgpa}&branch=${encodeURIComponent(branch)}`);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to fetch opportunities');
  }
  return data;
}

export async function checkOpportunityEligibility(profile) {
  const res = await fetch(`${API_BASE_URL}/opportunities/check-eligibility`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to check eligibility');
  }
  return data;
}

export async function fetchInterviewPrepGuide(opportunityId) {
  const res = await fetch(`${API_BASE_URL}/opportunities/prep-guide/${opportunityId}`);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to fetch prep guide');
  }
  return data;
}

export async function sendChatMessage({ message, contextSkills = [], contextCgpa = 7.5, contextTargetJob = '' }) {
  const res = await fetch(`${API_BASE_URL}/chat/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      context_skills: contextSkills,
      context_cgpa: contextCgpa,
      context_target_job: contextTargetJob,
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Failed to send chat message');
  }
  return data;
}
