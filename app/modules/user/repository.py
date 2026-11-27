from sqlmodel import Session, select

from app.core.security import hash_password
from app.modules.user.model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.exec(statement=statement).first()

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.exec(statement=statement).first()

    def create(self, user_data) -> User:
        user = User(**user_data.model_dump())
        user.hash_password = hash_password(user_data.password)

        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)

        return user

    def update(self, user: User, user_data) -> User:
        update_data = user_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)

        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.flush()
