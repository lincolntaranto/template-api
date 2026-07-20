from sqlalchemy.orm import Session

from core.security import get_password_hash
from models import User
from schemas.user import UserCreateSchema


def create_user(*, session: Session, user_create_schema: UserCreateSchema) -> User:
    password_hash = get_password_hash(user_create_schema.password)
    new_user = User(
        name=user_create_schema.name,
        password=password_hash,
        email=user_create_schema.email,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
