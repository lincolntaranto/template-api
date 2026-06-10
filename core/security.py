from datetime import timedelta, datetime, timezone
from typing import Any

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from core.config import oauth2_schema, settings
from models.session import get_session
from models.user import User

password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return password_hash.hash(password)

ALGORITHM = "HS256"

def create_access_token(subject: str | Any, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": str(subject),
        "exp": expire
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEYS, algorithms=[ALGORITHM])
        id_user = int(dict_info["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado!")
    user = session.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso negado!")
    return user