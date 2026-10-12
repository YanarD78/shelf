from pydantic import BaseModel, Field, ConfigDict
from dataclasses import asdict
from app.dto.external import ExternalItem
from datetime import date, datetime



class MovieBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: str
    title: str
    overview: str | None = None
    release_date: date | None = None
    cover_url: str | None = None
    vote_average: float | None = None
    @classmethod
    def from_external(cls, item: ExternalItem):
        return cls.model_validate({**asdict(item), **item.extra})

class SearchedMovie(MovieBase):
    pass

class Movie(MovieBase):
    runtime_minutes: int | None = None
    backdrop_path: str | None = None
    genres: list | None = None



class SearchQuery(BaseModel):
    query: str = Field(min_length=2, max_length=100)
    page: int = Field(default=1, ge=1)



class GetWishlistOut(BaseModel):
    id: int
    user_id: int
    local_id: int
    note: str | None
    created_at: datetime

class PostWishlistRequest(BaseModel):
    external_id: str
    note: str | None = None

class PostWishlistResponse(BaseModel):
    id: int
    local_id: int

class PatchWishlistRequest(BaseModel):
    note: str

class WishlistQuery(BaseModel):
    added_before: date | None = None
    added_after: date | None = None
    added_at: date | None = None

    released_before: date | None = None
    released_after: date | None = None
    released_at: date | None = None

    limit: int | None = Field(default=None, ge=1)
    offset: int | None = Field(default=None, ge=1)



class GetCompletedOut(BaseModel):
    id: int
    user_id: int
    local_id: int
    is_first: bool
    completed_on: date | None
    rating: float | None
    comment: str | None
    created_at: datetime

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

    limit: int | None = Field(default=None, ge=1)
    offset: int | None = Field(default=None, ge=1)