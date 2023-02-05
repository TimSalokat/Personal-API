from __future__ import annotations

from .database import crud, models, schemas
from .database.database import SessionTesting, SessionPersistent, testing_engine, persistent_engine

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os, sys, datetime, random
from starlette.requests import Request 

from termcolor import colored

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

@app.get("/ping")
async def ping():
    log("Ping", "green")
    return True

@app.get("/get-tasks", response_model=list[schemas.Task]) #? new
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    testing: bool = False
):
    db = get_db(testing)
    log("Got Tasks")
    return crud.get_tasks(db, skip=skip, limit=limit)

@app.get("/get-projects", response_model=list[schemas.Project]) #? new
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
    project = crud.get_project(db=db, project_id=project_id)
    project.total_tasks = project.total_tasks + 1
    db.commit()
    return crud.create_task(db=db, task=task, project_id=project_id)

@app.post("/add-project") # ? new
async def create_project(project: schemas.ProjectCreate, testing: bool = False):
    db = get_db(testing)
    return crud.create_project(db=db, project=project)

@app.put("/set-finished") # ?new
async def set_finished(task_id: str, testing: bool = False):
    db = get_db(testing)
    # Update Task
    task = crud.get_task(db=db, task_id=task_id)
    task.finished = not task.finished

    # Update Project
    project = crud.get_project(db=db, project_id=task.project_id)
    if(task.finished): project.finished_tasks = project.finished_tasks + 1
    else: project.finished_tasks = project.finished_tasks - 1
    db.commit();


@app.put("/edit-task") #? new
async def edit_task(
    task: schemas.TaskCreate,
    request: Request,
    testing: bool = False
):
    db = get_db(testing)
    log("Changed Task")
    project_id = request.headers.get("project_id")
    task_id = request.headers.get("task_id")
    return crud.edit_task(db=db, task=task, project_id=project_id, task_id=task_id)

@app.delete("/del-todo")
#! Need rework to work with sqlite
# async def del_todo(uuid: str):
#     for todo in Todos:
#         if(todo["uuid"] == uuid):
#             log(f"Removed {todo['heading']}", "yellow")
#             Todos.remove(todo)
#     save(Todos, "todos.txt")
#     return {"response": "Successful"}

@app.delete("/del-project")
async def placeholder():
    pass
#! Need rework to work with sqlite
# async def del_project(title: str):
#     title = title.title()
#     for project in Projects:
#         if(project["title"] == title):
#             log(f"Removed {title}", "yellow")
#             Projects.remove(project)
#     save(Projects, "projects.txt")