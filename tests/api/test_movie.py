from tests.mocks.tmdb import mock_get_movie, mock_get_search
from httpx import AsyncClient

# Test search movies
async def test_search_movies(client: AsyncClient, auth_headers, respx_mock):
    mock_get_search(respx_mock)
    response = await client.get(
        "/movies/search",
        params={"query": "Fight Club"},
        headers=auth_headers
    )
    assert response.status_code == 200

async def test_search_movies_without_token(client: AsyncClient, respx_mock):
    mock_get_search(respx_mock)
    response = await client.get(
        "/movies/search",
        params={"query": "Fight Club"},
        headers={"Authorization": "Bearer wrong token"}
    )
    assert response.status_code == 401
    assert "authenticated" in response.json()["detail"]



# Test get movie
async def test_get_movie_item(client: AsyncClient, auth_headers, respx_mock):
    mock_get_movie(respx_mock)
    response = await client.get(
        "/movies/item/550",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json() is not []

async def test_get_movie_item_without_token(client: AsyncClient, respx_mock):
    mock_get_movie(respx_mock)
    response = await client.get(
        "/movies/item/550"
    )
    assert response.status_code == 401



# Test add to watchlist
async def test_add_to_watchlist(client: AsyncClient, auth_headers, get_watchlist_json, respx_mock):
    mock_get_movie(respx_mock)
    response = await client.post(
        "/movies/watchlist",
        headers=auth_headers,
        json=get_watchlist_json
    )
    assert response.status_code == 201

async def test_add_to_watchlist_without_token(client: AsyncClient, get_watchlist_json, respx_mock):
    mock_get_movie(respx_mock)
    response = await client.post(
        "/movies/watchlist",
        json=get_watchlist_json
    )
    assert response.status_code == 401



# Test get watchlist
async def test_get_watchlist(client: AsyncClient, auth_headers):
    response = await client.get(
        "/movies/watchlist",
        headers=auth_headers
    )
    assert response.status_code == 200



# Test add to watched
async def test_add_to_watched(client: AsyncClient, auth_headers, get_watched_json, respx_mock):
    mock_get_movie(respx_mock)
    response = await client.post(
        "/movies/watchlist",
        headers=auth_headers,
        json=get_watched_json
    )
    assert response.status_code == 201

async def test_add_to_watched_without_token(client: AsyncClient, get_watched_json, respx_mock):
    mock_get_movie(respx_mock)
    response = await client.post(
        "/movies/watchlist",
        json=get_watched_json
    )
    assert response.status_code == 401