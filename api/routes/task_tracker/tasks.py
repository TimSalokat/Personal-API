
import sys, os

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request 
from sqlalchemy.orm import Session

import uuid, random

from ...database import models, schemas
from ...database.database import get_db

from ..auth import auth
from ..task_tracker.projects import get_project

router = APIRouter()

@router.post("/add/{project_id}",
    dependencies=[Depends(auth.authentication_middleware)])
async def add(
    project_id: str,
    request: Request,
    task: schemas.TaskCreate,
):
    db = get_db()
    db.commit()
    return create_task(db=db, task=task, project_id=project_id, owner=request.state.user_name)

@router.put("/set-finished")
async def set_finished(
    task_id: str,
):
    db = get_db()
    task = get_task(db=db, task_id=task_id)
    task.finished = not task.finished

    db.commit()
    db.refresh(task)
    return task

@router.put("/edit",
    dependencies=[Depends(auth.authentication_middleware)])
async def edit(
    task: schemas.TaskCreate,
    request: Request
):
    db = get_db()
    project_id = request.headers.get("project_id")
    section_id = request.headers.get("section_id")
    task_id = request.headers.get("task_id")
    return edit_task(db=db, task=task, project_id=project_id, section_id=section_id, task_id=task_id)

@router.delete("/delete",
    dependencies=[Depends(auth.authentication_middleware)])
async def delete(
    request: Request,
):
    db = get_db()
    return del_task(db=db, task_id=request.headers.get("task_id"))


def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate, project_id: str, owner: str):
    if(get_project(db=db, project_id=project_id).owner != owner):
        raise HTTPException(status_code=401, detail='Not your Project');
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

def edit_task(db: Session, task: schemas.TaskCreate, project_id: str, section_id: str, task_id: str):
    db_changed = get_task(db=db, task_id=task_id)
    
    db_changed.project_id = project_id
    db_changed.section_id = section_id
    db_changed.title = task.title
    db_changed.description = task.description
    db_changed.priority = task.priority
    
    db.commit()
    db.refresh(db_changed)
    return db_changed

def del_task(db:Session, task_id: str):
    db.query(models.Task).filter(models.Task.id == task_id).delete()
    db.commit();