# app/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, models
from .database import SessionLocal
from .models import TaskCreate, TaskResponse, User, Task
from .services.task_assignment_service_debug import assign_tasks_debug

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- User routes ---
@router.post("/users/", response_model=models.User)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(crud.UserDB).filter(crud.UserDB.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crud.create_user(
        db=db,
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        skill1=user.skill1,
        skill2=user.skill2,
        skill3=user.skill3,
        workload=user.workload
    )
    return User(
        name=db_user.full_name,
        role=db_user.role,
        skills=db_user.skills.split(",") if db_user.skills else [],
        workload=db_user.workload,
        email=db_user.email  # ✅ AJOUTÉ
    )

@router.get("/users/", response_model=List[models.User])
def read_users(db: Session = Depends(get_db)):
    users_db = crud.get_all_users(db)
    return [
        User(
            name=u.full_name,
            role=u.role,
            skills=u.skills.split(",") if u.skills else [],
            workload=u.workload,
            email=u.email
        )
        for u in users_db
    ]

# --- Task routes ---
@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.create_task(
        db=db,
        title=task.title,
        skill1=task.skill1,
        skill2=task.skill2,
        skill3=task.skill3,
        duration=task.duration
    )
    skills = [db_task.skill1]
    if db_task.skill2:
        skills.append(db_task.skill2)
    if db_task.skill3:
        skills.append(db_task.skill3)

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        required_skills=skills,
        duration=db_task.duration,
        assigned_to=db_task.assigned_to,
        is_assigned=db_task.is_assigned
    )

@router.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    tasks_db = crud.get_all_tasks(db)
    result = []
    for t in tasks_db:
        skills = [t.skill1]
        if t.skill2: skills.append(t.skill2)
        if t.skill3: skills.append(t.skill3)
        result.append(TaskResponse(
            id=t.id,
            title=t.title,
            required_skills=skills,
            duration=t.duration,
            assigned_to=t.assigned_to,
            is_assigned=t.is_assigned
        ))
    return result

# --- AI Assignment: ALL unassigned tasks ---
@router.post("/assign-tasks")
def assign_tasks_with_ai(db: Session = Depends(get_db)):
    unassigned_tasks_db = db.query(crud.TaskDB).filter(crud.TaskDB.is_assigned == False).all()
    if not unassigned_tasks_db:
        return {"message": "No unassigned tasks to assign"}

    users_db = crud.get_all_users(db)
    users_pydantic = [
        User(
            name=u.full_name,
            role=u.role,
            skills=u.skills.split(",") if u.skills else [],
            workload=u.workload,
            email=u.email  # ✅ Ajouté
        )
        for u in users_db
    ]

    tasks_pydantic = []
    for t in unassigned_tasks_db:
        skills = [t.skill1]
        if t.skill2: skills.append(t.skill2)
        if t.skill3: skills.append(t.skill3)
        tasks_pydantic.append(Task(title=t.title, required_skills=skills, duration=t.duration))

    ai_result = assign_tasks_debug(users_pydantic, tasks_pydantic)

    # Update DB
    title_to_task = {t.title: t for t in unassigned_tasks_db}
    for res in ai_result["results"]:
        task_title = res["task"]
        assigned_user = res["chosen"]["name"]
        if assigned_user and task_title in title_to_task:
            db_task = title_to_task[task_title]
            crud.update_task_assignment(db, db_task.id, assigned_user)

    return ai_result

# --- AI Assignment: SINGLE task by ID ---
@router.post("/assign-task/{task_id}")
def assign_single_task(task_id: int, db: Session = Depends(get_db)):
    # Get the specific unassigned task
    task_db = db.query(crud.TaskDB).filter(
        crud.TaskDB.id == task_id,
        crud.TaskDB.is_assigned == False
    ).first()

    if not task_db:
        raise HTTPException(
            status_code=404,
            detail="Task not found or already assigned"
        )

    # Get all users
    users_db = crud.get_all_users(db)
    users_pydantic = [
        User(
            name=u.full_name,
            role=u.role,
            skills=u.skills.split(",") if u.skills else [],
            workload=u.workload,
            email=u.email  # ✅ Ajouté
        )
        for u in users_db
    ]

    # Build task for AI
    skills = [task_db.skill1]
    if task_db.skill2: skills.append(task_db.skill2)
    if task_db.skill3: skills.append(task_db.skill3)
    task_pydantic = Task(
        title=task_db.title,
        required_skills=skills,
        duration=task_db.duration
    )

    # Run AI on single task
    ai_result = assign_tasks_debug(users_pydantic, [task_pydantic])

    # Update DB
    assigned_user = ai_result["results"][0]["chosen"]["name"]
    if assigned_user:
        crud.update_task_assignment(db, task_db.id, assigned_user)

    return ai_result