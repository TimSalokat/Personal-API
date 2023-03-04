
import sys, os

from fastapi import APIRouter
from starlette.requests import Request 
from sqlalchemy.orm import Session

import uuid, random

from ...database import models, schemas
from ...database.database import get_db

router = APIRouter();

@router.get("/get", response_model=list[schemas.Project])
async def get(
    skip: int = 0,
    limit: int = 100,
    testing: bool = False
):
    db = get_db(testing)
    return get_projects(db, skip=skip, limit=limit)

@router.post("/add") 
async def add(project: schemas.ProjectCreate, testing: bool = False):
    db = get_db(testing)
    return create_project(db=db, project=project)

@router.put("/edit")
async def edit(
    project: schemas.ProjectCreate,
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    project_id = request.headers.get("project_id")
    return edit_project(db=db, project=project, project_id=project_id)
    
@router.delete("/delete")
async def delete(
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    return del_project(db=db, project_id=request.headers.get("project_id"))



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