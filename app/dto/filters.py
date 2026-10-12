from dataclasses import dataclass
from datetime import date

@dataclass(slots=True)
class WishlistFilter:
    added_before: date | None
    added_after: date | None
    added_at: date | None

    released_before: date | None
    released_after: date | None
    released_at: date | None

    limit: int | None
    offset: int | None


@dataclass(slots=True)
class CompletedFilter:
    local_id: int | None

    completed_before: date | None
    completed_after: date | None
    completed_at: date | None

    limit: int | None
    offset: int | None