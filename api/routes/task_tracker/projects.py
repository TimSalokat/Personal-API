
import sys

from fastapi import APIRouter

sys.path.append("../../database");

from database import crud, models, schemas
from database.database import SessionTesting, SessionPersistent, testing_engine, persistent_engine

router = APIRouter();

@router.get("/get-projects")
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    testing: bool = False
):
    db = get_db(testing)
    return crud.get_projects(db, skip=skip, limit=limit)