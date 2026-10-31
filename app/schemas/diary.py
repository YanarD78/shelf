from pydantic import BaseModel, Field
from app.schemas.movie import Movie, SearchedMovie
from app.schemas.game import Game, SearchedGame
from datetime import date, datetime



class GetWishlistList(BaseModel):
    id: int
    local_id: int
    note: str | None
    created_at: datetime
    content: SearchedMovie | SearchedGame

class GetWishlistItem(BaseModel):
    id: int
    local_id: int
    note: str | None
    created_at: datetime
    content: Movie | Game

class PostWishlistRequest(BaseModel):
    external_id: str
    note: str | None = Field(default=None, max_length=200)

class PostWishlistResponse(BaseModel):
    id: int
    local_id: int

class PatchWishlistRequest(BaseModel):
    note: str | None = Field(default=None, max_length=200)

class WishlistQuery(BaseModel):
    added_before: date | None = None
    added_after: date | None = None
    added_at: date | None = None

    released_before: date | None = None
    released_after: date | None = None
    released_at: date | None = None

    limit: int | None = Field(default=50, ge=1, le=100)
    offset: int | None = Field(default=None, ge=0)



class GetCompletedList(BaseModel):
    id: int
    local_id: int
    is_first: bool
    completed_on: date | None
    rating: float | None
    comment: str | None
    created_at: datetime
    content: SearchedMovie | SearchedGame

class GetCompletedItem(BaseModel):
    id: int
    local_id: int
    is_first: bool
    completed_on: date | None
    rating: float | None
    comment: str | None
    created_at: datetime
    content: Movie | Game

class PostCompletedRequest(BaseModel):
    external_id: str
    is_first: bool
    completed_on: date | None = None
    rating: float | None = Field(default=None, ge=0.0, le=10.0)
    comment: str | None = Field(default=None, max_length=2000)

class PostCompletedResponse(BaseModel):
    id: int
    local_id: int

class PatchCompletedRequest(BaseModel):
    is_first: bool | None = None
    completed_on: date | None = None
    rating: float | None = Field(default=None, ge=0.0, le=10.0)
    comment: str | None = Field(default=None, max_length=2000)

class CompletedQuery(BaseModel):
    local_id: int | None = None

    completed_before: date | None = None
    completed_after: date | None = None
    completed_at: date | None = None

    limit: int | None = Field(default=50, ge=1, le=100)
    offset: int | None = Field(default=None, ge=0)