from fastapi import UploadFile
from sqlmodel import Session
from uuid import uuid4
from pathlib import Path

from app.modules.user.model import User
from app.modules.user.repository import UserRepository
from app.modules.media.v1.validator import MediaValidator
from app.modules.media.repository import MediaRepository
from app.modules.media.model import Media, MediaVisibility
from app.modules.media.storage.handler import StorageManager


class MediaService:
    def __init__(self, db: Session):
        self.db = db
        self.media_repo = MediaRepository(db)
        self.user_repo = UserRepository(db)
        self.storage_manager = StorageManager()

    def upload_multiple(
        self,
        files: list[UploadFile],
        user: User,
        visibility: MediaVisibility = MediaVisibility.PRIVATE,
    ) -> list[Media]:
        try:
            validated = MediaValidator.validate_files(files)

            backend = self.storage_manager.default_backend
            storage = self.storage_manager.get_storage(backend)

            uploaded_keys = []
            media_records = []

            for item in validated:
                file = item["file"]

                object_key = f"media/{uuid4()}" f"{item["extension"]}"

                storage.upload(file=file.file, object_key=object_key)

                uploaded_keys.append(object_key)

                media_records.append(
                    Media(
                        file_path="/adf",
                        file_url="asdf",
                        mime_type=item["mime_type"],
                        visibility=visibility,
                        user_id=user.id,
                    )
                )

            response = self.media_repo.create_many(data=media_records)

            self.db.commit()

            return response
        except Exception:
            self.db.rollback()
            pass
