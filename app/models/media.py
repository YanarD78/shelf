from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey, UniqueConstraint, CheckConstraint, String, ARRAY, Text
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, date
from enum import StrEnum

class MediaType(StrEnum):
    movie = "movie"
    game = "game"
    book = "book"

class ExternalType(StrEnum):
    tmdb = "tmdb"
    rawg = "rawg"



class ContentItem(Base):
    __tablename__ = "content_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[str] = mapped_column(nullable=False)

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    cover_url: Mapped[str | None] = mapped_column(String(500))
    vote_average: Mapped[float | None]
    release_date: Mapped[date | None]

    external_id: Mapped[str] = mapped_column(nullable=False)
    source: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint("media_type", "source", "external_id", name="uq_content"),
        CheckConstraint("media_type IN ('movie','game','book')", name="ck_content_media_type")
    )

    __mapper_args__ = {
        "polymorphic_on": "media_type",
        "polymorphic_identity": "content_item"
    }



class Movie(ContentItem):
    __tablename__ = "movie"
    media_id: Mapped[int] = mapped_column(ForeignKey("content_item.id", ondelete="CASCADE"), primary_key=True)
    runtime_minutes: Mapped[int | None]
    backdrop_url: Mapped[str | None] = mapped_column(String(500))
    genres: Mapped[list] = mapped_column(ARRAY(String))

    __mapper_args__ = {"polymorphic_identity": "movie", "polymorphic_load": "selectin"}


class Game(ContentItem):
    __tablename__ = "game"
    media_id: Mapped[int] = mapped_column(ForeignKey("content_item.id", ondelete="CASCADE"), primary_key=True)

    tba: Mapped[bool]
    metacritic: Mapped[int | None]
    playtime: Mapped[int]
    platforms: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    genres: Mapped[list[str]] = mapped_column(ARRAY(String))
    stores: Mapped[dict] = mapped_column(JSONB)
    

    __mapper_args__ = {"polymorphic_identity": "game", "polymorphic_load": "selectin"}
    

class Book(ContentItem):
    __tablename__ = "book"
    media_id: Mapped[int] = mapped_column(ForeignKey("content_item.id", ondelete="CASCADE"), primary_key=True)

    authors: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    page_count: Mapped[int | None]

    __mapper_args__ = {"polymorphic_identity": "book", "polymorphic_load": "selectin"}