import uuid

from sqlalchemy import Column, Integer, String, Boolean, Text, UUID

from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    admin = Column(Boolean, default=False, nullable=False)