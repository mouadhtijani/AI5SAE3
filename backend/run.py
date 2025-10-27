# run.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← Ajoutez cet import
from app.models_db import Base
from app.database import engine
from app.routes import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Task Distribution API")

# ✅ AJOUTEZ CE BLOC
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router, prefix="/api/tasks")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True)