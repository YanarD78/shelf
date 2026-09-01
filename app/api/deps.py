from app.database import async_session_maker
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from app.crud.user import UsersRepo
from app.crud.movies import MoviesRepo
from app.config import settings
from app.services.auth import UsersManager
from app.services.movie import MoviesManager
from httpx import AsyncClient
from app.clients.tmdb import TMDBClient
from app.core.security import security, decode_access_token
from app.core.exceptions import InvalidTokenError

from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated



# Get user language
SUPPORTED_LOCALES = settings.locales
DEFAULT_LOCALE = settings.def_locale

def parse_language(header_value: str) -> str | None:
    if not header_value:
        return None
    
    locales = []
    for part in header_value.split(","):
        part = part.strip()
        if ";q=" in part:
            l, q = part.split(";q=")
            locales.append((l.strip(), float(q)))
        else:
            locales.append((part, 1.0))
    locales.sort(key=lambda x: x[1], reverse=True)
    for l, _ in locales:
        if l in SUPPORTED_LOCALES:
            return l
    return None

def resolve_language(request: Request) -> str:
    return parse_language(request.headers.get("Accept-Language", "")) or DEFAULT_LOCALE
    
ResolveLang = Annotated[str, Depends(resolve_language)]



# Get current user id
def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)]
) -> int:
    if credentials is None:
        raise InvalidTokenError()
    return decode_access_token(credentials.credentials)

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
def get_user_manager(users_repo: UserRepoDep) -> UsersManager:
    return UsersManager(users_repo)

UserManagerDep = Annotated[UsersManager, Depends(get_user_manager)]



# Movie repo
def get_movies_repo(session: SessionDep) -> MoviesRepo:
    return MoviesRepo(session)

MovieRepoDep = Annotated[MoviesRepo, Depends(get_movies_repo)]

# Movie TMDB-Client
async def get_tmdb_client(client: HttpClientDep) -> TMDBClient:
    return TMDBClient(client)

TMDBClientDep = Annotated[TMDBClient, Depends(get_tmdb_client)]

# Movie manager
async def get_movie_manager(
    tmdbclient: TMDBClientDep,
    users_repo: UserRepoDep,
    movies_repo: MovieRepoDep,
    current_user: CurrentUser
) -> MoviesManager:
    return MoviesManager(tmdbclient, users_repo, movies_repo, current_user)

MovieManagerDep = Annotated[MoviesManager, Depends(get_movie_manager)]