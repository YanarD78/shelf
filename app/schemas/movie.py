from pydantic import BaseModel
from datetime import date, datetime



class SearchedFilm(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str | None
    vote_average: float



class GetWatchlistOut(BaseModel):
    id: int
    user_id: int
    local_id: int
    note: str | None
    added_at: datetime

class PostWatchlistRequest(BaseModel):
    external_id: int

class PostWatchlistResponse(BaseModel):
    id: int
    local_id: int

class WatchlistQuery(BaseModel):
    added_before: datetime | None = None
    added_after: datetime | None = None
    added_at: datetime | None = None
    released_before: date | None = None
    released_after: date | None = None
    released_at: date | None = None



class GetWatchedOut(BaseModel):
    id: int
    user_id: int
    local_id: int
    first_watch: bool
    watched_at: date | None
    rating: float | None
    comment: str | None
    added_at: datetime

class PostWatchedRequest(BaseModel):
    external_id: int
    first_watch: bool
    watched_at: date
    rating: float | None = None
    comment: str | None = None

class PostWatchedResponse(BaseModel):
    id: int
    local_id: int

class WatchedQuery(BaseModel):
    local_id: int | None = None
    added_before: datetime | None = None
    added_after: datetime | None = None
    added_at: datetime | None = None