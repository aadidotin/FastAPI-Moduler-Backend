from fastapi import APIRouter, Depends, UploadFile, File

from app.modules.auth.v1.dependency import get_current_user
from app.modules.user.v1.schema import UserResponse, UpdateUserRequest
from app.modules.user.model import User

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", response_model=UserResponse)
async def my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/update_profile")
async def update_profile(
    payload: UpdateUserRequest,
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    pass
