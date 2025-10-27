from sqlalchemy.orm import Session
from . import models
from datetime import datetime

def get_project(db: Session, project_id: int):
    return db.get(models.Project, project_id)

def get_latest_summary(db: Session, project_id: int):
    return db.query(models.Summary).filter(models.Summary.project_id==project_id).order_by(models.Summary.generated_at.desc()).first()

def save_summary(db: Session, project_id: int, content: str):
    latest = get_latest_summary(db, project_id)
    version = (latest.version + 1) if latest else 1
    s = models.Summary(project_id=project_id, content=content, version=version, generated_at=datetime.utcnow())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def fetch_activities(db: Session, project_id: int, limit: int = 20):
    return db.query(models.Activity).filter(models.Activity.project_id==project_id).order_by(models.Activity.created_at.desc()).limit(limit).all()

def fetch_tasks(db: Session, project_id: int):
    return db.query(models.Task).filter(models.Task.project_id==project_id).all()
