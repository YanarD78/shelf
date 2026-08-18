from app.database import async_session_maker
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.crud.users import UsersRepo
from app.services.auth import UsersManager
from app.services.movies import MoviesManager
from httpx import AsyncClient
from app.clients.tmdb import TMDBClient
from app.core.security import oauth_scheme, decode_token

from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession



def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(oauth_scheme)) -> int:
    token = credentials.credentials
    user_id = decode_token(token)
    return user_id



# HTTP-Client
async def get_http_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient() as client:
        yield client

# SQLAlchemy session
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise



# User repo
def get_user_repo(session: AsyncSession = Depends(get_session)) -> UsersRepo:
    return UsersRepo(session)

# User manager
def get_user_manager(repo: UsersRepo = Depends(get_user_repo)) -> UsersManager:
    return UsersManager(repo)



# Movie TMDB-Client
async def get_tmdb_client(client: AsyncClient = Depends(get_http_client)) -> TMDBClient:
    return TMDBClient(client)

# Movie manager
async def get_movie_manager(
    tmdbclient: TMDBClient = Depends(get_tmdb_client),
    repo: UsersRepo = Depends(get_user_repo),
    current_user: int = Depends(get_current_user)
) -> MoviesManager:
    return MoviesManager(tmdbclient, repo, current_user)