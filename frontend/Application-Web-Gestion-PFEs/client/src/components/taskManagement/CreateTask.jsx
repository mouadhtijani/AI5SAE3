import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createTask } from '../../api/taskAssignmentApi';

export default function CreateTask() {
  const [formData, setFormData] = useState({
    title: "",
    skill1: "",
    skill2: "",
    skill3: "",
    duration: 1
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createTask({
        title: formData.title,
        skill1: formData.skill1,
        skill2: formData.skill2 || undefined,
        skill3: formData.skill3 || undefined,
        duration: parseInt(formData.duration)
      });
      alert("Task created successfully!");
      navigate("/admin/tasks");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <div className="container" style={{ padding: '20px' }}>
      <h2>Create New Task</h2>
      <form onSubmit={handleSubmit}>
        <input name="title" placeholder="Task title" onChange={handleChange} required style={{ display: 'block', margin: '10px 0', padding: '8px', width: '300px' }} />
        <input name="skill1" placeholder="Skill 1 (required)" onChange={handleChange} required style={{ display: 'block', margin: '10px 0', padding: '8px', width: '300px' }} />
        <input name="skill2" placeholder="Skill 2 (optional)" onChange={handleChange} style={{ display: 'block', margin: '10px 0', padding: '8px', width: '300px' }} />
        <input name="skill3" placeholder="Skill 3 (optional)" onChange={handleChange} style={{ display: 'block', margin: '10px 0', padding: '8px', width: '300px' }} />
        <input name="duration" type="number" min="1" placeholder="Duration (hours)" onChange={handleChange} required style={{ display: 'block', margin: '10px 0', padding: '8px', width: '300px' }} />
        <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}>
          Create Task
        </button>
      </form>
    </div>
  );
}