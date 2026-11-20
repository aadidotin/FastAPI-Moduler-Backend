from fastapi import FastAPI

from app.routers.v1 import router as v1_router

app = FastAPI(
    title="FastAPI backend", description="FastAPI Moduler Backend Development"
)

app.include_router(v1_router, prefix="/api/v1")
