from fastapi import APIRouter, status
from app.api.deps import UserManagerDep, ResolveLang
from app.schemas.user import UserRegistration, UserLogin, RegistrationResponse
from app.schemas.token import TokenResponse, RefreshRequest



router = APIRouter(prefix="/auth", tags=["user"])



@router.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def registration(data: UserRegistration, language: ResolveLang, manager: UserManagerDep):
    language = data.language or language
    result = await manager.register_user(email=data.email, username=data.username, password=data.password, language=language)
    return result

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, manager: UserManagerDep):
    result = await manager.login(email=data.email, password=data.password)
    return result

@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, manager: UserManagerDep):
    result = await manager.refresh_token(token=data.refresh_token)
    return result