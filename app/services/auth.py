from app.crud.user import UsersRepo
from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_tokens, hash_password, check_password, decode_refresh_token

class UsersManager:
    """A class designed for user registration and authorization"""
    def __init__(self, repo: UsersRepo):
        self.repo = repo

    async def register_user(self, email: str, username: str, password: str, language: str) -> dict:
        hashed_password = hash_password(password)
        user_id = await self.repo.add_user_with_preferences(
            username=username,
            email=email,
            password=hashed_password,
            lang=language
        )

        return {"id": user_id, "message": "User created successfully"}

    async def login(self, email: str, password: str) -> dict:
        user = await self.repo.find_user(email=email)
        if user is None:
            raise InvalidCredentialsError()
        
        is_password_correct = check_password(
            password,
            user.password
        )
        if not is_password_correct:
            raise InvalidCredentialsError()
        
        tokens = create_tokens(user.id)
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "Bearer"
        }

    async def refresh_token(self, token: str) -> dict:
        user_id = decode_refresh_token(refresh_token=token)
        user = await self.repo.find_user_by_id(user_id=user_id)
        if user is None:
            raise InvalidCredentialsError("User no longer exists")
        
        token = create_tokens(user_id)
        return {
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "token_type": "Bearer"
        }