from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from sqlalchemy import Column, DateTime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str | None = Field(default=None)
    email: str = Field(unique=True)
    password_hash: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None),
        sa_column=Column(
            DateTime(),
            nullable=False,
            onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
        ),
    )
