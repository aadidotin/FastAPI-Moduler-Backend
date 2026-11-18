from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import datetime


class UserCreateRequest(SQLModel):
    first_name: str
    last_name: str | None
    email: EmailStr
    password: str


class UserResponse(SQLModel):
    id: int
    first_name: str
    last_name: str | None
    email: str
    is_active: bool
    created_at: datetime
