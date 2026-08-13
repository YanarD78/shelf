from fastapi import APIRouter, Depends

from app.api.deps import get_user_manager

from app.schemas.user import UserRegistration, RegistrationResponse
from app.services.auth import UsersManager

router = APIRouter()

@router.post("/registration", tags=["user"], response_model=RegistrationResponse)
async def registration(data: UserRegistration, manager: UsersManager = Depends(get_user_manager)):
    result = await manager.register_user(data)
    return result