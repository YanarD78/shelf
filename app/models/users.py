from app.database import Base

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, ForeignKey

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

class Preferences(Base):
    __tablename__ = "users_preferences"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    include_adult: Mapped[bool] = mapped_column(default=False)
    language: Mapped[str] = mapped_column(default="en-US")