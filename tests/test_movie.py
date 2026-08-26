from tests.handlers.tmdb import mock_tmdb_search_error, mock_tmdb_search_success
from httpx import AsyncClient

async def test_get_movie(client: AsyncClient, auth_headers):
    mock_tmdb_search_success()

    response = await client.get(
        "/movies/search",
        params={"query": "Fight Club"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Fight Club"

async def test_get_movie_tmdb_unavailable(client: AsyncClient, auth_headers):
    mock_tmdb_search_error()

    response = await client.get(
        "/movies/search",
        params={"query": "Fight Club"},
        headers=auth_headers
    )
    assert response.status_code == 502

async def test_get_movie_without_token(client: AsyncClient):
    response = await client.get(
        "/movies/search",
        params={"query": "Fight Club"}
    )
    assert response.status_code == 401

async def test_get_movie_with_wrong_token(client: AsyncClient):
    response = await client.get(
        "/movies/search",
        params={
            "query": "Fight Club"
        },
        headers={
            "Authorization": "Bearer wrong_token"
        }
    )
    assert response.status_code == 401