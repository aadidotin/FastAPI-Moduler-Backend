from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional

from app.modules.user.v1.schema import UserResponse


class RegisterRequest(SQLModel):
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    password: str = Field(min_length=8)


class AuthenticateResponse(SQLModel):
    user: UserResponse
