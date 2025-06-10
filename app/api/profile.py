from fastapi import Depends, APIRouter

from app.models.models import User
from app.utils.get_current_user import get_current_user

router = APIRouter()


@router.get("/", description="Get profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.user_id,
        "username": current_user.username
    }
