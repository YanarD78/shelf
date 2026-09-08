from app.database import Base
from app.models.user import Users

from datetime import datetime, date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey, UniqueConstraint



class Movie(Base):
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)
    tmdb_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    poster_path: Mapped[str | None] = mapped_column()
    release_date: Mapped[str | None] = mapped_column()



class UsersWatchlists(Base):
    __tablename__ = "users_watchlists"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey(Movie.id), nullable=False)
    added_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uq_watchlist_user_movie"),
    )

class UsersWatched(Base):
    __tablename__ = "users_watched"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey(Movie.id), nullable=False)
    first_watch: Mapped[bool] = mapped_column(nullable=False)
    watched_at: Mapped[date | None] = mapped_column()
    rating: Mapped[float | None] = mapped_column()
    comment: Mapped[str | None] = mapped_column()
    added_at: Mapped[datetime] = mapped_column(server_default=func.now())