from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.media.v1.service import MediaService
from app.modules.media.repository import MediaRepository


def get_media_service(db: Session = Depends(get_session)) -> MediaService:
    return MediaRepository(db=db)
