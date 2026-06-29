from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from services import crud
from core.email.utils import (
    send_email,
    generate_reset_password_email,
    generate_new_account_email,
    generate_update_password_email,
)
from core.security import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    generate_password_reset_token,
    verify_password_reset_token,
)
from services.crud import get_user_by_email
from core.limiter import limiter
from models.session import get_session
from models.user import User
from schemas.login import LoginSchema
from schemas.user import UserCreateSchema, UserResponse, NewPassword

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/create_user", response_model=UserResponse)
@limiter.limit("2/minute", per_method=True)
def create_user(
    request: Request,
    user_create_schema: UserCreateSchema,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """Criar um usuário"""
    user = get_user_by_email(session=session, email=user_create_schema.email)
    if user:
        raise HTTPException(status_code=400, detail="email já cadastrado!")
    password_hash = get_password_hash(user_create_schema.password)
    new_user = User(
        name=user_create_schema.name,
        password=password_hash,
        email=user_create_schema.email,
    )
    email_data = generate_new_account_email(email_to=new_user.email)
    session.add(new_user)
    session.commit()
    background_tasks.add_task(
        send_email,
        email_to=new_user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    session.refresh(new_user)
    return new_user


@auth_router.post("/login")
@limiter.limit("5/minute", per_method=True)
def login(
    request: Request, login_schema: LoginSchema, session: Session = Depends(get_session)
):
    """Rota para login"""
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    else:
        access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "Bearer"}


@auth_router.post("/login-form")
@limiter.limit("5/minute", per_method=True)
def login_form(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(form.username, form.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    else:
        access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "Bearer"}


@auth_router.post("/password-recovery/{email}")
@limiter.limit("3/hour", per_method=True)
def recover_password(
    request: Request, email: str, session: Session = Depends(get_session)
):
    """Rota para enviar email de recuperação de senha"""
    user = crud.get_user_by_email(session=session, email=email)

    if user:
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )
        send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return {
        "message": "Se esse e-mail estiver cadastrado, enviamos um link para recuperação de senha."
    }


@auth_router.post("/reset-password")
@limiter.limit("5/minute", per_method=True)
def reset_password(
    request: Request, body: NewPassword, session: Session = Depends(get_session)
):
    """Rota para trocar a senha"""
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Token invalido!")
    user = get_user_by_email(session=session, email=email)
    if not user:
        # A mensagem deve ser a mesma por segurança. Recomendação do criador do FastAPI.
        raise HTTPException(status_code=400, detail="Token invalido!")
    user.password = get_password_hash(body.new_password)
    session.commit()
    email_data = generate_update_password_email(user=user.name)
    send_email(
        email_to=email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return {"mensagem": "Senha atualizada com sucesso!"}
