from sqlmodel import SQLModel
from pydantic import EmailStr, Field

from app.core.config import settings
from app.modules.user.v1.schema import UserResponse


class RegisterRequest(SQLModel):
    name: str = Field(min_length=1)
    email: str = EmailStr
    password: str = Field(min_length=8, max_length=16)


class LoginRequest(SQLModel):
    email: str = EmailStr
    password: str


class TokenRefreshRequest(SQLModel):
    old_refresh_token: str


class TokenResponse(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


class AuthResponse(SQLModel):
    user: UserResponse
    token: TokenResponse
