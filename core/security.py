import uuid
from datetime import timedelta, datetime, timezone
from typing import Any

from fastapi import Depends, HTTPException
import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import oauth2_schema, settings
from models.session import get_session
from models.user import User

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


ALGORITHM = "HS256"

DUMMY_HASH = "$argon2i$v=19$m=16,t=2,p=1$Uzd6Ym82c25XcW1iVkZNdQ$QMAWuZp748LzlKi+9Umv9w"


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": str(subject), "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(
    token: str = Depends(oauth2_schema), session: Session = Depends(get_session)
) -> User:
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        id_user = uuid.UUID(dict_info["sub"])
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Acesso negado!")
    user = session.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso negado!")
    return user


def authenticate_user(email: EmailStr, password: str, session: Session) -> User | bool:
    user = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    elif not verify_password(password, user.password):
        return False
    return user


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return str(decoded_token["sub"])
    except InvalidTokenError:
        return None
