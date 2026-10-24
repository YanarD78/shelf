from fastapi import Depends, Query, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import AsyncClient
from app.database import async_session_maker
from app.models.media import MediaType
from app.repositories.user import UserRepo
from app.repositories.diary import DiaryRepo
from app.services.auth import UserManager
from app.services.diary import Manager
from app.providers.tmdb import TMDBClient
from app.providers.rawg import RAWGClient
from app.core.security import decode_access_token
from app.core.exceptions import InvalidTokenError
from app.schemas.diary import WishlistQuery, CompletedQuery
from app.schemas.movie import MovieSearchQuery
from app.schemas.game import GameSearchQuery
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncIterator
from typing import Annotated



security = HTTPBearer(auto_error=False)



# _____Get current user id_____
def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)]
) -> int:
    if credentials is None:
        raise InvalidTokenError()
    return decode_access_token(credentials.credentials)

CurrentUser = Annotated[int, Depends(get_current_user)]



# _____HTTP-Client_____
def get_http_client(request: Request) -> AsyncClient:
    return request.app.state.http

HttpClientDep = Annotated[AsyncClient, Depends(get_http_client)]



# _____SQLAlchemy session_____
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

SessionDep = Annotated[AsyncSession, Depends(get_session, scope="function")]



# _____User repo_____
def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(session)

UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]

# _____User manager_____
def get_user_manager(users_repo: UserRepoDep) -> UserManager:
    return UserManager(users_repo)

UserManagerDep = Annotated[UserManager, Depends(get_user_manager)]



# _____TMDB-Client_____
def get_tmdb_client(client: HttpClientDep) -> TMDBClient:
    return TMDBClient(client)

TMDBClientDep = Annotated[TMDBClient, Depends(get_tmdb_client)]

# _____RAWG-Client_____
def get_rawg_client(client: HttpClientDep) -> RAWGClient:
    return RAWGClient(client)

RAWGClientDep = Annotated[RAWGClient, Depends(get_rawg_client)]



# _____Diary repo_____
def get_repo(session: SessionDep) -> DiaryRepo:
    return DiaryRepo(session)

DiaryRepoDep = Annotated[DiaryRepo, Depends(get_repo)]



# _____Manager_____
def get_manager(
    tmdbclient: TMDBClientDep,
    rawgclient: RAWGClientDep,
    users_repo: UserRepoDep,
    diary_repo: DiaryRepoDep,
    current_user: CurrentUser
) -> Manager:
    return Manager(
        {
            MediaType.movie: tmdbclient,
            MediaType.game: rawgclient
        },
        users_repo,
        diary_repo,
        current_user
    )

ManagerDep = Annotated[Manager, Depends(get_manager)]



# _____Get watchlist query_____
GetWishlistQuery = Annotated[WishlistQuery, Query()]

# _____Get watched query_____
GetCompletedQuery = Annotated[CompletedQuery, Query()]



# _____Movie search query_____
GetMovieSearchQuery = Annotated[MovieSearchQuery, Query()]

# _____Game search query_____
GetGameSearchQuery = Annotated[GameSearchQuery, Query()]