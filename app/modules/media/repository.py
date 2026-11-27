from sqlmodel import Session, select, delete

from app.modules.media.model import Media


class MediaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Media | None:
        statement = select(Media).where(Media.id == id)
        return self.db.exec(statement).first()

    def create(self, data: Media) -> Media:
        self.db.add(data)
        self.db.flush()
        self.db.refresh(data)

        return data

    def create_many(self, data: list[Media]) -> list[Media]:
        self.db.add_all(data)

        self.db.flush()
        for media in data:
            self.db.refresh(media)

        return data

    def delete(self, id: int) -> None:
        statement = delete(Media).where(Media.id == id)

        self.db.exec(statement)
        self.db.flush

    def delete_many(self, ids: list[int]) -> None:
        statement = delete(Media).where(Media.id.in_(ids))

        self.db.exec(statement)
        self.db.flush
