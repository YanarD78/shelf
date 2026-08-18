from fastapi import APIRouter, Depends, status
from app.api.deps import get_user_manager
from app.schemas.user import UserRegistration, UserLogin, RegistrationResponse
from app.schemas.token import TokenResponse
from app.services.auth import UsersManager

router = APIRouter()

@router.post("/registration", tags=["user"], response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def registration(data: UserRegistration, manager: UsersManager = Depends(get_user_manager)):
    result = await manager.register_user(data)
    return result

@router.post("/login", tags=["user"], response_model=TokenResponse)
async def login(data: UserLogin, manager: UsersManager = Depends(get_user_manager)):
    result = await manager.login(data)
    return result