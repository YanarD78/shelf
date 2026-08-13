from app.database import async_session_maker
from fastapi import Depends
from app.crud.users import UsersRepo
from app.services.auth import UsersManager

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

def get_user_repo(session: AsyncSession = Depends(get_session)) -> UsersRepo:
    return UsersRepo(session)

def get_user_manager(repo: UsersRepo = Depends(get_user_repo)) -> UsersManager:
    return UsersManager(repo)