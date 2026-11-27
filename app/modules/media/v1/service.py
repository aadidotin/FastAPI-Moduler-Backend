from fastapi import UploadFile
from sqlmodel import Session

from app.modules.user.model import User
from app.modules.user.repository import UserRepository
from app.modules.media.v1.validator import MediaValidator
from app.modules.media.repository import MediaRepository
from app.modules.media.model import Media, MediaVisibility


class MediaService:
    def __init__(self, db: Session):
        self.db = db
        self.media_repo = MediaRepository(db)
        self.user_repo = UserRepository(db)

    def upload_multiple(
        self,
        files: list[UploadFile],
        user: User,
        visibility: MediaVisibility = MediaVisibility.PRIVATE,
    ) -> list[Media]:
        try:
            validated = MediaValidator.validate_files(files)
            pass
        except Exception:
            self.db.rollback()
            pass
