from app.database import Base
from app.models.user import Users
from app.models.media import ContentItem
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey, UniqueConstraint, CheckConstraint, Index
from datetime import datetime, date



class Wishlist(Base):
    __tablename__ = "user_wishlist"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    local_id: Mapped[int] = mapped_column(ForeignKey(ContentItem.id), nullable=False)
    note: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "local_id", name="uq_wishlist_user"),
    )

class Completed(Base):
    __tablename__ = "user_completed"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    local_id: Mapped[int] = mapped_column(ForeignKey(ContentItem.id), nullable=False)
    is_first: Mapped[bool] = mapped_column(nullable=False)
    completed_on: Mapped[date | None]
    rating: Mapped[float | None]
    comment: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        CheckConstraint("rating BETWEEN 0 AND 10", name="ck_completed_rating"),
        Index("ix_completed_user_local", "user_id", "local_id")
    )