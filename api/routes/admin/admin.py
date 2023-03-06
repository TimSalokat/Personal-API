
from fastapi import APIRouter, Depends
from starlette.requests import Request 
from sqlalchemy.orm import Session

from passlib.context import CryptContext
import uuid, random

from ...database import models, schemas
from ...database.database import get_db

from ..auth import auth

router = APIRouter()

@router.get("/get-users",
    dependencies=[Depends(auth.authentication_middleware), Depends(auth.authorization_middleware)])
async def get():
    db = get_db()
    return db.query(models.User).all()