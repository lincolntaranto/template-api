from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User


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
