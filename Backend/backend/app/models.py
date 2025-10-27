from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="project", cascade="all,delete-orphan")
    activities = relationship("Activity", back_populates="project", cascade="all,delete-orphan")
    summaries = relationship("Summary", back_populates="project", cascade="all,delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String)
    status = Column(String, default="todo")
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="tasks")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String)
    meta = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="activities")

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    content = Column(Text)
    generated_at = Column(DateTime, default=datetime.utcnow)
    version = Column(Integer, default=1)

    project = relationship("Project", back_populates="summaries")
