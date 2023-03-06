from __future__ import annotations

from .database import models, schemas
from .database.database import base_engine, get_db

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sqlalchemy.orm import Session

import os, sys, datetime, random
from starlette.requests import Request 

from termcolor import colored

from .routes.task_tracker import projects, tasks, sections
from .routes.auth import auth, users
from .routes.admin import admin

models.Base.metadata.create_all(bind=base_engine)

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["Admin Routes"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["User Management"])

app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(sections.router, prefix="/sections", tags=["Sections"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

router = APIRouter()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://127.0.0.1:3000",
    "127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)

def add_admin(db):
    if(users.get_user(db, "admin")):
        return
    else:
        hashed_pwd = users.pwd_context.hash("admin");
        db_user = models.User(
            name="admin",
            password=hashed_pwd,
            role="admin",)
        db.add(db_user)
        db.commit()
        db.refresh(db_user) 

add_admin(get_db())

def log(message, color="green"):
    prefix = colored("[Back-Log]", "green")
    _time = datetime.datetime.now()
    time = colored(f"[{_time.hour}:{_time.minute}:{_time.second}]", "green")

    if(color != "green"):
        message = colored(message, color);

    print(f"{time} {prefix} {message}")