from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert
from app.core.exceptions import UserAlreadyExistsError

from app.models.users import Users

class UsersRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, username: str, email: str, password: str) -> int:
        try:
            stmt = insert(Users).values(username=username, email=email, password=password).returning(Users.id)
            result = await self.session.execute(stmt)
            return result.scalar()
        except IntegrityError:
            raise UserAlreadyExistsError()