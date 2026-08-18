from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, Sequence
from app.core.exceptions import UserAlreadyExistsError

from app.models.users import Users, Preferences

class UsersRepo:
    "A class designed to interact with the database for searching and adding users"
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, username: str, email: str, password: str) -> int:
        try:
            stmt = insert(Users).values(username=username, email=email, password=password).returning(Users.id)
            result = await self.session.execute(stmt)
            return result.scalar()
        except IntegrityError:
            raise UserAlreadyExistsError()

    async def find_user(self, email: str) -> Users | None:
        stmt = select(Users).where(Users.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_preferences(self, user_id: int) -> Preferences | None:
        stmt = select(Preferences).where(Preferences.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()