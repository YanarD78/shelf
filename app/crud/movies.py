from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, delete
from app.core.exceptions import RecordAlreadyExists

from app.models.movies import UsersWatchlists

class MoviesRepo:
    """A class designed to interact with the database for searching and adding films"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_watchlist(self, user_id: int, movie_id: int) -> int:
        try:
            
            stmt = insert(UsersWatchlists).values(user_id=user_id, movie_id=movie_id).returning(UsersWatchlists.id)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        
        except IntegrityError:
            raise RecordAlreadyExists()

    async def delete_from_watchlist(self, user_id: int, movie_id: int) -> int:
        stmt = delete(UsersWatchlists).where(UsersWatchlists.user_id==user_id, UsersWatchlists.movie_id==movie_id).returning(UsersWatchlists.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()