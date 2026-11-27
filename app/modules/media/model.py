from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

from app.modules.user.model import User


class MediaVisibility(Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    S3 = "s3"
    AZURE = "azure"


class Media(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_url: str
    file_path: str
    mime_type: str
    original_name: str
    visibility: MediaVisibility = Field(
        default="private",
        sa_column=Column(
            SQLAlchemyEnum(
                MediaVisibility,
                values_callable=lambda enum: [item.value for item in enum],
            ),
            nullable=False,
        ),
    )
    user_id: int | None = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: User | None = Relationship(back_populates="media")
