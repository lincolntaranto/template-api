from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import verify_access_token, verify_password, get_password_hash
from models import User
from models.session import get_session
from schemas.user import UserResponse, UserUpdatePasswordSchema

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