from app.database import Base
from app.models.user import Users

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey, UniqueConstraint

class UsersWatchlists(Base):
    __tablename__ = "users_watchlists"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id))
    movie_id: Mapped[int] = mapped_column(nullable=False)
    added_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uq_user_service"),
    )