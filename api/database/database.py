from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from termcolor import colored

BASE_DATABASE_URL = "sqlite:///./database.db"

base_engine = create_engine(
    BASE_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=base_engine)

Base = declarative_base()

def get_db():
    db = SessionMaker()
    try:
        return db
    finally:
        db.close()