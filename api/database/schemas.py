from pydantic import BaseModel
from typing import List

class TaskBase(BaseModel):
    title: str
    description: str
    section_id: str
    priority: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    project_id: str
    finished: bool

    class Config:
        orm_mode = True

class SectionBase(BaseModel):
    title: str

class SectionCreate(SectionBase):
    pass

class Section(SectionBase):
    id: str
    project_id: str
    tasks: List[Task] = []
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    title: str
    color: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str

    sections: List[Section] = []
    total_tasks: int
    finished_tasks: int

    class Config:
        orm_mode = True