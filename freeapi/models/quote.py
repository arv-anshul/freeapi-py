from datetime import date

from pydantic import BaseModel, Field


class Quote(BaseModel):
    author: str
    authorSlug: str
    content: str
    dateAdded: date = Field(default_factory=date.today)
    dateModified: date = Field(default_factory=date.today)
    id: int
    length: int
    tags: list[str]
