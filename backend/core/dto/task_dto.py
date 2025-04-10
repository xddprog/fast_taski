from datetime import datetime
from pydantic import BaseModel, field_validator

from backend.core.dto.tag_dto import TagModel
from backend.core.dto.user_dto import BaseUserModel, UserTeamModel


class BaseTaskModel(BaseModel):
    id: int
    name: str
    description: str
    deadline: str | datetime
    column_id: int

    @field_validator('deadline')
    def convert_to_string(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M')
        return v


class TimeEntryModel(BaseModel):
    id: int
    duration_minutes: int
    comment: str


class TaskModel(BaseTaskModel):
    tags: list[TagModel]
    assignees: list[BaseUserModel]
    creator: BaseUserModel
    time_entries: list[TimeEntryModel]
    parent: BaseTaskModel | None = None
    parent_id: int | None = None
    sub_tasks_count: int
    comments_count: int


class CreateTaskModel(BaseModel):
    column_id: int
    name: str
    deadline: datetime
    description: str | None = None
    tags: list[int] = []
    assignees: list[int] = []

    @field_validator('deadline')
    def convert_to_naive(cls, v):
        if v.tzinfo is not None:  # If timezone-aware
            return v.replace(tzinfo=None)  # Convert to naive
        return v


class UpdateTaskModel(BaseModel):
    name: str | None = None
    description: str | None = None
    deadline: str | None = None