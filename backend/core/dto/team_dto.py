from fastapi import Form, UploadFile
from pydantic import BaseModel

from backend.core.dto.column_dto import ColumnModel
from backend.core.dto.task_dto import BaseTaskModel
from backend.core.dto.user_dto import BaseUserModel, UserTeamModel


class BaseTeamModel(BaseModel):
    id: int
    name: str
    avatar: str | None = None
    description: str


class CreateTeamModel(BaseModel):
    name: str
    avatar: UploadFile = Form(default=None)
    description: str | None = Form(default=None)
    members: list[str] = Form(default=[])   


class UpdateTeamModel(BaseModel):
    name: str
    avatar: UploadFile = Form(default=None)
    description: str | None = Form(default=None)
    

class TeamModel(BaseTeamModel):
    owner: BaseUserModel
    members: list[UserTeamModel]
    owner: BaseUserModel


class InviteMembersModel(BaseModel):
    emails: list[str]