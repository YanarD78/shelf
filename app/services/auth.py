from fastapi.concurrency import run_in_threadpool
from app.repositories.user import UserRepo
from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_tokens, hash_password, check_password, decode_refresh_token

class UserService:
    """A class designed for user registration and authorization"""
    def __init__(self, repo: UserRepo):
        self.repo = repo

        

    async def register_user(self, email: str, username: str, password: str) -> dict:
        hashed_password = await run_in_threadpool(hash_password, password)
        user_id = await self.repo.add_user_with_preferences(
            username=username,
            email=email.strip().lower(),
            password=hashed_password
        )

        return {"id": user_id, "message": "User created successfully"}

    async def login(self, email: str, password: str) -> dict:
        user = await self.repo.find_user(email=email.strip().lower())
        to_check = user.password if user else hash_password("password1234")
        
        is_password_correct = await run_in_threadpool(check_password, password, to_check)
        if user is None or not is_password_correct:
            raise InvalidCredentialsError()
        
        tokens = create_tokens(user.id)
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "Bearer"
        }

    async def refresh_token(self, token: str) -> dict:
        user_id = decode_refresh_token(token=token)
        user = await self.repo.find_user_by_id(user_id=user_id)
        if user is None:
            raise InvalidCredentialsError("User no longer exists")
        
        new_tokens = create_tokens(user_id)
        return {
            "access_token": new_tokens["access_token"],
            "refresh_token": new_tokens["refresh_token"],
            "token_type": "Bearer"
        }