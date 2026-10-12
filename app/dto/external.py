from dataclasses import dataclass
from datetime import date

@dataclass(slots=True)
class ExternalItem:
    external_id: str
    title: str
    overview: str | None
    release_date: date | None
    cover_url: str | None
    vote_average: float | None
    extra: dict