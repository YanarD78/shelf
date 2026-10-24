from pydantic import BaseModel, ConfigDict
from dataclasses import asdict
from app.dto.external import ExternalItem
from datetime import date



class BaseContent(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: str
    title: str
    description: str | None = None
    release_date: date | None = None
    cover_url: str | None = None
    vote_average: float | None = None
    @classmethod
    def from_external(cls, item: ExternalItem):
        return cls.model_validate({**asdict(item), **item.extra})