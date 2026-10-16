import pytest_asyncio
from app.main import app
from app.api.deps import get_http_client, get_session
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from app.config import settings
from app.database import Base
from collections.abc import AsyncIterator



@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(settings.test_db)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    connection = await engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint"
    )

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()

@pytest_asyncio.fixture
async def http_client(respx_mock) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(timeout=10) as http:
        yield http

@pytest_asyncio.fixture
async def client(http_client, db_session):
    app.dependency_overrides[get_http_client] = lambda: http_client
    app.dependency_overrides[get_session] = lambda: db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()



@pytest_asyncio.fixture
def payload() -> dict:
    return {
        "username": "string",
        "email": "test@example.com",
        "password": "stringst"
    }

@pytest_asyncio.fixture
async def registered_user(client: AsyncClient, payload: dict):
    response = await client.post(
        "/auth/register",
        json=payload
    )
    assert response.status_code == 201

@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, payload: dict, registered_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"]
        }
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()["access_token"]}"}



@pytest_asyncio.fixture
def get_watchlist_json():
    return {
        "external_id": "550",
        "note": "string"
    }

@pytest_asyncio.fixture
def get_watched_json():
    return {
        "external_id": "550",
        "is_first": True,
        "completed_on": "2026-10-11",
        "rating": 10,
        "comment": "string",
    }