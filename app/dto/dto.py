from dataclasses import dataclass
from datetime import date, datetime

@dataclass(slots=True)
class WatchlistFilter:
    added_before: datetime | None = None
    added_after: datetime | None = None
    added_at: datetime | None = None
    released_before: date | None = None
    released_after: date | None = None
    released_at: date | None = None

@dataclass(slots=True)
class WatchedFilter:
    local_id: int | None
    added_before: datetime | None = None
    added_after: datetime | None = None
    added_at: datetime | None = None