// frontend/src/services/api.js
import axios from "axios";
const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

const API = axios.create({ baseURL: API_URL, timeout: 10000 });

export const getProjects = async () => {
  const res = await API.get(`/projects`);
  return res.data;
};

// POST pour lancer la génération.
// Retour possible : { status: "...", summary: "..." } ou { status: "started_in_background" }
export const summarizeProgress = async (projectId) => {
  const res = await API.post(`/projects/${projectId}/summaries/generate`);
  return res.data;
};

// GET dernier résumé : renvoie string (ou null)
export const getLatestSummary = async (projectId) => {
  const res = await API.get(`/projects/${projectId}/summaries/latest`);
  const data = res.data ?? {};
  // backend peut renvoyer { summary: "..." } ou { id:..., content: "..." }
  return data.summary ?? data.content ?? null;
};

export default API;
