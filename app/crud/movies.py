from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, delete, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.core.exceptions import RecordAlreadyExists
from datetime import date

from app.models.movies import UsersWatchlists, UsersWatched, Movie

class MoviesRepo:
    """A class designed to interact with the database for searching and adding films"""
    def __init__(self, session: AsyncSession):
        self.session = session



    async def get_movie(self, tmdb_id: int) -> int | None:
        stmt = select(Movie.id).where(Movie.tmdb_id==tmdb_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def add_movie(self, tmdb_id: int, title: str, poster_path: str, release_date: str) -> int:
        stmt = pg_insert(Movie).values(
            tmdb_id=tmdb_id,
            title=title,
            poster_path=poster_path,
            release_date=release_date
        ).on_conflict_do_nothing(index_elements=["tmdb_id"]).returning(Movie.id)
        result = await self.session.execute(stmt)
        local_movie_id = result.scalar()
        if local_movie_id is None:
            local_movie_id = await self.get_movie(tmdb_id=tmdb_id)
        return local_movie_id



    async def add_to_watchlist(self, user_id: int, local_movie_id: int) -> int:
        try:
            
            stmt = insert(UsersWatchlists).values(
                user_id=user_id,
                movie_id=local_movie_id
            ).returning(UsersWatchlists.id)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        
        except IntegrityError:
            raise RecordAlreadyExists()

    async def delete_from_watchlist(self, user_id: int, local_movie_id: int) -> int:
        stmt = delete(UsersWatchlists).where(
            UsersWatchlists.user_id==user_id,
            UsersWatchlists.movie_id==local_movie_id
        ).returning(UsersWatchlists.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()



    async def add_to_watched(self, user_id: int, local_movie_id: int, first_watch: bool, watched_at: date, rating: float | None, comment: str | None) -> int:
        if first_watch:
            update_stmt = update(UsersWatched).where(
                UsersWatched.user_id==user_id,
                UsersWatched.movie_id==local_movie_id,
                UsersWatched.first_watch==True
            ).values(
                first_watch=False
            )
            await self.session.execute(update_stmt)

        stmt = insert(UsersWatched).values(
            user_id=user_id,
            movie_id=local_movie_id,
            first_watch=first_watch,
            watched_at=watched_at,
            rating=rating,
            comment=comment
        ).returning(UsersWatched.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_from_watched(self, user_id: int, record_id: int) -> int:
        stmt = delete(UsersWatched).where(
            UsersWatched.user_id==user_id,
            UsersWatched.id==record_id
        ).returning(UsersWatched.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()