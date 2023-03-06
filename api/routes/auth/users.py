
from fastapi import APIRouter, Depends
from starlette.requests import Request 
from sqlalchemy.orm import Session

from passlib.context import CryptContext
import uuid, random

from ...database import models, schemas
from ...database.database import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post("/add")
async def add(
    user: schemas.UserCreate,
):
    db = get_db()
    hashed_pwd = pwd_context.hash(user.password);
    db_user = models.User(
        name=user.name,
        password=hashed_pwd,
        role="user",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db, username):
    return db.query(models.User).filter(models.User.name == username).first()

def verify_password(plain_pwd, hashed_pwd):
    if(pwd_context.verify(plain_pwd, hashed_pwd)):
        return True

def verify_user(db, user):
    _user = get_user(db, user.name)
    if(not _user):
        return "User not found"
    if(verify_password(user.password, _user.password)):
        return True;
    return "Wrong password"