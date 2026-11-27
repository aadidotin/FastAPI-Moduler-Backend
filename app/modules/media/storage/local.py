import shutil

from pathlib import Path
from fastapi import HTTPException
from app.core.config import settings
from app.modules.media.storage.base import StorageInterface


class LocalStorage(StorageInterface):

    def __init__(self):

        self.root = Path(settings.MEDIA_LOCAL_PATH).resolve()

        self.root.mkdir(parents=True, exist_ok=True)

    def upload(self, file, object_key):

        destination = (self.root / object_key).resolve()

        if not destination.is_relative_to(self.root):
            raise HTTPException(status_code=400, detail="Invalid storage key")

        destination.parent.mkdir(parents=True, exist_ok=True)

        file.seek(0)

        with open(destination, "wb") as output:
            shutil.copyfileobj(file, output)

        return object_key

    def delete(self, object_key):

        destination = (self.root / object_key).resolve()

        if not destination.is_relative_to(self.root):
            raise ValueError("Invalid storage key")

        if destination.exists():
            destination.unlink()

    def get_url(self, object_key, visibility):

        if visibility == "public":
            return f"/media/{object_key}"

        return None

    def get_path(self, object_key):

        destination = (self.root / object_key).resolve()

        if not destination.is_relative_to(self.root):
            raise ValueError("Invalid storage key")

        return destination
