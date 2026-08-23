from app.database import async_session_maker
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.crud.user import UsersRepo
from app.services.auth import UsersManager
from app.services.movie import MoviesManager
from httpx2 import AsyncClient
from app.clients.tmdb import TMDBClient
from app.core.security import oauth_scheme, decode_token
from app.core.exceptions import InvalidTokenError

from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(oauth_scheme)]
) -> int:
    if credentials is None:
        raise InvalidTokenError()
    return decode_token(credentials.credentials)

CurrentUser = Annotated[int, Depends(get_current_user)]


# HTTP-Client
async def get_http_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient() as client:
        yield client

HttpClientDep = Annotated[AsyncClient, Depends(get_http_client)]


# SQLAlchemy session
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# User repo
def get_user_repo(session: SessionDep) -> UsersRepo:
    return UsersRepo(session)

UserRepoDep = Annotated[UsersRepo, Depends(get_user_repo)]

# User manager
def get_user_manager(repo: UserRepoDep) -> UsersManager:
    return UsersManager(repo)

UserManagerDep = Annotated[UsersManager, Depends(get_user_manager)]


# Movie TMDB-Client
async def get_tmdb_client(client: HttpClientDep) -> TMDBClient:
    return TMDBClient(client)

TMDBClientDep = Annotated[TMDBClient, Depends(get_tmdb_client)]

# Movie manager
async def get_movie_manager(
    tmdbclient: TMDBClientDep,
    repo: UserRepoDep,
    current_user: CurrentUser
) -> MoviesManager:
    return MoviesManager(tmdbclient, repo, current_user)

MovieManagerDep = Annotated[MoviesManager, Depends(get_movie_manager)]