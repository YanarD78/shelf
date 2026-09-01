from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from typing import AsyncIterator
import respx

from app.database import Base
from app.config import settings
from app.api.deps import get_session
from app.main import app



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

    async_session_maker = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    session = async_session_maker()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()

@pytest_asyncio.fixture(autouse=True)
def mock_external_apis():
    with respx.mock:
        yield

@pytest_asyncio.fixture()
async def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as client:
        yield client
    app.dependency_overrides.clear()



@pytest_asyncio.fixture
async def registred_user(client: AsyncClient):
    payload = {
        "username": "string",
        "email": "user@example.com",
        "password": "stringst"
    }
    await client.post("/auth/register", json=payload)
    return payload

@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, registred_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": registred_user["email"],
            "password": registred_user["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}