from fastapi import APIRouter, Depends, UploadFile, File

from app.modules.user.model import User
from app.modules.auth.v1.dependency import get_current_user
from app.modules.media.v1.dependency import get_media_service
from app.modules.media.v1.service import MediaService

router = APIRouter(prefix="/media", tags=["Media"])


@router.post("/upload")
async def upload(
    files: list[UploadFile] = File(...),
    service: MediaService = Depends(get_media_service),
    current_user: User = Depends(get_current_user),
):
    return service.upload_multiple(files=files, user=current_user)
