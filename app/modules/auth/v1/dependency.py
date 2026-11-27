from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import decode_access_token
from app.modules.auth.v1.service import AuthService
from app.modules.user.model import User
from app.modules.user.repository import UserRepository

# oauth_schema = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_session)) -> AuthService:
    return AuthService(db=db)


def get_current_user(
    # token: str = Depends(oauth_schema),
    # db: Session = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session),
) -> User:
    # access_token = decode_access_token(token=token)
    access_token = decode_access_token(token=token.credentials)

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(int(access_token.get("sub")))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
