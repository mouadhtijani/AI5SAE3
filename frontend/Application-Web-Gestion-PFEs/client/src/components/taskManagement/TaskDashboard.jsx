import React, { useState, useEffect } from 'react';
import { getTasks, assignAllTasks, assignTaskById } from '../../api/taskAssignmentApi';


export default function TaskDashboard() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadTasks = async () => {
    try {
      const data = await getTasks();
      setTasks(data);
    } catch (err) {
      alert("Error loading tasks: " + err.message);
    }
  };

  useEffect(() => { loadTasks(); }, []);

  const handleAssignAll = async () => {
    setLoading(true);
    try {
      await assignAllTasks();
      await loadTasks();
      alert("All tasks assigned!");
    } catch (err) {
      alert("Error: " + err.message);
    }
    setLoading(false);
  };

  const handleAssignOne = async (id) => {
    try {
      await assignTaskById(id);
      await loadTasks();
      alert("Task assigned!");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <div className="container" style={{ padding: '20px' }}>
      <h2>AI Task Assignment Dashboard</h2>
      <button 
        onClick={() => window.location.href = '/admin/tasks/create'}
        style={{ padding: '10px 15px', margin: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', cursor: 'pointer' }}
      >
        + Create Task
      </button>
      <button 
        onClick={handleAssignAll} 
        disabled={loading}
        style={{ padding: '10px 15px', margin: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}
      >
        {loading ? "Assigning..." : "Assign All Unassigned Tasks"}
      </button>

      <div>
        {tasks.map(task => (
          <div key={task.id} style={{ border: '1px solid #ccc', margin: '15px 0', padding: '15px', borderRadius: '5px' }}>
            <h3>{task.title}</h3>
            <p><strong>Skills:</strong> {task.required_skills.join(', ')}</p>
            <p><strong>Duration:</strong> {task.duration} hours</p>
            <p><strong>Assigned to:</strong> {task.assigned_to || "—"} </p>
            {!task.is_assigned && (
              <button 
                onClick={() => handleAssignOne(task.id)}
                style={{ padding: '8px 12px', backgroundColor: '#17a2b8', color: 'white', border: 'none', cursor: 'pointer', marginTop: '10px' }}
              >
                Assign with AI
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}