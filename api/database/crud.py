from sqlalchemy.orm import Session

import uuid, random
from . import models, schemas

def get_project(db: Session, project_id: str):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_project_by_title(db: Session, title: str):
    return db.query(models.Project).filter(models.Project.title == title).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    color = "#"+''.join(random.choice('ABCDEF0123456789') for i in range(6))
    db_project = models.Project(
        id=str(uuid.uuid4()),
        title=project.title,
        total_tasks=0,
        finished_tasks=0,
        color=color
        )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate, project_id: str):
    db_task = models.Task(
        **task.dict(),
        project_id=project_id,
        id=str(uuid.uuid4()),
        finished=False
        )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task