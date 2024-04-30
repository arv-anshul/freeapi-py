from datetime import datetime
from enum import StrEnum, auto

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class TodoStatus(StrEnum):
    PENDING = auto()
    DONE = auto()


class Todo(BaseModel):
    status: TodoStatus = TodoStatus.PENDING
    date: datetime = Field(default_factory=datetime.now)
    title: str = "A short title for todo"
    description: str = "Long description for this todo."


class TodoInDB(Todo):
    id: ObjectId | str = Field(alias="_id")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return v
        if ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("id field not valid.")

    @field_serializer("id", return_type=str)
    def serialize_id(v):
        return str(v)


class UpdateTodo(BaseModel):
    title: str | None = None
    description: str | None = None
