from sqlalchemy.orm import sessionmaker, Session
from .base import db

SessionLocal = sessionmaker(db)


def get_session():
    with SessionLocal() as session:
        yield session
