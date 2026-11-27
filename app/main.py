from fastapi import FastAPI

from app.core.config import settings

# from app.exceptions.register import register_exception_handlers
from app.exceptions.handler import register_exception_handlers

from app.routers.v1 import router as v1_router

app = FastAPI(
    title="FastAPI backend",
    description="FastAPI Moduler Backend Development",
    debug=settings.DEBUG,
)

app.include_router(v1_router, prefix="/api/v1")


register_exception_handlers(app=app)
