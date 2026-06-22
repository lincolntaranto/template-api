from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import Settings, settings
from routes.auth_routes import auth_router
from routes.user_routes import user_router

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
