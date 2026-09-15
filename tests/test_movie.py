from tests.handlers.tmdb import mock_tmdb_search_error, mock_tmdb_search_success, mock_get_movie
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



# Get wathlist
async def test_get_watchlist(client: AsyncClient, auth_headers, add_watchlist):
    response = await client.get(
        "/movies/watchlist",
        params={"released_before": "2000-01-01"},
        headers=auth_headers
    )
    assert response.status_code == 200

async def test_get_watchlist_with_wrong_token(client: AsyncClient, add_watchlist):
    response = await client.get(
        "/movies/watchlist",
        params={"released_before": "2000-01-01"},
        headers={"Authorization": "Bearer wrong_token"}
    )
    assert response.status_code == 401



# Add to watchlist
async def test_add_to_watchlist(client: AsyncClient, auth_headers):
    mock_get_movie()
    response = await client.post(
        "/movies/watchlist",
        json={"external_id": 550},
        headers=auth_headers
    )
    assert response.status_code == 200

async def test_add_to_watchlist_with_wrong_token(client: AsyncClient):
    mock_get_movie()
    response = await client.post(
        "/movies/watchlist",
        json={"external_id": 550},
        headers={
            "Authorization": "Bearer wrong_token"
        }
    )
    assert response.status_code == 401

async def test_add_to_watchlist_with_integrity_error(client: AsyncClient, auth_headers):
    mock_get_movie()
    await client.post(
        "/movies/watchlist",
        json={"external_id": 550},
        headers=auth_headers
    )
    response = await client.post(
        "/movies/watchlist",
        json={"external_id": 550},
        headers=auth_headers
    )
    assert response.status_code == 409



# Delete from watchlist
async def test_delete_from_watchlist(client: AsyncClient, auth_headers):
    mock_get_movie()
    post_response = await client.post(
        "/movies/watchlist",
        json={"external_id": 550},
        headers=auth_headers
    )
    response = await client.delete(
        f"/movies/watchlist/{post_response.json()["local_id"]}",
        headers=auth_headers
    )
    assert response.status_code == 204

async def test_delete_from_watchlist_with_no_content_error(client: AsyncClient, auth_headers):
    response = await client.delete(
        "/movies/watchlist/550",
        headers=auth_headers
    )
    assert response.status_code == 404



# Get watched
async def test_get_watched(client: AsyncClient, auth_headers, add_watched):
    response = await client.get(
        "/movies/watched",
        headers=auth_headers
    )
    assert response.status_code == 200



# Add to watched
async def test_add_to_watched(client: AsyncClient, auth_headers):
    mock_get_movie()
    response = await client.post(
        "/movies/watched",
        json={
            "external_id": 550,
            "first_watch": True,
            "watched_at": "1999-05-12",
            "rating": 9.5,
            "comment": "Test comment"
        },
        headers=auth_headers
    )
    assert response.status_code == 200

async def test_add_to_watched_with_wrong_token(client: AsyncClient):
    mock_get_movie()
    response = await client.post(
        "/movies/watched",
        json={
            "external_id": 550,
            "first_watch": True,
            "watched_at": "1999-05-12",
            "rating": 9.5,
            "comment": "Test comment"
        },
        headers={
            "Authorization": "Bearer wrong_token"
        }
    )
    assert response.status_code == 401



# Delete from watched
async def test_delete_from_watched(client: AsyncClient, auth_headers):
    mock_get_movie()
    post_reponse = await client.post(
        "/movies/watched",
        json={
            "external_id": 550,
            "first_watch": True,
            "watched_at": "1999-05-12",
            "rating": 9.5,
            "comment": "Test comment"
        },
        headers=auth_headers
    )
    response = await client.delete(
        f"/movies/watched/{post_reponse.json()["id"]}",
        headers=auth_headers
    )
    assert response.status_code == 204

async def test_delete_from_else_watched(client: AsyncClient, auth_headers):
    mock_get_movie()
    post_reponse = await client.post(
        "/movies/watched",
        json={
            "external_id": 550,
            "first_watch": True,
            "watched_at": "1999-05-12",
            "rating": 9.5,
            "comment": "Test comment"
        },
        headers=auth_headers
    )
    response = await client.delete(
        f"/movies/watched/{post_reponse.json()["id"]}",
        headers=auth_headers
    )
    assert response.status_code == 204