// NotificationCenter.js
import React from "react";
import { useNotifications } from "../contexts/NotificationsContext";

export default function NotificationCenter({ open, onClose }) {
  const { notifications, clearNotifications } = useNotifications();
  if (!open) return null;

  return (
    <div style={{
      position: "fixed",
      right: 20,
      top: 80,
      width: 360,
      maxHeight: "70vh",
      overflowY: "auto",
      background: "#fff",
      boxShadow: "0 8px 30px rgba(0,0,0,0.12)",
      borderRadius: 8,
      padding: 12,
      zIndex: 9999
    }}>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:8}}>
        <h4 style={{margin:0}}>Notifications</h4>
        <div style={{display:"flex", gap:8}}>
          <button onClick={clearNotifications}>Effacer</button>
          <button onClick={onClose}>Fermer</button>
        </div>
      </div>
      <div style={{ fontSize: 13 }}>
        {notifications.length === 0 && <div className="small-muted">Aucune notification</div>}
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {notifications.map(n => (
            <li key={n.id} style={{ padding: "8px 6px", borderBottom: "1px solid #eee" }}>
              <div style={{ fontSize: 12, color: "#666" }}>{new Date(n.time).toLocaleString()}</div>
              <div style={{ marginTop: 6 }}>{n.text}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
