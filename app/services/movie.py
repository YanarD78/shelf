from app.crud.movies import MoviesRepo
from app.crud.user import UsersRepo
from app.clients.tmdb import TMDBClient
from app.core.exceptions import ItemNotFound, ExternalServerError

from datetime import date

class MoviesManager:
    """A class designed for searching for movies and saving them"""
    def __init__(self, client: TMDBClient, users_repo: UsersRepo, movies_repo: MoviesRepo, current_user: int):
        self.client = client
        self.users_repo = users_repo
        self.movies_repo = movies_repo
        self.user = current_user

    async def _resolve_local_movie_id(self, tmdb_id: int) -> int:
        local_movie_id = await self.movies_repo.get_movie(tmdb_id=tmdb_id)
        if local_movie_id is not None:
            return local_movie_id
        
        movie = await self.client.get_movie(tmdb_id=tmdb_id)
        return await self.movies_repo.add_movie(
            tmdb_id=movie["id"],
            title=movie["title"],
            poster_path=movie["poster_path"],
            release_date=movie["release_date"]
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



    async def add_to_watchlist(self, tmdb_id: int) -> dict[str, int]:
        local_movie_id = await self._resolve_local_movie_id(tmdb_id=tmdb_id)

        result = await self.movies_repo.add_to_watchlist(
            user_id=self.user,
            local_movie_id=local_movie_id
        )
        return {"id": result, "movie_id": local_movie_id}

    async def delete_from_watchlist(self, local_movie_id: int) -> None:
        result = await self.movies_repo.delete_from_watchlist(user_id=self.user, local_movie_id=local_movie_id)
        if not result:
            raise ItemNotFound("The movie not found")



    async def add_to_watched(self, tmdb_id: int, first_watch: bool, watched_at: date, rating: float | None, comment: str | None) -> dict[str, int]:
        local_movie_id = await self._resolve_local_movie_id(tmdb_id=tmdb_id)

        result = await self.movies_repo.add_to_watched(
            user_id=self.user,
            local_movie_id=local_movie_id,
            first_watch=first_watch,
            watched_at=watched_at,
            rating=rating,
            comment=comment,
        )
        return {"id": result, "movie_id": local_movie_id}

    async def delete_from_watched(self, record_id: int) -> None:
        result = await self.movies_repo.delete_from_watched(
            user_id=self.user,
            record_id=record_id
        )
        if not result:
            raise ItemNotFound("The movie not found")