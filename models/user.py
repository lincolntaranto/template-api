from sqlalchemy import Column, Integer, String, Boolean, Text

from base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    admin = Column(Boolean, default=False, nullable=False)