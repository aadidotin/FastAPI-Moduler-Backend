from sqlmodel import SQLModel, Field
from datetime import datetime, UTC


class RefreshToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    token_hash: str = Field(max_length=64, unique=True, index=True)
    expired_at: datetime
    revoked_at: datetime | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
