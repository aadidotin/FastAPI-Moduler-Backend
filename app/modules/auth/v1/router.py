from fastapi import APIRouter, Depends

from app.modules.auth.v1.schema import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    TokenRefreshRequest,
    TokenResponse,
)
from app.modules.auth.v1.service import AuthService
from app.modules.auth.v1.dependency import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse)
async def register(
    payload: RegisterRequest, service: AuthService = Depends(get_auth_service)
):
    user, token = service.register(payload)

    return AuthResponse(user=user, token=token)


@router.post("/login", response_model=AuthResponse)
async def login(
    payload: LoginRequest, service: AuthService = Depends(get_auth_service)
):
    user, token = service.login(payload)

    return AuthResponse(user=user, token=token)


@router.post("/refresh", response_model=TokenResponse)
async def token_refresh(
    payload: TokenRefreshRequest, service: AuthService = Depends(get_auth_service)
):
    token = service.refresh_tokens(old_refresh_token=payload.old_refresh_token)

    return token
