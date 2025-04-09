from pydantic import BaseModel

from backend.core.dto.tag_dto import TagModel
from backend.core.dto.user_dto import BaseUserModel, UserTeamModel


class BaseTaskModel(BaseModel):
    id: int
    name: str
    description: str
    deadline: str


class TimeEntryModel(BaseModel):
    id: int
    duration_minutes: int
    comment: str


class TaskModel(BaseTaskModel):
    tags: list[TagModel]
    assignees: list[BaseUserModel]
    creator: BaseUserModel
    time_entries: list[TimeEntryModel]
    parent: BaseTaskModel
    sub_tasks_count: int


class CreateTaskModel(BaseModel):
    team_id: int
    name: str
    description: str | None = None
    tags: list[int] = []
    assignees: list[int] = []


class UpdateTaskModel(BaseModel):
    name: str | None = None
    description: str | None = None
    deadline: str | None = None