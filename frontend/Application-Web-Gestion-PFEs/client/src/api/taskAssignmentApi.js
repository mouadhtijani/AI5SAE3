// src/api/taskAssignmentApi.js
const API_BASE = "http://127.0.0.1:8000/api/tasks";

export const createTask = async (taskData) => {
  const response = await fetch(`${API_BASE}/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(taskData)
  });
  if (!response.ok) throw new Error("Failed to create task");
  return response.json();
};

export const getTasks = async () => {
  const response = await fetch(`${API_BASE}/tasks/`);
  if (!response.ok) throw new Error("Failed to fetch tasks");
  return response.json();
};

export const assignAllTasks = async () => {
  const response = await fetch(`${API_BASE}/assign-tasks`, { method: "POST" });
  if (!response.ok) throw new Error("AI assignment failed");
  return response.json();
};

export const assignTaskById = async (taskId) => {
  const response = await fetch(`${API_BASE}/assign-task/${taskId}`, { method: "POST" });
  if (!response.ok) throw new Error("AI assignment failed");
  return response.json();
};