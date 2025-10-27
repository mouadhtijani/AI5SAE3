// frontend/src/components/ProjectList.js
import React, { useEffect, useState, useRef } from "react";
import { getProjects, summarizeProgress, getLatestSummary } from "../services/api";
import SummaryCard from "./SummaryCard";
import { toast } from "react-toastify";
import { useNotifications } from "../contexts/NotificationsContext";

/**
 * WS_BASE résout automatiquement l'hôte (localhost/127.0.0.1).
 * Si votre frontend est servi en https, définissez REACT_APP_WS_URL=wss://your-host
 */
const host = window.location.hostname || "127.0.0.1";
const defaultWsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const WS_BASE = process.env.REACT_APP_WS_URL || `${defaultWsProtocol}://${host}:8000`;

export default function ProjectList() {
  const [projects, setProjects] = useState([]);
  const [summaries, setSummaries] = useState({});
  const [loadingIds, setLoadingIds] = useState({});
  const wsRefs = useRef({}); // { projectId: { ws, retryCount } }
  const { addNotification } = useNotifications(); // Notifications provider must wrap App

  useEffect(() => {
    fetchProjects();
    return () => {
      // cleanup all websockets on unmount
      Object.values(wsRefs.current).forEach(entry => {
        try { entry?.ws?.close(); } catch (e) {}
      });
      wsRefs.current = {};
    };
  }, []);

  // When projects list changes, open WS per project if not already
  useEffect(() => {
    projects.forEach(p => {
      if (!p || !p.id) return;
      if (wsRefs.current[p.id]) return; // already open or trying
      createProjectWS(p.id, p.title);
    });
  }, [projects]);

  async function fetchProjects() {
    try {
      const data = await getProjects();
      setProjects(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("fetchProjects error:", err);
      toast.error("Erreur lors du chargement des projets !");
    }
  }

  // Create (and auto-reconnect) websocket for a project
  function createProjectWS(projectId, projectTitle) {
    const url = `${WS_BASE}/ws/projects/${projectId}`;
    console.log("[WS] creating", url);
    let localRetry = 0;

    const connect = () => {
      try {
        const ws = new WebSocket(url);

        ws.onopen = () => {
          console.log(`[WS ${projectId}] open`);
          // reset retry counter on success
          wsRefs.current[projectId] = { ws, retryCount: 0 };
        };

        ws.onmessage = (ev) => {
          try {
            const msg = JSON.parse(ev.data);
            console.log(`[WS ${projectId}] msg`, msg);

            if (msg.type === "summary_generated" && msg.summary) {
              // update visible summary
              setSummaries(prev => ({ ...prev, [projectId]: msg.summary }));
              // persist notification in context (history)
              addNotification({
                text: `Résumé généré pour "${projectTitle}"`,
                summary: msg.summary,
                projectId,
                type: "summary_generated"
              });
              // small toast
              toast.info(`Nouveau résumé pour ${projectTitle}`);
            } else if (msg.type === "notification" && msg.text) {
              addNotification({ text: msg.text, projectId, type: "notification" });
              toast.info(msg.text);
            } else {
              // fallback: store raw message as notification
              addNotification({ text: JSON.stringify(msg), projectId, type: "raw" });
            }
          } catch (e) {
            console.error(`[WS ${projectId}] parse error`, e);
          }
        };

        ws.onclose = (ev) => {
          console.warn(`[WS ${projectId}] closed`, ev.reason || ev.code);
          // schedule reconnect with exponential backoff
          const entry = wsRefs.current[projectId] || { retryCount: 0 };
          const nextRetry = Math.min((entry.retryCount || 0) + 1, 10);
          wsRefs.current[projectId] = { ws: null, retryCount: nextRetry };
          const delay = Math.min(30000, 1000 * 2 ** (nextRetry - 1));
          console.log(`[WS ${projectId}] reconnect in ${delay}ms (retry ${nextRetry})`);
          setTimeout(connect, delay);
        };

        ws.onerror = (err) => {
          console.error(`[WS ${projectId}] error`, err);
          // ensure socket closed to trigger onclose and reconnect
          try { ws.close(); } catch (e) {}
        };

      } catch (err) {
        console.error(`[WS ${projectId}] create error`, err);
        localRetry++;
        const delay = Math.min(30000, 1000 * 2 ** Math.min(localRetry, 8));
        setTimeout(connect, delay);
      }
    };

    connect();
  }

  const setLoading = (id, v) => setLoadingIds(prev => ({ ...prev, [id]: v }));

  const handleSummarize = async (id) => {
    setLoading(id, true);
    try {
      const res = await summarizeProgress(id);
      const direct = res?.summary ?? res?.content ?? null;

      if (direct) {
        setSummaries(prev => ({ ...prev, [id]: direct }));
        // persist notification
        addNotification({ text: `Résumé généré (manuellement)`, summary: direct, projectId: id, type: "summary_generated" });
        toast.success("Résumé généré !");
        setLoading(id, false);
        return;
      }

      // fallback: poll /latest a few times
      let got = null;
      for (let i = 0; i < 10; i++) {
        await new Promise(r => setTimeout(r, 500));
        try {
          const latest = await getLatestSummary(id);
          if (latest) { got = latest; break; }
        } catch (e) {
          // ignore transient errors
        }
      }

      if (got) {
        setSummaries(prev => ({ ...prev, [id]: got }));
        addNotification({ text: `Résumé récupéré pour le projet ${id}`, summary: got, projectId: id, type: "summary_fetched" });
        toast.success("Résumé récupéré !");
      } else {
        toast.info("La génération est en cours...");
      }
    } catch (err) {
      console.error("handleSummarize error:", err);
      toast.error("Erreur lors du résumé !");
    } finally {
      setLoading(id, false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Projets étudiants</h2>
      {projects.length === 0 && <div className="small-muted">Aucun projet trouvé.</div>}
      {projects.map(p => (
        <div key={p.id} style={{ border: "1px solid #ddd", padding: 12, marginBottom: 12, borderRadius: 8, background: "#fff" }}>
          <h3 style={{ margin: "0 0 6px 0" }}>{p.title}</h3>
          <p style={{ margin: "0 0 12px 0", color: "#444" }}>{p.description}</p>
          <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 8 }}>
            <button
              onClick={() => handleSummarize(p.id)}
              disabled={!!loadingIds[p.id]}
              style={{ padding: "8px 12px", borderRadius: 6, cursor: loadingIds[p.id] ? "default" : "pointer" }}
            >
              {loadingIds[p.id] ? "Génération..." : "Résumer l’avancement"}
            </button>
            <small style={{ color: "#666" }}>Progress: {p.progress ?? "N/A"}</small>
          </div>

          {summaries[p.id] && <SummaryCard summary={summaries[p.id]} />}
        </div>
      ))}
    </div>
  );
}
