from __future__ import annotations

from .database import models, schemas
from .database.database import SessionTesting, SessionPersistent, testing_engine, persistent_engine, get_db

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sqlalchemy.orm import Session

import os, sys, datetime, random
from starlette.requests import Request 

from termcolor import colored

from .routes.task_tracker import projects, tasks, sections

models.Base.metadata.create_all(bind=testing_engine)
models.Base.metadata.create_all(bind=persistent_engine)

def get_persistent_db():
    db = SessionPersistent()
    try:
        return db
    finally:
        db.close()

app = FastAPI()

app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(sections.router, prefix="/sections", tags=["Sections"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

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