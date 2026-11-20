from app.modules.user.model import User
from app.modules.user.repository import UserRepository


class AuthSerivce:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, data) -> User:
        pass

    def login(self, data) -> User:
        pass


class TokenService:
    def __init__(self):
        pass
