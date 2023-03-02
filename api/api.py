from __future__ import annotations

from .database import crud, models, schemas
from .database.database import SessionTesting, SessionPersistent, testing_engine, persistent_engine

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sqlalchemy.orm import Session

import os, sys, datetime, random
from starlette.requests import Request 

from termcolor import colored

from .routes.task_tracker import projects

models.Base.metadata.create_all(bind=testing_engine)
models.Base.metadata.create_all(bind=persistent_engine)

def get_db(testing=False):
    if(testing):
        log("Using testing", "yellow")
        db = SessionTesting()
    else:
        db = SessionPersistent()
    try:
        return db
    finally:
        db.close()

def get_persistent_db():
    db = SessionPersistent()
    try:
        return db
    finally:
        db.close()

app = FastAPI()

app.include_router(projects.router, prefix="/projects", tags=["Projects"])

router = APIRouter();

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://127.0.0.1:3000",
    "127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins = origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)

def log(message, color="green"):
    prefix = colored("[Back-Log]", "green")
    _time = datetime.datetime.now()
    time = colored(f"[{_time.hour}:{_time.minute}:{_time.second}]", "green")

    if(color != "green"):
        message = colored(message, color);

    print(f"{time} {prefix} {message}")

@app.get("/get-tasks", response_model=list[schemas.Task]) 
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    testing: bool = False
):
    db = get_db(testing)
    log("Got Tasks")
    return crud.get_tasks(db, skip=skip, limit=limit)

@app.get("/get-projects", response_model=list[schemas.Project]) 
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    testing: bool = False
):
    db = get_db(testing)
    log("Got Projects")
    return crud.get_projects(db, skip=skip, limit=limit)

@app.post("/add-task/{project_id}") #? new
async def create_task(
    project_id: str,
    task: schemas.TaskCreate,
    testing: bool = False
):
    db = get_db(testing)
    log(f"Created Task: {task.title}")
    db.commit()
    return crud.create_task(db=db, task=task, project_id=project_id)

@app.post("/add-project") 
async def create_project(project: schemas.ProjectCreate, testing: bool = False):
    db = get_db(testing)
    return crud.create_project(db=db, project=project)

@app.post("/add-section")
async def create_section(
    section: schemas.SectionCreate,
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    project_id = request.headers.get("project_id")
    return crud.create_section(db=db, section=section, project_id=project_id)

@app.put("/set-finished")
async def set_finished(task_id: str, testing: bool = False):
    db = get_db(testing)
    # Update Task
    task = crud.get_task(db=db, task_id=task_id)
    task.finished = not task.finished
    db.commit()
    db.refresh(task)
    return task

@app.put("/edit-task")
async def edit_task(
    task: schemas.TaskCreate,
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    log("Changed Task")
    project_id = request.headers.get("project_id")
    section_id = request.headers.get("section_id")
    task_id = request.headers.get("task_id")
    return crud.edit_task(db=db, task=task, project_id=project_id, section_id=section_id, task_id=task_id)

@app.put("/edit-project")
async def edit_project(
    project: schemas.ProjectCreate,
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    log("Changed Project")
    project_id = request.headers.get("project_id")
    return crud.edit_project(db=db, project=project, project_id=project_id)

@app.put("/rename-section")
async def rename_section(
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    log("Renamed Section")
    section_id = request.headers.get("section_id")
    new_title = request.headers.get("new_title")
    return crud.rename_section(db=db, section_id=section_id, new_title=new_title)

@app.delete("/del-task")
async def del_task(
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    log("Deleted Task")
    return crud.del_task(db=db, task_id=request.headers.get("task_id"))

@app.delete("/del-project")
async def del_project(
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    log("Deleted Project")
    return crud.del_project(db=db, project_id=request.headers.get("project_id"))