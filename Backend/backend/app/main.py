# backend/app/main.py
import asyncio
import os

from fastapi import FastAPI, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
# on importe models sous alias pour éviter l'avertissement "unused import" :
from . import models as _models  # imported to register SQLAlchemy models
from . import crud, tasks, ws_manager

# create tables in dev (use Alembic for prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Projects API (dev)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def schedule_ws(project_id: int, message: dict):
    """
    Helper sync function to be used with FastAPI BackgroundTasks.
    It schedules the async ws_manager.manager.send_to_project(...) call on the running loop.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # schedule the async send without blocking
        asyncio.create_task(ws_manager.manager.send_to_project(project_id, message))
    else:
        # fallback: run the coroutine (rare in normal FastAPI runtime)
        asyncio.run(ws_manager.manager.send_to_project(project_id, message))


@app.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = crud.get_project(db, project_id)
    if not p:
        return {"error": "not found"}, 404
    return p


@app.get("/projects/{project_id}/summaries/latest")
def get_latest_summary(project_id: int, db: Session = Depends(get_db)):
    s = crud.get_latest_summary(db, project_id)
    if not s:
        return {"summary": None}
    return {"summary": s.content, "generated_at": s.generated_at, "version": s.version}

@app.post("/projects/{project_id}/summaries/generate")
def generate_summary(project_id: int, background_tasks: BackgroundTasks):
    # Dev option: force synchronous generation if env var set
    if os.getenv("FORCE_SYNC_SUMMARY", "0") == "1":
        # Mode dev forcé : exécution synchrone et renvoi du résumé + notification WS
        result = tasks.generate_summary_sync(project_id)
        if result.get("ok"):
            content = result.get("content")
            summary_id = result.get("summary_id")
            # schedule WS notify (non blocking)
            background_tasks.add_task(
                ws_manager.notify_project,
                project_id,
                {"type": "summary_generated", "project_id": project_id, "summary": content, "summary_id": summary_id}
            )
            background_tasks.add_task(
                ws_manager.notify_project,
                project_id,
                {"type":"notification", "project_id":project_id, "text": f"Nouveau résumé pour {project_id}"}
            )
            return {"status":"done", "summary": content, "summary_id": summary_id}
        return {"status":"error", "error": result.get("error")}

    # Sinon comportement normal : utiliser Celery si configuré
    if getattr(tasks, "celery", None):
        tasks.celery.send_task("app.tasks.generate_project_summary_task", args=[project_id])
        return {"status": "started_in_background"}
    # fallback si pas de celery :
    result = tasks.generate_summary_sync(project_id)
    if result.get("ok"):
        return {"status":"done", "summary": result.get("content"), "summary_id": result.get("summary_id")}
    return {"status":"error", "error": result.get("error")}


@app.websocket("/ws/projects/{project_id}")
async def ws_project(websocket: WebSocket, project_id: int):
    # connect: use the manager from ws_manager module
    await ws_manager.manager.connect(websocket, project_id)
    try:
        while True:
            # on attend des messages pour garder la connexion ouverte
            await websocket.receive_text()
    except WebSocketDisconnect:
        # disconnect (manager.disconnect is synchronous in your current ws_manager)
        try:
            ws_manager.manager.disconnect(websocket, project_id)
        except Exception:
            # if manager.disconnect is async in some versions, try awaiting
            try:
                await ws_manager.manager.disconnect(websocket, project_id)
            except Exception:
                pass


@app.post("/summarize/{project_id}")
def summarize_compat(project_id: int, background_tasks: BackgroundTasks):
    # compat route -> reuse generate_summary
    return generate_summary(project_id, background_tasks)


@app.get("/health")
def health():
    return {"ok": True}
