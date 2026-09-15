from app.repositories.movie import MoviesRepo
from app.repositories.user import UsersRepo
from app.dto.dto import WatchlistFilter, WatchedFilter
from app.clients.tmdb import TMDBClient
from app.core.exceptions import ItemNotFound, ExternalServerError
from typing import Sequence

from datetime import date

class MoviesManager:
    """A class designed for searching for movies and saving them"""
    def __init__(self, client: TMDBClient, users_repo: UsersRepo, movies_repo: MoviesRepo, current_user: int):
        self.client = client
        self.users_repo = users_repo
        self.movies_repo = movies_repo
        self.user = current_user

    async def _resolve_local_id(self, external_id: int) -> int:
        local_id = await self.movies_repo.get_movie(external_id=external_id)
        if local_id is not None:
            return local_id
        
        movie = await self.client.get_movie(external_id=external_id)
        return await self.movies_repo.add_movie(
            external_id=movie["id"],
            title=movie["title"],
            poster_path=movie["poster_path"],
            release_date=date.fromisoformat(movie["release_date"]) if movie["release_date"] else None
        )



    async def search_movie(self, query: str) -> list[dict]:
        try:
            preferences = await self.users_repo.get_user_preferences(user_id=self.user)
            data = await self.client.search_movie(
                query=query,
                include_adult=preferences.include_adult,
                language=preferences.language
            )
            return data["results"]
        except KeyError:
            raise ExternalServerError()



    async def get_watchlist(self, filters: WatchlistFilter) -> Sequence:
        result = await self.movies_repo.get_watchlist(user_id=self.user, filters=filters)
        return result

    async def add_to_watchlist(self, external_id: int) -> dict[str, int]:
        local_id = await self._resolve_local_id(external_id=external_id)

        result = await self.movies_repo.add_to_watchlist(
            user_id=self.user,
            local_id=local_id
        )
        return {"id": result, "local_id": local_id}

    async def delete_from_watchlist(self, local_id: int) -> None:
        result = await self.movies_repo.delete_from_watchlist(user_id=self.user, local_id=local_id)
        if not result:
            raise ItemNotFound("The movie not found")


    async def get_watched(self, filters: WatchedFilter) -> Sequence:
        result = await self.movies_repo.get_watched(user_id=self.user, filters=filters)
        return result

    async def add_to_watched(self, external_id: int, first_watch: bool, watched_at: date, rating: float | None, comment: str | None) -> dict[str, int]:
        local_id = await self._resolve_local_id(external_id=external_id)

        result = await self.movies_repo.add_to_watched(
            user_id=self.user,
            local_id=local_id,
            first_watch=first_watch,
            watched_at=watched_at,
            rating=rating,
            comment=comment,
        )
        return {"id": result, "local_id": local_id}

    async def delete_from_watched(self, row_id: int) -> None:
        result = await self.movies_repo.delete_from_watched(
            user_id=self.user,
            row_id=row_id
        )
        if not result:
            raise ItemNotFound("The movie not found")