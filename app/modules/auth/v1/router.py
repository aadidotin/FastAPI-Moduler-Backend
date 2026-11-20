from fastapi import APIRouter

from app.modules.auth.v1.schema import RegisterRequest, AuthenticateResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(payload: RegisterRequest):
    print(payload)
