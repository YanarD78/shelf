from pydantic import BaseModel, Field, field_validator
from fastapi import Query
from app.schemas.base import BaseContent
from datetime import date



class SearchedGame(BaseContent):
    pass

class Game(BaseContent):
    tba: bool
    metacritic: float | None
    playtime: int | None
    platforms: list
    genres: list
    stores: list



class GameSearchQuery(BaseModel):
    query: str = Field(min_length=2, max_length=100)
    page: int = Field(default=1, ge=1, le=500)
    dates: str | None = None
    parent_platforms: str | None = None
    platforms: str | None = None

    @field_validator("dates")
    @classmethod
    def date_validator(cls, dates: str | None) -> None:
        if isinstance(dates, str):
            arr = dates.split(",")
            for x in arr:
                date.fromisoformat(x)
        return dates

    @field_validator("platforms", "parent_platforms")
    @classmethod
    def platform_validator(cls, platforms: str | None) -> None:
        if isinstance(platforms, str):
            arr = platforms.split(",")
            for x in arr:
                int(x)
        return platforms