
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request 
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
import jwt
from typing import Optional
from termcolor import colored

import uuid, random

from ...database import models, schemas
from ...database.database import get_db

from .users import verify_user, get_user

router = APIRouter();

bearer_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def log(message, color="green"):
    prefix = colored("[Back-Log]", "green")
    _time = datetime.now()
    time = colored(f"[{_time.hour}:{_time.minute}:{_time.second}]", "green")

    if(color != "green"):
        message = colored(message, color);

    print(f"{time} {prefix} {message}")

@router.get("/verify-token")
async def verify(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  
):
    token = credentials.credentials
    username = decode_token(token)
    user = get_user(db=get_db(), username=username)
    
    return {
        "name":user.name,
        "role": user.role}

@router.post("/login", response_model=schemas.Token)
def login(
    user: schemas.UserCreate,
):
    db = get_db()
    response = verify_user(db, user);
    if(response == True):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(
            data={"user": user.name}, expires_delta=access_token_expires
        )
        return schemas.Token(access_token=access_token, token_type="bearer")
     
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    log(f"Decoding token {token}", "yellow")
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], verify_expiration=True)
        print(f"Successfully authorized {decoded_token['user']}")
        print(f"Token of valid until: {datetime.fromtimestamp(decoded_token['exp'])}")
        return decoded_token["user"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def authentication_middleware(request: Request):
    token = request.headers.get('Authorization')
    if token is None:
        raise HTTPException(status_code=401, detail='Missing Authorization')
    try:
        request.state.user_name = decode_token(token)
    except:
        raise HTTPException(status_code=401, detail='Invalid token')
    return True

def authorization_middleware(request: Request):
    username = request.state.user_name
    user = get_user(get_db(), username)
    request.state.user_role = user.role
    if user is None or user.role != 'admin':
        raise HTTPException(status_code=403, detail='Forbidden')
    return True