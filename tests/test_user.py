from httpx import AsyncClient



# Registration
async def test_register(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "username": "string",
            "email": "user@example.com",
            "password": "stringst"
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

async def test_register_integrity_error(client: AsyncClient, registred_user):
    response = await client.post(
        "/auth/register",
        json={
            "username": registred_user["username"],
            "email": registred_user["email"],
            "password": registred_user["password"]
        }
    )
    assert response.status_code == 409



# Login
async def test_login(client: AsyncClient, registred_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": registred_user["email"],
            "password": registred_user["password"]
        }
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"

async def test_login_wrong_password(client: AsyncClient, registred_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": registred_user["email"],
            "password": "wrong_password"
        }
    )
    assert response.status_code == 401