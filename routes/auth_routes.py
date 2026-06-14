from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.email.utils import send_email
from core.security import get_password_hash, authenticate_user, create_access_token
from models.session import get_session
from models.user import User
from schemas.login import LoginSchema
from schemas.user import UserCreateSchema, UserResponse

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/create_user", response_model=UserResponse)
def create_user(user_create_schema: UserCreateSchema, session: Session = Depends(get_session)):
    user = session.execute(select(User).where(User.email == user_create_schema.email)).scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="email já cadastrado!")
    password_hash = get_password_hash(user_create_schema.password)
    new_user = User(
        name = user_create_schema.name,
        password = password_hash,
        email = user_create_schema.email
    )
    send_email(email_to=new_user.email, subject="Conta Criada com sucesso!", html_content="<p>Email funcionando!</p>")
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@auth_router.post("/login")
def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    else:
        access_token = create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

@auth_router.post("/login-form")
def login_form(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form.username, form.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    else:
        access_token = create_access_token(user.id)
    return{
        "access_token": access_token,
        "token_type": "Bearer"
    }