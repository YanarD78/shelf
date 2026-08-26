from httpx import AsyncClient

async def test_register(client: AsyncClient):
    response = await client.post(
        "/registration",
        json={
            "username": "string",
            "email": "user@example.com",
            "password": "stringst"
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

async def test_login(client: AsyncClient, registred_user):
    response = await client.post(
        "/login",
        json={
            "email": registred_user["email"],
            "password": registred_user["password"]
        }
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"



async def test_register_integrity_error(client: AsyncClient, registred_user):
    response = await client.post(
        "/registration",
        json={
            "username": registred_user["username"],
            "email": registred_user["email"],
            "password": registred_user["password"]
        }
    )
    assert response.status_code == 409

async def test_login_wrong_password(client: AsyncClient, registred_user):
    response = await client.post(
        "/login",
        json={
            "email": registred_user["email"],
            "password": "wrong_password"
        }
    )
    assert response.status_code == 401