from fastapi import FastAPI

from app.core.config import settings
from app.routers.v1 import router as v1_router

app = FastAPI(
    title="FastAPI backend",
    description="FastAPI Moduler Backend Development",
    debug=settings.DEBUG,
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"success": True, "message": "Application is running"}
