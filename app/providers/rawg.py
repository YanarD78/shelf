from httpx import AsyncClient, HTTPStatusError, RequestError
from app.config import settings
from app.core.exceptions import ExternalServerError, ItemNotFound
from app.dto.external import ExternalItem
from datetime import date
import logging

logger = logging.getLogger(__name__)

BASE_RAWG_URL = "https://api.rawg.io/api"

class RAWGClient:
    """A class designed to execute HTTP requests to the RAWG database"""
    def __init__(self, client: AsyncClient):
        self.client = client
        self.key = {"key": settings.rawg_api}



    async def _get(self, path: str, **params) -> dict:
        try:
            response = await self.client.get(
                f"{BASE_RAWG_URL}{path}",
                params={**self.key, **params}
            )
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ItemNotFound() from e
            logger.warning("RAWG returned %s for %s", e.response.status_code, path)
            raise ExternalServerError() from e
        except RequestError as e:
            logger.error("TMDB request failed: %r (path=%s)", e, path)
            raise ExternalServerError() from e

        

    async def search(self, query: str, page: int, **kwargs) -> list[ExternalItem]:
        data = await self._get(path="/games", search=query, page=page, **kwargs)
        results: list = data["results"]
        return [self._to_search_item(obj) for obj in results]

    async def get(self, external_id: str) -> ExternalItem:
        try:
            id_int = int(external_id)
        except ValueError:
            raise ItemNotFound()
        return self._to_item(await self._get(f"/games/{id_int}"))



    def _to_search_item(self, obj: dict) -> ExternalItem:
        return ExternalItem(
            external_id=str(obj["id"]),
            title=obj["name"],
            description=None,
            release_date=date.fromisoformat(obj["released"]) if obj.get("released") else None,
            cover_url=obj.get("background_image") or None,
            vote_average=obj.get("rating") * 2,
            extra=None
        )

    def _to_item(self, obj: dict) -> ExternalItem:
        return ExternalItem(
            external_id=str(obj["id"]),
            title=obj["name"],
            description=obj.get("description_raw"),
            release_date=date.fromisoformat(obj["released"]) if obj.get("released") else None,
            cover_url=obj.get("background_image") or None,
            vote_average=obj["rating"] * 2 if obj.get("rating") is not None else None,
            extra={
                "tba": obj["tba"] if obj.get("released") is None else False,
                "metacritic": obj.get("metacritic") or None,
                "playtime": obj.get("playtime") or None,
                "platforms": self.platforms_to_names(obj["platforms"]) if obj.get("platforms") else [],
                "genres": self.genres_to_names(obj["genres"]) if obj.get("genres") else [],
                "stores": self.stores_to_names(obj["stores"]) if obj.get("stores") else []
            }
        )

    def stores_to_names(self, data: list[dict]) -> list[dict]:
        stores = [s["store"] for s in data]
        result = []
        for s in stores:
            result.append({"name": s["name"], "url": s["domain"]})
        return result

    def genres_to_names(self, genres: list[dict]) -> list[str]:
        return [g["name"] for g in genres] if genres else []

    def platforms_to_names(self, data: list[dict]) -> list[str]:
        platforms = []
        for p in data:
            platforms.append(p["platform"])
        return [p["name"] for p in platforms]