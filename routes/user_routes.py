from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.email.utils import send_email
from core.security import verify_access_token, verify_password, get_password_hash
from models import User
from models.session import get_session
from schemas.user import UserResponse, UserUpdatePasswordSchema, UserUpdateEmailSchema, UserUpdateNameSchema

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/me", response_model=UserResponse)
def get_me(current_user : User = Depends(verify_access_token)):
    return current_user

@user_router.patch("/password")
def update_password(user_update_password: UserUpdatePasswordSchema,
                          user: User = Depends(verify_access_token),
                          session: Session = Depends(get_session)):
    verify = verify_password(user_update_password.current_password, user.password)
    if not verify:
        raise HTTPException(status_code=401, detail="Senha incorreta!")
    if user_update_password.current_password == user_update_password.new_password:
        raise HTTPException(status_code=400, detail="A nova senha não pode ser igual a antiga!")
    hashed_password = get_password_hash(user_update_password.new_password)
    user.password = hashed_password
    session.add(user)
    session.commit()
    return{
        "mensagem": "Senha atualizada com sucesso!"
    }

@user_router.patch("/email")
def update_email(user_update_email: UserUpdateEmailSchema,
                 user: User = Depends(verify_access_token),
                 session: Session = Depends(get_session)):
    verify = verify_password(user_update_email.current_password, user.password)
    if not verify:
        raise HTTPException(status_code=401, detail="Senha incorreta!")
    if user.email == user_update_email.new_email:
        raise HTTPException(status_code=400, detail="O novo email não pode ser igual ao antigo!")
    existing = session.execute(select(User).where(User.email == user_update_email.new_email)).scalar_one_or_none()
    if existing:
        HTTPException(status_code=400, detail="Email já cadastrado!")
    email_antigo = user.email
    user.email = user_update_email.new_email
    session.add(user)
    session.commit()
    session.refresh(user)
    #Lembrar de melhorar o HTML content mais tarde.
    send_email(email_to=email_antigo,
               subject="Atenção: Seu email foi atualizado!",
               html_content=f"<p>Seu email foi atualizado para {user.email}</p>")
    send_email(email_to=user.email,
               subject="Email Atualizado!",
               html_content="<p>Email atualizado com sucesso!</p>")
    return{
        "mensagem": "Email atualizado com sucesso!"
    }

@user_router.patch("/username")
def update_username(user_update_name: UserUpdateNameSchema,
                    user: User = Depends(verify_access_token),
                    session: Session = Depends(get_session)):
    verify = verify_password(user_update_name.current_password, user.password)
    if not verify:
        raise HTTPException(status_code=401, detail="Senha incorreta!")
    user.name = user_update_name.new_name
    session.commit()
    session.refresh(user)
    return{
        "mensagem": "Nome atualizado com sucesso!"
    }