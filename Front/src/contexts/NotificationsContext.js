// NotificationsContext.js
import React, { createContext, useContext, useState } from "react";

const NotificationsContext = createContext();

export function NotificationsProvider({ children }) {
  const [notifications, setNotifications] = useState([]);

  function addNotification(payload) {
    // payload peut être string ou objet {text,...} ou {summary:...}
    const text =
      typeof payload === "string"
        ? payload
        : payload?.text ?? payload?.summary ?? JSON.stringify(payload);
    const item = {
      id: Date.now() + Math.floor(Math.random() * 999),
      text,
      time: new Date().toISOString(),
      raw: payload,
    };
    setNotifications((prev) => [item, ...prev]);
  }

  function clearNotifications() {
    setNotifications([]);
  }

  return (
    <NotificationsContext.Provider value={{ notifications, addNotification, clearNotifications }}>
      {children}
    </NotificationsContext.Provider>
  );
}

export function useNotifications() {
  const ctx = useContext(NotificationsContext);
  if (!ctx) throw new Error("useNotifications must be used inside NotificationsProvider");
  return ctx;
}
