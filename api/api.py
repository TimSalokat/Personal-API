from __future__ import annotations

from .database import crud, models, schemas
from .database.database import SessionLocal, engine

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os, sys, datetime, random

from termcolor import colored

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
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

Todos = []
Projects = []

def log(message, color="green"):
    prefix = colored("[Back-Log]", "green")
    _time = datetime.datetime.now()
    time = colored(f"[{_time.hour}:{_time.minute}:{_time.second}]", "green")

    if(color != "green"):
        message = colored(message, color);

    print(f"{time} {prefix} {message}")


def Startup():
    try:
        Todos = eval(load_save("todos.txt"))
        Projects = eval(load_save("projects.txt"))
        log("Successfully initialized")
    except:
        with open("saves/todos.txt", "w") as file:
            file.write("[]")
            file.close()
            Todos=eval(load_save("todos.txt"))
        with open("saves/projects.txt", "w") as file:
            file.write("[]")
            file.close()
            Projects=eval(load_save("projects.txt"))

    return Todos, Projects

class Todo(BaseModel):
    uuid: str
    project_uuid: str  

    title: str
    description: str
    priority: int
    finished: bool

class Project(BaseModel):
    uuid: str

    title: str
    description: str
    total: int
    finished: int

    color: str

def getProjectByUuid(uuid):
    for _project in eval(load_save("projects.txt")):
        if _project["uuid"] == uuid:
            return _project    

def getTodoByUuid(uuid):
    for _todo in eval(load_save("todos.txt")):
        if _todo["uuid"] == uuid:
            return _todo    


def save(toSave,fileName):
    path = "saves/" + fileName
    with open(path, "w") as file:
        file.write(str(toSave))
        file.close()

def load_save(fileName):
    path = "saves/" + fileName
    with open(path, "r") as file:
        return file.read() 

@app.get("/ping")
async def ping():
    log("Ping", "green")
    return True

@app.get("/get-tasks") #? new
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    log("Got Tasks")
    return crud.get_tasks(db, skip=skip, limit=limit)
# async def get_todos():
#     log("Got Todos")
#     Todos = eval(load_save("todos.txt"))
#     return {"todos": Todos}

@app.get("/get-projects", response_model=list[schemas.Project]) #? new
# async def get_projects():
#     log("Got Projects")
#     Projects = eval(load_save("projects.txt"))
#     return {"projects": Projects}
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session=Depends(get_db)
):
    log("Got Projects")
    return crud.get_projects(db, skip=skip, limit=limit)

@app.post("/add-task/{project_id}") #? new
async def create_task(
    project_id: str,
    task: schemas.TaskCreate,
     db: Session = Depends(get_db)
):
    return crud.create_task(db=db, task=task, project_id=project_id)

# async def add_todo(todo: Todo):

#     project = getProjectByUuid(todo.project_uuid);
#     project["total"] += 1;

#     Todos.append({
#         "uuid": todo.uuid,
#         "project_uuid": todo.project_uuid,

#         "project_title": project["title"],
#         "project_color": project["color"],

#         "title": todo.title,
#         "description": todo.description,
#         "priority": todo.priority,
#         "finished": todo.finished })
#     log(f"Added Todo: {todo.title} - in Project: {project['title']}", "yellow")
#     save(Todos, "todos.txt")
#     return {"response": "Successful"}

@app.post("/add-project") # ? new
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

# async def add_project(project: Project):
    
#     hexadecimal = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
#     Projects.append({
#         "uuid": project.uuid,
#         "title": project.title.title(),
#         "description": project.description,
#         "total": 0,
#         "finished": 0,
#         "color": hexadecimal,
#     })
#     save(Projects, "projects.txt")
#     log(f"Added Project: {project.title}", "yellow")
#     return {"response": "Successful"}

@app.put("/set-finished")
async def set_finished(uuid: str):

    todo = getTodoByUuid(uuid);

    project = getProjectByUuid(todo["project_uuid"]);
    if(todo["finished"] == False): project["finished"] += 1;
    else: project["finished"] -= 1;  

    todo["finished"] = not todo["finished"]
    log(f"Changed status of: {todo['title']} to {todo['finished']}")
    save(Todos, "todos.txt")
    return {"response": "Successful"}

@app.put("/edit-todo/{uuid}")
async def edit_todo(uuid:str, todo: Todo):
    for todo_item in Todos:
        if(todo_item["uuid"] == uuid):
            todo_item["heading"] = todo.heading
            todo_item["description"] = todo.description
            todo_item["project"] = todo.project
    save(Todos, "todos.txt")
    log(f"Changed Todo {todo.heading}")
    return {"response": "Successful"}

@app.delete("/del-todo")
async def del_todo(uuid: str):
    for todo in Todos:
        if(todo["uuid"] == uuid):
            log(f"Removed {todo['heading']}", "yellow")
            Todos.remove(todo)
    save(Todos, "todos.txt")
    return {"response": "Successful"}

@app.delete("/del-project")
async def del_project(title: str):
    title = title.title()
    for project in Projects:
        if(project["title"] == title):
            log(f"Removed {title}", "yellow")
            Projects.remove(project)
    save(Projects, "projects.txt")
    return {"response": "Successful"}

Todos, Projects = Startup()