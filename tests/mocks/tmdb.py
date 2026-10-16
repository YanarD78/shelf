import respx
from app.config import settings
import httpx

def mock_get_search(router: respx.MockRouter, query: str = "Fight Club"):
    return router.get(f"{settings.tmdb_url}/3/search/movie", params={"query": query}).mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "results": [
                    {
                        "id": 550,
                        "title": "Fight Club",
                        "overview": ".....",
                        "poster_path": "/pp124214",
                        "release_date": "1999-10-15",
                        "vote_average": 8.4
                    }
                ]
            }
        )
    )

def mock_get_movie(router: respx.MockRouter, query: int = 550):
    return router.get(f"{settings.tmdb_url}/3/movie/{query}").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "id": 550,
                "title": "Fight Club",
                "overview": ".....",
                "release_date": "1999-10-15",
                "poster_path": "/pp123124124",
                "vote_average": 8.4,
                "runtime": 120,
                "backdrop_url": "/bp1213241",
                "genres": [
                    {"id": 1, "name": "thriller"},
                    {"id": 2, "name": "drama"}
                ]
            }
        )
    )