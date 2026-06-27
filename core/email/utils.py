import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Template

from core.config import settings

import resend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (Path(__file__).parent / "build" / template_name).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(*, email_to: str, subject: str = "", html_content: str = "") -> None:
    assert (
        settings.emails_enabled
    ), "Nenhuma configuração fornecida para variáveis de e-mail"
    address = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    params: resend.Emails.SendParams = {
        "from": address,
        "to": [email_to],
        "subject": subject,
        "html": html_content,
    }
    response = resend.Emails.send(params)
    logger.info(f"send email result: {response}")


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Recuperação de senha do usuário {email}!"
    link = f"{settings.FRONTEND_HOST}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Nova Conta!"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "link": settings.FRONTEND_HOST,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_old_email(email_to: str, new_email: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Email Alterado!"
    html_content = render_email_template(
        template_name="old_email_update.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "username": email_to,
            "new_email": new_email,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_update_email(new_email: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Novo Email!"
    html_content = render_email_template(
        template_name="email_update.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": new_email,
            "new_email": new_email,
        },
    )
    return EmailData(html_content=html_content, subject=subject)
