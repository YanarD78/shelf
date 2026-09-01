from pydantic import BaseModel

class Film(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str | None
    vote_average: float

class WatchlistResponse(BaseModel):
    id: int

class WatchlistRequest(BaseModel):
    movie_id: int