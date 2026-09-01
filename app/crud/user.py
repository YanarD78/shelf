from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select
from app.core.exceptions import UserAlreadyExistsError

from app.models.user import Users, Preferences

class UsersRepo:
    """A class designed to interact with the database for searching and adding users"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user_with_preferences(self, username: str, email: str, password: str, lang: str) -> int:
        try:
            stmt = insert(Users).values(username=username, email=email, password=password).returning(Users.id)
            result = await self.session.execute(stmt)
            user_id = result.scalar_one()

            stmt = insert(Preferences).values(user_id=user_id, include_adult=False, language=lang)
            await self.session.execute(stmt)

            return user_id
        except IntegrityError:
            raise UserAlreadyExistsError()

    async def find_user(self, email: str) -> Users | None:
        stmt = select(Users).where(Users.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_user_by_id(self, user_id: int) -> Users | None:
        stmt = select(Users).where(Users.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_preferences(self, user_id: int) -> Preferences | None:
        stmt = select(Preferences).where(Preferences.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()