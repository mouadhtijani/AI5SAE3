export const createUser = async (userData) => {
  const res = await fetch("http://127.0.0.1:8000/api/tasks/users/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData)
  });
  return res.json();
};