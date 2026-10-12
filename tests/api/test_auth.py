from httpx import AsyncClient

# Register
async def test_register(client: AsyncClient, payload: dict):
    response = await client.post(
        "/auth/register",
        json=payload
    )
    assert response.status_code == 201

async def test_register_with_long_password(client: AsyncClient, payload: dict):
    response = await client.post(
        "/auth/register",
        json={
            "username": payload["username"],
            "email": payload["email"],
            "password": "йцукенгшщзхъфывапролджэячсмитьбю.йцукенгшщзхъ"
        }
    )
    assert response.status_code == 422

async def test_register_with_integrity_error(client: AsyncClient, registered_user, payload: dict):
    response = await client.post(
        "/auth/register",
        json=payload
    )
    assert response.status_code == 409



# Login
async def test_login(client: AsyncClient, payload: dict, registered_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"]
        }
    )
    assert response.status_code == 200
    assert response.json() is not None

async def test_login_with_wrong_password(client: AsyncClient, payload: dict, registered_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": payload["email"],
            "password": "wrong password"
        }
    )
    assert response.status_code == 401
    assert "Incorrect" in response.json()["detail"]