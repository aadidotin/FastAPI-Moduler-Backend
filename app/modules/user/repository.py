from sqlmodel import Session, select

from app.modules.user.model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.exec(statement).first()

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.exec(statement).first()

    def create(self, user_data) -> User:
        user = User(**user_data.model_dump())

        self.db.add(user)
        self.db.flush()
        self.db.refresh()

        return user

    def update(self, user: User, user_data) -> User:
        pass
