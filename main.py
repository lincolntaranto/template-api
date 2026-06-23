from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from core.config import settings
from routes.auth_routes import auth_router
from routes.user_routes import user_router

limiter = Limiter(
    key_func=get_remote_address,
    strategy="fixed-window",
    storage_options={"uri": "memory://"}
)


app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(auth_router)
app.include_router(user_router)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
