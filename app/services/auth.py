from app.crud.users import UsersRepo
from app.schemas.user import UserRegistration, UserLogin
from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_tokens

import bcrypt

class UsersManager:
    def __init__(self, repo: UsersRepo):
        self.repo = repo

    async def register_user(self, user_data: UserRegistration):
        bytes_password = user_data.password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(bytes_password, salt).decode()
        user_id = await self.repo.add_user(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )
        return {"id": user_id, "message": "User create successfully"}

    async def login(self, user_data: UserLogin):
        user = await self.repo.find_user(user_data.email)
        if user is None:
            raise InvalidCredentialsError()
        
        is_password_correct = bcrypt.checkpw(
            user_data.password.encode("utf-8"),
            user.password.encode("utf-8")
        )
        if not is_password_correct:
            raise InvalidCredentialsError()

        tokens = create_tokens(user.id)
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer"
        }