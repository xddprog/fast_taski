from fastapi import Form, UploadFile
from pydantic import BaseModel

from backend.core.dto.task_dto import BaseTaskModel
from backend.core.dto.user_dto import BaseUserModel


class BaseTeamModel(BaseModel):
    id: int
    name: str
    avatar: str
    description: str
    owner_id: int


class CreateTeamModel(BaseModel):
    name: str
    avatar: UploadFile = Form(default=None)
    description: str | None = Form(default=None)
    members: list[int] = Form(default=[])   


class TeamModel(BaseTeamModel):
    members: list[BaseUserModel]
    owner: BaseUserModel
    tasks: list[BaseTaskModel]