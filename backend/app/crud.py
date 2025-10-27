from typing import List, Optional
from sqlalchemy.orm import Session
from .models_db import UserDB, TaskDB

# --- User CRUD ---
def get_all_users(db: Session) -> List[UserDB]:
    return db.query(UserDB).all()

def create_user(
        db: Session,
        full_name: str,
        email: str,
        role: str,
        skill1: str,
        workload: float,
        skill2: Optional[str] = None,
        skill3: Optional[str] = None,
):
    skills = [skill1]
    if skill2: skills.append(skill2)
    if skill3: skills.append(skill3)
    db_user = UserDB(
        full_name=full_name,
        email=email,
        role=role,
        skills=",".join(skills),
        workload=workload
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Task CRUD ---
def create_task(
        db: Session,
        title: str,
        skill1: str,
        duration: int,
        skill2: Optional[str] = None,
        skill3: Optional[str] = None,
):
    db_task = TaskDB(
        title=title,
        skill1=skill1,
        skill2=skill2,
        skill3=skill3,
        duration=duration,
        assigned_to=None,
        is_assigned=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_all_tasks(db: Session) -> List[TaskDB]:
    return db.query(TaskDB).all()

def delete_task(db: Session, task_id: int):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
# app/crud.py

def update_task_assignment(db: Session, task_id: int, assigned_to: str):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        task.assigned_to = assigned_to
        task.is_assigned = True
        db.commit()
        db.refresh(task)
    return task