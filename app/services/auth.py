from app.crud.user import UsersRepo
from app.schemas.user import UserRegistration, UserLogin
from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_tokens, hash_password, check_password

class UsersManager:
    "A class designed for user registration and authorization"
    def __init__(self, repo: UsersRepo):
        self.repo = repo

    async def register_user(self, user_data: UserRegistration):
        hashed_password = hash_password(user_data.password)
        user_id = await self.repo.add_user(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )
        return {"id": user_id, "message": "User created successfully"}

    async def login(self, user_data: UserLogin):
        user = await self.repo.find_user(user_data.email)
        if user is None:
            raise InvalidCredentialsError()
        
        is_password_correct = check_password(
            user_data.password,
            user.password
        )
        if not is_password_correct:
            raise InvalidCredentialsError()
        
        tokens = create_tokens(user.id)
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer"
        }