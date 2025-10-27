// App.js
import React, { useState } from "react";
import ProjectList from "./components/ProjectList";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { NotificationsProvider } from "./contexts/NotificationsContext";
import NotificationsButton from "./components/NotificationsButton";
import NotificationCenter from "./components/NotificationCenter";

function AppContent() {
  const [open, setOpen] = useState(false);
  return (
    <>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 16 }}>
        <h1 style={{ textAlign: "center", margin: "0 0 0 0" }}>
          Gestion des Projets Étudiants - Communication & Notifications
        </h1>
        <NotificationsButton open={open} onToggle={() => setOpen(v => !v)} />
      </div>

      <ProjectList />
      <NotificationCenter open={open} onClose={() => setOpen(false)} />
    </>
  );
}

export default function App() {
  return (
    <NotificationsProvider>
      <AppContent />
      <ToastContainer position="top-right" autoClose={4000} />
    </NotificationsProvider>
  );
}
