from pwdlib import PasswordHash
from datetime import datetime, timedelta, UTC
from uuid import uuid4

import jwt
import hashlib

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(password=plain_password, hash=hashed_password)


def _create_token(
    user_id: int, token_type: str, secret_key: str, expires_delta: timedelta
) -> str:
    now = datetime.now(UTC)

    payload = {
        "sub": str(user_id),
        "type": token_type,
        "jti": str(uuid4()),
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(payload, secret_key, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: int) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return _create_token(
        user_id=user_id,
        token_type="access",
        secret_key=settings.JWT_ACCESS_SECRET_KEY,
        expires_delta=expires_delta,
    )


def create_refresh_token(user_id: int) -> str:
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    return _create_token(
        user_id=user_id,
        token_type="refresh",
        secret_key=settings.JWT_REFRESH_SECRET_KEY,
        expires_delta=expires_delta,
    )


def _decode_token(token: str, token_type: str, secret_key: str) -> dict:
    payload = jwt.decode(token, secret_key, algorithms=[settings.JWT_ALGORITHM])

    if payload.get("type") != token_type:
        raise jwt.InvalidTokenError("Invalid token type")

    subject = payload.get("sub")

    if not isinstance(subject, str) or not subject.isdigit():
        raise jwt.InvalidTokenError("Invalid token subject")

    return payload


def decode_access_token(token: str) -> dict:
    return _decode_token(
        token=token, token_type="access", secret_key=settings.JWT_ACCESS_SECRET_KEY
    )


def decode_refresh_token(token: str) -> dict:
    return _decode_token(
        token=token, token_type="refresh", secret_key=settings.JWT_REFRESH_SECRET_KEY
    )


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
