
import sys, os

from fastapi import APIRouter

from ...database import crud, models, schemas
from ...database.database import get_db

router = APIRouter();

@router.get("/get-projects")
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    testing: bool = False
):
    db = get_db(testing)
    return crud.get_projects(db, skip=skip, limit=limit)