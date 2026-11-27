from fastapi import APIRouter

from app.modules.auth.v1.router import router as auth_router
from app.modules.user.v1.router import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
