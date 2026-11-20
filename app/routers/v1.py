from fastapi import APIRouter

from app.modules.auth.v1.router import router as auth_router

router = APIRouter()

# Include Routers
router.include_router(auth_router)
