from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    token_hash: str = Field(max_length=64, unique=True, index=True)
    expires_at: datetime | None = Field(default=None)
    revoked_at: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
