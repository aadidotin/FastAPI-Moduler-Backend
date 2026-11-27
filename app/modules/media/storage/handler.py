from app.core.config import settings

from app.modules.media.storage.local import LocalStorage


class StorageManager:

    def __init__(self):
        self.providers = {
            "local": LocalStorage(),
        }

    def get_storage(self, backend: str):
        storage = self.providers.get(backend)

        if storage is None:
            raise ValueError("Unsupported storage backend")

        return storage

    @property
    def default_backend(self):
        return settings.MEDIA_STORAGE_BACKEND
