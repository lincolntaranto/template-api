from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import get_password_hash
from models import User
from schemas.user import UserUpdatePasswordSchema


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """Procura o usuário pelo email fornecido.

    Args:
        session (Session): sessão do banco de dados.
        email (str): email a ser procurado.

    Returns:
        User: retorna o usuário caso seja encontrado.
        None: caso não encontrado retorna None.
    """
    session_user = session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()
    return session_user


def change_password(
    *, session: Session, user_update_password: UserUpdatePasswordSchema, user: User
) -> User:
    hashed_password = get_password_hash(user_update_password.new_password)
    user.password = hashed_password
    session.add(user)
    session.commit()
    return user


def delete_account(*, session: Session, user: User) -> None:
    session.delete(user)
    session.commit()
    return None
