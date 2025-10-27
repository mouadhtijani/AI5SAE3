from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class UserCreate(BaseModel):
    name: Optional[str]
    email: str

class UserOut(BaseModel):
    id: int
    name: Optional[str]
    email: str
    class Config:
        orm_mode = True

class TaskOut(BaseModel):
    id: int
    title: Optional[str]
    status: Optional[str]
    assignee_id: Optional[int]
    updated_at: datetime
    class Config:
        orm_mode = True

class ActivityOut(BaseModel):
    id: int
    action: str
    meta: Optional[Any]
    created_at: datetime
    class Config:
        orm_mode = True

class SummaryOut(BaseModel):
    id: int
    content: str
    generated_at: datetime
    version: int
    class Config:
        orm_mode = True

class ProjectOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    progress: int
    created_at: datetime
    class Config:
        orm_mode = True
