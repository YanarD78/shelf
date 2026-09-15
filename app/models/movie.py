from app.database import Base
from app.models.user import Users
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey, UniqueConstraint
from datetime import datetime, date




class Movie(Base):
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    poster_path: Mapped[str | None] = mapped_column()
    release_date: Mapped[date | None] = mapped_column()



class UserWatchlist(Base):
    __tablename__ = "user_watchlist"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    local_id: Mapped[int] = mapped_column(ForeignKey(Movie.id), nullable=False)
    note: Mapped[str | None] = mapped_column()
    added_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "local_id", name="uq_watchlist_user_movie"),
    )

class UserWatched(Base):
    __tablename__ = "user_watched"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    local_id: Mapped[int] = mapped_column(ForeignKey(Movie.id), nullable=False)
    first_watch: Mapped[bool] = mapped_column(nullable=False)
    watched_at: Mapped[date | None] = mapped_column()
    rating: Mapped[float | None] = mapped_column()
    comment: Mapped[str | None] = mapped_column()
    added_at: Mapped[datetime] = mapped_column(server_default=func.now())