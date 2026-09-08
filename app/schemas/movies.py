from pydantic import BaseModel
from datetime import date



class Film(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str | None
    vote_average: float



class WatchlistRequest(BaseModel):
    movie_id: int

class WatchlistResponse(BaseModel):
    id: int
    movie_id: int



class WatchedRequest(BaseModel):
    movie_id: int
    first_watch: bool
    watched_at: date
    rating: float | None = None
    comment: str | None = None

class WatchedResponse(BaseModel):
    id: int
    movie_id: int