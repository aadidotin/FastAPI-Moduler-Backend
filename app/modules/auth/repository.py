from sqlmodel import Session, select
from datetime import datetime

from app.modules.auth.model import RefreshToken


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        self.db.flush()
        self.db.refresh(refresh_token)

        return refresh_token


    def revoke_active_refresh_token(self) -> None:
        pass


    def create_refresh_token(
        self,
        refresh_token: RefreshToken
    ) -> RefreshToken:

        self.db.add(refresh_token)
        self.db.flush()
        self.db.refresh(refresh_token)

        return refresh_token

    def get_by_token_hash(
        self,
        token_hash: str
    ) -> RefreshToken | None:

        statement = (
            select(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .with_for_update()
        )

        return self.db.exec(statement).first()

    def revoke_refresh_token(
        self,
        refresh_token: RefreshToken,
        revoked_at: datetime
    ) -> RefreshToken:

        refresh_token.revoked_at = revoked_at

        self.db.add(refresh_token)
        self.db.flush()

        return refresh_token
