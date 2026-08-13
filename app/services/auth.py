from app.crud.users import UsersRepo
from app.schemas.user import UserRegistration

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