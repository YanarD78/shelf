from fastapi import APIRouter, status
from app.api.deps import UserManagerDep
from app.schemas.user import UserRegistration, UserLogin, RegistrationResponse
from app.schemas.token import TokenResponse

router = APIRouter()

@router.post("/registration", tags=["user"], response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def registration(data: UserRegistration, manager: UserManagerDep):
    result = await manager.register_user(data)
    return result

@router.post("/login", tags=["user"], response_model=TokenResponse)
async def login(data: UserLogin, manager: UserManagerDep):
    result = await manager.login(data)
    return result