from httpx import AsyncClient, HTTPStatusError, RequestError
from app.config import settings
from app.core.exceptions import ExternalServerError, ItemNotFound
from app.dto.external import ExternalItem
from datetime import date

class TMDBClient:
    """A class designed to execute HTTP requests to the TMDB database"""
    def __init__(self, client: AsyncClient):
        self.client = client
        self.base_url = settings.tmdb_url
        self.img_base = "https://image.tmdb.org/t/p"
        self.headers = {
            "Authorization": f"Bearer {settings.tmdb_token}",
            "accept": "application/json"
        }



    async def _get(self, path: str, **params) -> dict:
        try:
            response = await self.client.get(
                f"{self.base_url}{path}",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ItemNotFound() from e
            raise ExternalServerError() from e
        except RequestError as e:
            raise ExternalServerError() from e

        

    async def search(self, query: str, include_adult: bool, page: int, year: int | None) -> list[ExternalItem]:
        data = await self._get(path="/3/search/movie", query=query, include_adult=include_adult, page=page, year=year)
        results = data["results"]
        return [self._to_item(m) for m in results]

    async def get(self, external_id: str) -> ExternalItem:
        try:
            id_int = int(external_id)
        except ValueError:
            raise ItemNotFound()
        return self._to_item(await self._get(f"/3/movie/{id_int}"))



    def _to_item(self, m: dict) -> ExternalItem:
        return ExternalItem(
            external_id=str(m["id"]),
            title=m["title"],
            description=m.get("overview") or None,
            release_date=date.fromisoformat(m["release_date"]) if m.get("release_date") else None,
            cover_url=self._to_img(m.get("poster_path")),
            vote_average=m.get("vote_average"),
            extra={
                "runtime_minutes": m.get("runtime") or None,
                "backdrop_url": self._to_img(m.get("backdrop_path"), "w1280"),
                "genres": self.genres_to_list(m.get("genres"))
            }
        )

    def genres_to_list(self, genres: list[dict]) -> list:
        return [g["name"] for g in genres] if genres else []

    def _to_img(self, path: str | None, size: str = "w500") -> str | None:
        return f"{self.img_base}/{size}{path}" if path else None