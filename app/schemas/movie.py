from pydantic import BaseModel, Field, ConfigDict, field_validator
from dataclasses import asdict
from app.dto.external import ExternalItem
from datetime import date, datetime

class BaseContent(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: str
    title: str
    description: str | None = None
    release_date: date | None = None
    cover_url: str | None = None
    vote_average: float | None = None
    @classmethod
    def from_external(cls, item: ExternalItem):
        return cls.model_validate({**asdict(item), **item.extra})



class SearchedMovie(BaseContent):
    pass

class Movie(BaseContent):
    runtime_minutes: int | None = None
    backdrop_url: str | None = None
    genres: list[str] | None = None


class SearchedGame(BaseContent):
    pass

class Game(BaseContent):
    pass


class SearchedBook(BaseContent):
    pass

class Book(BaseContent):
    pass



class SearchQuery(BaseModel):
    query: str = Field(min_length=2, max_length=100)
    page: int = Field(default=1, ge=1, le=500)
    year: int | None = Field(default=None, ge=1880)

    @field_validator("year")
    @classmethod
    def year_not_too_far(cls, v: int | None) -> int | None:
        if v is not None and v > date.today().year + 10:
            raise ValueError("Year is too far in the future")
        return v



class GetWishlistList(BaseModel):
    id: int
    local_id: int
    note: str | None
    created_at: datetime
    content: SearchedMovie | SearchedGame | SearchedBook

class GetWishlistItem(BaseModel):
    id: int
    local_id: int
    note: str | None
    created_at: datetime
    content: Movie | Game | Book

class PostWishlistRequest(BaseModel):
    external_id: str
    note: str | None = None

class PostWishlistResponse(BaseModel):
    id: int
    local_id: int

class PatchWishlistRequest(BaseModel):
    note: str | None

class WishlistQuery(BaseModel):
    added_before: date | None = None
    added_after: date | None = None
    added_at: date | None = None

    released_before: date | None = None
    released_after: date | None = None
    released_at: date | None = None

    limit: int | None = Field(default=None, ge=1, le=100)
    offset: int | None = Field(default=None, ge=0)



class GetCompletedList(BaseModel):
    id: int
    local_id: int
    is_first: bool
    completed_on: date | None
    rating: float | None
    comment: str | None
    created_at: datetime
    content: SearchedMovie | SearchedGame | SearchedBook

class GetCompletedItem(BaseModel):
    id: int
    local_id: int
    is_first: bool
    completed_on: date | None
    rating: float | None
    comment: str | None
    created_at: datetime
    content: Movie | Game | Book

class PostCompletedRequest(BaseModel):
    external_id: str
    is_first: bool
    completed_on: date | None = None
    rating: float | None = Field(default=None, ge=0.0, le=10.0)
    comment: str | None = None

class PostCompletedResponse(BaseModel):
    id: int
    local_id: int

class PatchCompletedRequest(BaseModel):
    is_first: bool | None = None
    completed_on: date | None = None
    rating: float | None = Field(default=None, ge=0.0, le=10.0)
    comment: str | None = None

class CompletedQuery(BaseModel):
    local_id: int | None = None

    completed_before: date | None = None
    completed_after: date | None = None
    completed_at: date | None = None

    limit: int | None = Field(default=None, ge=1, le=100)
    offset: int | None = Field(default=None, ge=0)