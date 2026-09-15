from httpx import AsyncClient, HTTPStatusError, RequestError
from app.config import settings
from app.core.exceptions import ExternalServerError

class TMDBClient:
    """A class designed to execute HTTP requests to the TMDB database"""
    def __init__(self, client: AsyncClient):
        self.client = client



    async def search_movie(self, query: str, include_adult: bool, language: str) -> list[dict]:
        headers = {
            "Authorization": f"Bearer {settings.tmdb_api}",
            "accept": "application/json"
        }
        params = {
            "query": query,
            "include_adult": include_adult,
            "language": language,
            "page": 1
        }

        try:
            response = await self.client.get(url=f"{settings.tmdb_url}/3/search/movie", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except (HTTPStatusError, RequestError):
            raise ExternalServerError()

    async def get_movie(self, external_id: int) -> dict:
        headers = {
            "Authorization": f"Bearer {settings.tmdb_api}",
            "accept": "application/json"
        }
        try:
            response = await self.client.get(url=f"{settings.tmdb_url}/3/movie/{external_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except (HTTPStatusError, RequestError):
            raise ExternalServerError()