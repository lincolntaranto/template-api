from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int

    model_config = {"env_file": ".env"}

settings = Settings()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
