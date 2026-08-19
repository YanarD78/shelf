from httpx2 import AsyncClient, HTTPStatusError, RequestError
from app.config import settings
from app.core.exceptions import ExternalServerError

class TMDBClient:
    "A class designed to execute HTTP requests to the TMDB database"
    def __init__(self, client: AsyncClient):
        self.client = client

    async def search_movie(self, query: str, include_adult: bool, language: str) -> dict:
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
        except HTTPStatusError:
            raise ExternalServerError()
        except RequestError:
            raise ExternalServerError()