from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .loan import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./loans.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)
