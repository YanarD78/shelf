from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime
from app.config import settings
from datetime import datetime

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping = True
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    type_annotation_map = {datetime: DateTime(timezone=True)}