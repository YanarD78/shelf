from pydantic import BaseModel, Field, field_validator
from app.schemas.base import BaseContent
from datetime import date



class SearchedMovie(BaseContent):
    pass

class Movie(BaseContent):
    runtime_minutes: int | None = None
    backdrop_url: str | None = None
    genres: list[str] | None = None



class MovieSearchQuery(BaseModel):
    query: str = Field(min_length=2, max_length=100)
    page: int = Field(default=1, ge=1, le=500)
    year: int | None = Field(default=None, ge=1880)

    @field_validator("year")
    @classmethod
    def year_not_too_far(cls, v: int | None) -> int | None:
        if v is not None and v > date.today().year + 10:
            raise ValueError("Year is too far in the future")
        return v