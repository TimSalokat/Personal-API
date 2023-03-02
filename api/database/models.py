from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    sections = relationship("Section", primaryjoin="Project.id == Section.project_id", cascade="all, delete-orphan")
    total_tasks = Column(Integer)
    finished_tasks = Column(Integer)

    color = Column(String)

class Section(Base):
    __tablename__ = "sections"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, unique=False)
    project_id = Column(String, ForeignKey("projects.id"))
    tasks = relationship("Task", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    section_id = Column(String, ForeignKey("sections.id"))

    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer)
    finished = Column(Boolean)