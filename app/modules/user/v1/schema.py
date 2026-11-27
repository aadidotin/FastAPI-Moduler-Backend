from sqlmodel import SQLModel
from datetime import datetime


class UserResponse(SQLModel):
    id: int
    name: str
    email: str
    created_at: datetime


class UpdateUserRequest(SQLModel):
    name: str
