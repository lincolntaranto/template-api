from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv

from core.config import settings

load_dotenv()

db_url = settings.DATABASE_URL

if not db_url:
    raise ValueError("DATABASE_URL não encontrada.")

db = create_engine(db_url)


class Base(DeclarativeBase):
    pass
