from fastapi import HTTPException, status

from app.modules.auth.v1.schema import RegisterRequest
from app.modules.user.model import User
from app.modules.user.repository import UserRepository


class AuthSerivce:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, data: RegisterRequest) -> User:
        user = self.user_repo.get_by_email(email=data.email)

        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already taken"
            )

        new_user = User(**data.model_dump())
        return self.user_repo.create(new_user)

    def login(self, data) -> User:
        pass


class TokenService:
    def __init__(self):
        pass
