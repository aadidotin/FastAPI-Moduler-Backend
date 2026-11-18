from sqlmodel import SQLModel
from datetime import datetime


class UserResponse(SQLModel):
    id: int
    first_name: str
    last_name: str | None
    email: str
    is_active: bool
    created_at: datetime
