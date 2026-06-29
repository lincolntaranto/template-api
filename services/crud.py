from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User


def get_user_by_email(*, session: Session, email: str) -> User | None:
    session_user = session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()
    return session_user


def get_username_by_email(*, session: Session, email: str) -> str | None:
    session_user = session.execute(
        select(User.name).where(User.email == email)
    ).scalar_one_or_none()
    return session_user
