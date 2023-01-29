from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="project")
    total_tasks = Column(Integer)
    finished_tasks = Column(Integer)

    color = Column(String)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))

    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer)
    finished = Column(Boolean)
    
    project = relationship("Project", back_populates="tasks")