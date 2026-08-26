import respx
import httpx
from app.config import settings

def mock_tmdb_search_success():
    respx.get(f"{settings.tmdb_url}/3/search/movie").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "results": [
                    {
                        "id": 550,
                        "title": "Fight Club",
                        "overview": "A ticking-ti3me-bomb insomniac...",
                        "release_date": "1999-10-15",
                        "vote_average": 8.4
                    }
                ]
            }
        )
    )

def mock_tmdb_search_error():
    respx.get(f"{settings.tmdb_url}/3/search/movie").mock(
        return_value=httpx.Response(
            status_code=500,
            json={"status_message": "Internal server error"})
    )