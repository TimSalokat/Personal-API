from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str
    priority: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    project_id: str
    finished: bool

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    title: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str

    tasks: list[Task] = []
    total_tasks: int
    finished_tasks: int
    color: str

    class Config:
        orm_mode = True