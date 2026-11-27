from fastapi import HTTPException, status
from sqlmodel import Session
from datetime import datetime, timezone
import jwt

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_refresh_token,
    verify_password,
)
from app.modules.user.model import User
from app.modules.auth.model import RefreshToken
from app.modules.user.repository import UserRepository
from app.modules.auth.repository import AuthRepository
from app.modules.auth.v1.schema import RegisterRequest, LoginRequest, TokenResponse
from app.exceptions.custom import InvalidRefreshTokenError


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.auth_repo = AuthRepository(db)

    def register(self, data: RegisterRequest) -> tuple[User, TokenResponse]:
        try:
            user = self.user_repo.get_by_email(email=data.email)

            if user is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already taken."
                )

            user = self.user_repo.create(data)

            token = self._generate_tokens(user=user)

            self.db.commit()

            return user, token
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def login(self, data: LoginRequest) -> tuple[User, TokenResponse]:
        try:
            user = self.user_repo.get_by_email(email=data.email)

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials.",
                )

            if not verify_password(data.password, user.hash_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials.",
                )

            token = self._generate_tokens(user=user)

            self.db.commit()

            return user, token
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def _generate_tokens(self, user: User) -> TokenResponse:

        if user.id is None:
            raise ValueError("User must be presisted before generating token.")

        access_token = create_access_token(user_id=user.id)
        refresh_token = create_refresh_token(user_id=user.id)

        # Decode refresh_token
        payload = decode_refresh_token(token=refresh_token)

        # Extract refresh_token's expiry for DB insertion
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        token_hash = hash_refresh_token(token=refresh_token)

        refresh_token_instance = RefreshToken(
            user_id=user.id, token_hash=token_hash, expires_at=expires_at
        )

        self.auth_repo.create_refresh_token(refresh_token_instance)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh_tokens(self, old_refresh_token: str) -> TokenResponse:
        try:
            # 1. Validate JWT signature, expiry and token type.
            payload = decode_refresh_token(old_refresh_token)

            # 2. Hash the incoming refresh token.
            old_token_hash = hash_refresh_token(old_refresh_token)

            # 3. Find and lock its database record.
            stored_token = self.auth_repo.get_by_token_hash(old_token_hash)

            if stored_token is None:
                raise InvalidRefreshTokenError("Invalid refresh token.")

            now = datetime.now(timezone.utc)

            # 4. Check revocation and database expiry.
            if stored_token.revoked_at is not None:
                raise InvalidRefreshTokenError(
                    "Refresh token has already been used or revoked."
                )

            if stored_token.expires_at <= now:
                raise InvalidRefreshTokenError("Refresh token has expired.")

            # 5. Verify the user still exists and is active.
            user = self.user_repo.get_by_id(user_id=stored_token.user_id)

            if user is None:
                raise InvalidRefreshTokenError("User is unavailable.")

            if payload["sub"] != str(user.id):
                raise InvalidRefreshTokenError("Invalid refresh token.")

            # 6. Revoke the old refresh token.
            self.auth_repo.revoke_refresh_token(stored_token, revoked_at=now)

            # 7. Prepare token & response.
            response = self._generate_tokens(user=user)

            # 8. Commit revocation and insertion together.
            self.db.commit()

            return response
        except InvalidRefreshTokenError:
            self.db.rollback()
            raise

        except jwt.InvalidTokenError as exc:
            self.db.rollback()
            raise InvalidRefreshTokenError("Invalid or expired refresh token.")

        except Exception as exc:
            self.db.rollback()
            raise
