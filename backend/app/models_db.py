from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)  # ← doit exister
    role = Column(String)
    skills = Column(String)
    workload = Column(Float)
class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    skill1 = Column(String)
    skill2 = Column(String, nullable=True)
    skill3 = Column(String, nullable=True)
    duration = Column(Integer)
    assigned_to = Column(String, nullable=True)
    is_assigned = Column(Boolean, default=False)