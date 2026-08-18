from pydantic import BaseModel

class Film(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str
    vote_average: float