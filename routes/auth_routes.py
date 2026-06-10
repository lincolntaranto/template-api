from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import get_password_hash
from models.session import get_session
from models.user import User
from schemas.user import UserCreateSchema, UserResponse

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/create_user", response_model=UserResponse)
async def create_user(user_create_schema: UserCreateSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == user_create_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="email já cadastrado!")
    else:
        password_hash = get_password_hash(user_create_schema.password)
        new_user = User(
            name = user_create_schema.name,
            password = password_hash,
            email = user_create_schema.email
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return{
            new_user
        }