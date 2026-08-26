from pydantic import BaseModel
from typing import Optional

class Film(BaseModel):
    id: int
    title: str
    overview: str
    release_date: Optional[str]
    vote_average: float