// frontend/src/components/SummaryCard.js
import React from "react";

const SummaryCard = ({ summary }) => {
  if (!summary) return <div style={{ marginTop: 10 }} className="small-muted">Aucun résumé.</div>;
  return (
    <div style={{ marginTop: 10, padding: 10, background: "#f9f9f9", borderRadius: 8, borderLeft: "4px solid #007bff" }}>
      <strong>Résumé :</strong>
      <pre style={{ whiteSpace: "pre-wrap", marginTop: 8 }}>{summary}</pre>
    </div>
  );
};

export default SummaryCard;
