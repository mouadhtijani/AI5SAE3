// NotificationsButton.js
import React from "react";
import { useNotifications } from "../contexts/NotificationsContext";

export default function NotificationsButton({ open, onToggle }) {
  const { notifications } = useNotifications();
  const count = notifications.length;
  return (
    <button onClick={onToggle} style={{ position: "relative", padding: "8px 12px", borderRadius: 6 }}>
      🔔 Notifications
      {count > 0 && (
        <span style={{
          position: "absolute",
          top: -6,
          right: -6,
          background: "#e63946",
          color: "#fff",
          borderRadius: 12,
          padding: "2px 6px",
          fontSize: 12
        }}>
          {count}
        </span>
      )}
      {open ? " (Fermer)" : ""}
    </button>
  );
}
