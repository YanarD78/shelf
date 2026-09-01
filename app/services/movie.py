from app.crud.movies import MoviesRepo
from app.crud.user import UsersRepo
from app.clients.tmdb import TMDBClient
from app.core.exceptions import ItemNotFound, ExternalServerError

class MoviesManager:
    """A class designed for searching for movies and saving them"""
    def __init__(self, client: TMDBClient, users_repo: UsersRepo, movies_repo: MoviesRepo, current_user: int):
        self.client = client
        self.users_repo = users_repo
        self.movies_repo = movies_repo
        self.user = current_user

    async def search_movie(self, query: str) -> dict:
        try:
            preferences = await self.users_repo.get_user_preferences(user_id=self.user)
            data = await self.client.search_movie(query=query, include_adult=preferences.include_adult, language=preferences.language)
            if data is None:
                raise ItemNotFound("The movie not found")
            return data['results']
        except KeyError:
            raise ExternalServerError()

    async def add_to_watched(self):
        pass

    async def delete_from_watched(self):
        pass

    async def add_to_watchlist(self, movie_id: int) -> dict:
        result = await self.movies_repo.add_to_watchlist(user_id=self.user, movie_id=movie_id)
        return {"id": result}

    async def delete_from_watchlist(self, movie_id: int) -> None:
        result = await self.movies_repo.delete_from_watchlist(user_id=self.user, movie_id=movie_id)
        if not result:
            raise ItemNotFound("The movie not found")