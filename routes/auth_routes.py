from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

import crud
from core.email.utils import send_email, generate_reset_password_email
from core.security import get_password_hash, authenticate_user, create_access_token, generate_password_reset_token, \
    verify_password_reset_token
from crud import get_user_by_email
from models.session import get_session
from models.user import User
from schemas.login import LoginSchema
from schemas.user import UserCreateSchema, UserResponse, NewPassword

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

@auth_router.post("/password-recovery/{email}")
def recover_password(email: str, session: Session = Depends(get_session)):
    user = crud.get_user_by_email(session= session, email=email)

    if user:
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(email_to=user.email, email=email, token=password_reset_token)
        send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content
        )
    return {
        "message": "Se esse e-mail estiver cadastrado, enviamos um link para recuperação de senha."
    }

@auth_router.post("/reset-password/")
def reset_password( body: NewPassword, session: Session = Depends(get_session)):
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Token invalido!")
    user = get_user_by_email(session=session, email=email)
    if not user:
        #A mensagem deve ser a mesma por segurança. Recomendação do criador do FastAPI.
        raise HTTPException(status_code=400, detail="Token invalido!")
    user.password = get_password_hash(body.new_password)
    session.commit()
    #Temporarario. Lembrar de atualizar mais tarde por algo melhor.
    send_email(email_to=email, subject="Senha atualizada", html_content="<p>Sua senha foi atualizada</p>")
    return {
        "mensagem": "Senha atualizada com sucesso!"
    }
