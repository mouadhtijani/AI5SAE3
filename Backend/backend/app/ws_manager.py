# backend/app/ws_manager.py
import asyncio
from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # project_id -> set(WebSocket)
        self._conns: Dict[int, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, project_id: int):
        await websocket.accept()
        async with self._lock:
            s = self._conns.setdefault(project_id, set())
            s.add(websocket)
        print(f"[ws] connected project={project_id} clients={len(self._conns.get(project_id,[]))}")

    async def disconnect(self, websocket: WebSocket, project_id: int):
        async with self._lock:
            conns = self._conns.get(project_id, set())
            if websocket in conns:
                conns.remove(websocket)
        print(f"[ws] disconnected project={project_id}")

    async def send_to_project(self, project_id: int, message: dict):
        """Send JSON message to all connected clients for project_id."""
        async with self._lock:
            conns = list(self._conns.get(project_id, set()))
        if not conns:
            print(f"[ws] send_to_project: no clients for project {project_id}")
            return
        print(f"[ws] broadcasting to project {project_id} -> {len(conns)} clients")
        to_remove = []
        for ws in conns:
            try:
                await ws.send_json(message)
            except Exception as e:
                print("[ws] send error:", e)
                to_remove.append(ws)
        if to_remove:
            async with self._lock:
                for ws in to_remove:
                    if ws in self._conns.get(project_id, set()):
                        self._conns[project_id].remove(ws)

# singleton manager to import in other modules
manager = ConnectionManager()

def notify_project(project_id: int, message: dict):
    """
    Sync helper to schedule sending message to project clients.
    Use this in FastAPI BackgroundTasks: background_tasks.add_task(ws_manager.notify_project, project_id, message)
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # schedule without blocking
        asyncio.create_task(manager.send_to_project(project_id, message))
    else:
        # fallback if no loop running (rare in FastAPI)
        asyncio.run(manager.send_to_project(project_id, message))
