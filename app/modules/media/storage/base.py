from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageInterface(ABC):

    @abstractmethod
    def upload(self, file: BinaryIO, object_key: str, mime_type: str):
        pass

    @abstractmethod
    def delete(self, object_key: str):
        pass

    @abstractmethod
    def get_url(self, object_key: str, visibility: str):
        pass
