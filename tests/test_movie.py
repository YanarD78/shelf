from tests.handlers.tmdb import mock_tmdb_search_error, mock_tmdb_search_success
from httpx import AsyncClient



# Find movie
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



# Add to watchlist
async def test_add_to_watchlist(client: AsyncClient, auth_headers):
    response = await client.post(
        "/movies/watchlist",
        json={"movie_id": 550},
        headers=auth_headers
    )
    assert response.status_code == 200

async def test_add_to_watchlist_with_integrity_error(client: AsyncClient, auth_headers):
    await client.post(
        "/movies/watchlist",
        json={"movie_id": 550},
        headers=auth_headers
    )
    response = await client.post(
        "/movies/watchlist",
        json={"movie_id": 550},
        headers=auth_headers
    )
    assert response.status_code == 409



# Delete from watchlist
async def test_delete_from_watchlist(client: AsyncClient, auth_headers):
    await client.post(
        "/movies/watchlist",
        json={"movie_id": 550},
        headers=auth_headers
    )

    response = await client.delete(
        "/movies/watchlist/550",
        headers=auth_headers
    )
    assert response.status_code == 204

async def test_delete_from_watchlist_with_no_content_error(client: AsyncClient, auth_headers):
    response = await client.delete(
        "/movies/watchlist/550",
        headers=auth_headers
    )
    assert response.status_code == 404