from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, delete, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.core.exceptions import RecordAlreadyExists
from app.dto.dto import WatchlistFilter, WatchedFilter
from app.models.movie import UserWatchlist, UserWatched, Movie
from datetime import date
from typing import Sequence

class MoviesRepo:
    """A class designed to interact with the database for searching and adding films"""
    def __init__(self, session: AsyncSession):
        self.session = session



    async def get_movie(self, external_id: int) -> int | None:
        stmt = select(Movie.id).where(Movie.external_id==external_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def add_movie(self, external_id: int, title: str, poster_path: str, release_date: date) -> int:
        stmt = pg_insert(Movie).values(
            external_id=external_id,
            title=title,
            poster_path=poster_path,
            release_date=release_date
        ).on_conflict_do_nothing(index_elements=["external_id"]).returning(Movie.id)
        result = await self.session.execute(stmt)
        local_id = result.scalar()
        if local_id is None:
            local_id = await self.get_movie(external_id=external_id)
        return local_id



    async def get_watchlist(self, user_id: int, filters: WatchlistFilter) -> Sequence:
        stmt = select(UserWatchlist).where(UserWatchlist.user_id == user_id)

        if filters.added_before is not None:
            stmt = stmt.where(UserWatchlist.added_at < filters.added_before)
        if filters.added_after is not None:
            stmt = stmt.where(UserWatchlist.added_at > filters.added_after)
        if filters.added_at is not None:
            stmt = stmt.where(UserWatchlist.added_at == filters.added_at)

        needs_movie_join = any((
            filters.released_before,
            filters.released_after,
            filters.released_at,
        ))
        if needs_movie_join:
            stmt = stmt.join(Movie, UserWatchlist.local_id == Movie.id)
            if filters.released_before is not None:
                stmt = stmt.where(Movie.release_date < filters.released_before)
            if filters.released_after is not None:
                stmt = stmt.where(Movie.release_date > filters.released_after)
            if filters.released_at is not None:
                stmt = stmt.where(Movie.release_date == filters.released_at)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_to_watchlist(self, user_id: int, local_id: int) -> int:
        try:
            
            stmt = insert(UserWatchlist).values(
                user_id=user_id,
                local_id=local_id
            ).returning(UserWatchlist.id)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        
        except IntegrityError:
            raise RecordAlreadyExists()

    async def delete_from_watchlist(self, user_id: int, local_id: int) -> int:
        stmt = delete(UserWatchlist).where(
            UserWatchlist.user_id==user_id,
            UserWatchlist.local_id==local_id
        ).returning(UserWatchlist.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()



    async def get_watched(self, user_id: int, filters: WatchedFilter) -> Sequence:
        stmt = select(UserWatched).where(UserWatched.user_id == user_id)

        if filters.added_before is not None:
            stmt = stmt.where(UserWatched.added_at < filters.added_before)
        if filters.added_after is not None:
            stmt = stmt.where(UserWatched.added_at > filters.added_after)
        if filters.added_at is not None:
            stmt = stmt.where(UserWatched.added_at == filters.added_at)

        if filters.local_id is not None:
            stmt = stmt.where(UserWatched.local_id == filters.local_id)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_to_watched(self, user_id: int, local_id: int, first_watch: bool, watched_at: date, rating: float | None, comment: str | None) -> int:
        if first_watch:
            update_stmt = update(UserWatched).where(
                UserWatched.user_id==user_id,
                UserWatched.local_id==local_id,
                UserWatched.first_watch==True
            ).values(
                first_watch=False
            )
            await self.session.execute(update_stmt)

        stmt = insert(UserWatched).values(
            user_id=user_id,
            local_id=local_id,
            first_watch=first_watch,
            watched_at=watched_at,
            rating=rating,
            comment=comment
        ).returning(UserWatched.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_from_watched(self, user_id: int, row_id: int) -> int:
        stmt = delete(UserWatched).where(
            UserWatched.user_id==user_id,
            UserWatched.id==row_id
        ).returning(UserWatched.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()