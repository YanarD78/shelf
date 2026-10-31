from fastapi import APIRouter, status
from app.api.deps import UserServiceDep
from app.schemas.auth import RegistrationRequest, RegistrationResponse, LoginRequest, RefreshRequest, LoginResponse



router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def registration(data: RegistrationRequest, service: UserServiceDep):
    result = await service.register_user(email=data.email, username=data.username, password=data.password)
    return result

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, service: UserServiceDep):
    result = await service.login(email=data.email, password=data.password)
    return result

@router.post("/refresh", response_model=LoginResponse)
async def refresh(data: RefreshRequest, service: UserServiceDep):
    result = await service.refresh_token(token=data.refresh_token)
    return result