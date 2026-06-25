from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise ValueError("DATABASE_URL não encontrada.")

db = create_engine(db_url)


class Base(DeclarativeBase):
    pass
