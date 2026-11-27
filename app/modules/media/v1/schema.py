from sqlmodel import SQLModel

from app.modules.media.model import MediaVisibility


class MediaResponse(SQLModel):
    id: int
    file_url: str
    file_path: str
    mime_type: str
    original_name: str
    visibility: MediaVisibility
