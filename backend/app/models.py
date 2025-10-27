from pydantic import BaseModel
from typing import List, Optional

# --- User models ---
class User(BaseModel):
    name: str
    role: str
    skills: List[str]
    workload: float
    email: str

class UserCreate(BaseModel):
    full_name: str
    role: str
    skill1: str
    skill2: Optional[str] = None
    skill3: Optional[str] = None
    workload: float
    email: str


# --- Task models ---
class Task(BaseModel):
    title: str
    required_skills: List[str]
    duration: int

class TaskCreate(BaseModel):
    title: str
    skill1: str
    skill2: Optional[str] = None
    skill3: Optional[str] = None
    duration: int

class TaskResponse(BaseModel):
    id: int
    title: str
    required_skills: List[str]
    duration: int
    assigned_to: Optional[str] = None
    is_assigned: bool

# --- Assignment models ---
class SuggestionRequest(BaseModel):
    users: List[User]
    tasks: List[Task]

class SuggestionResponse(BaseModel):
    task: str
    assigned_to: str
    score: float