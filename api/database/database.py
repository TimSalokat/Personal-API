from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TESTING_DATABASE_URL = "sqlite:///./testing.db"
PERSISTENT_DATABASE_URL = "sqlite:///./persistent.db"

testing_engine = create_engine(
    TESTING_DATABASE_URL, connect_args={"check_same_thread": False}
)
persistent_engine = create_engine(
    PERSISTENT_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)
SessionPersistent = sessionmaker(autocommit=False, autoflush=False, bind=persistent_engine)

Base = declarative_base()