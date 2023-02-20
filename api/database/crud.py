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
    if(project.color == "#000000"):
        color = "#"+''.join(random.choice('ABCDEF0123456789') for i in range(6))
    else:
        color = project.color
    new_id = str(uuid.uuid4())
    db_project = models.Project(
        id=new_id,
        title=project.title,
        total_tasks=0,
        finished_tasks=0,
        color=color
        )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def edit_project(db: Session, project:schemas.ProjectCreate, project_id: str):
    db_changed = get_project(db=db, project_id=project_id)

    db_changed.title = project.title
    db_changed.color = project.color
    
    db.commit()
    db.refresh(db_changed)
    return db_changed

def del_project(db:Session, project_id: str):
    project_to_delete = db.query(models.Project).filter(models.Project.id == project_id).first()
    db.delete(project_to_delete)
    db.commit()


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

def edit_task(db: Session, task: schemas.TaskCreate, project_id: str, task_id: str):
    db_changed = get_task(db=db, task_id=task_id)
    
    db_changed.project_id = project_id
    db_changed.title = task.title
    db_changed.description = task.description
    db_changed.priority = task.priority
    
    db.commit()
    db.refresh(db_changed)
    return db_changed

def del_task(db:Session, task_id: str):
    db.query(models.Task).filter(models.Task.id == task_id).delete()
    db.commit();

def create_section(db:Session, section: schemas.SectionCreate, project_id: str):
    db_section = models.Section(
        **section.dict(),
        id=str(uuid.uuid4()),
        project_id=project_id,
    )
    db.add(db_section)
    db.commit()
    db.refresh(db_section);
    return db_section