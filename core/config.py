from typing import Self

from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr, model_validator, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int
    FRONTEND_HOST: str

    PROJECT_NAME: str

    SMTP_HOST: str | None = None
    SMTP_PORT: int
    SMTP_TLS: bool
    SMTP_SSL: bool
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    BACKEND_CORS_ORIGINS: list[str] = []

    model_config = {"env_file": ".env"}

settings = Settings()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
