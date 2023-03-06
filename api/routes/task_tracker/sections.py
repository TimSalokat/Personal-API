
import sys, os

from fastapi import APIRouter, Depends
from starlette.requests import Request 
from sqlalchemy.orm import Session

import uuid, random

from ...database import models, schemas
from ...database.database import get_db

from ..auth import auth

router = APIRouter()

@router.post("/add",
    dependencies=[Depends(auth.authentication_middleware)])
async def add(
    section: schemas.SectionCreate,
    request: Request
):
    db = get_db()
    project_id = request.headers.get("project_id")
    return create_section(db=db, section=section, project_id=project_id)

@router.put("/edit",
    dependencies=[Depends(auth.authentication_middleware)])
async def edit(
    request: Request,
):
    db = get_db()
    section_id = request.headers.get("section_id")
    new_title = request.headers.get("new_title")
    return rename_section(db=db, section_id=section_id, new_title=new_title)



def get_section(db:Session, section_id:str):
    return db.query(models.Section).filter(models.Section.id == section_id).first();

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

def rename_section(db: Session, section_id: str, new_title=str):
    db_changed = get_section(db=db, section_id=section_id)
    db_changed.title = new_title

    db.commit()
    db.refresh(db_changed)
    return db_changed