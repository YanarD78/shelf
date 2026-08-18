from app.crud.users import UsersRepo
from app.clients.tmdb import TMDBClient

class MoviesManager:
    "A class designed for searching for movies and saving them"
    def __init__(self, client: TMDBClient, repo: UsersRepo, current_user: int):
        self.client = client
        self.repo = repo
        self.user = current_user

    async def search_movie(self, query: str) -> dict:
        preferences = await self.repo.get_user_preferences(self.user)
        data = await self.client.search_movie(query, preferences.include_adult, preferences.language)
        return data['results']

    async def add_to_watched(self):
        pass

    async def add_to_watchlist(self):
        pass