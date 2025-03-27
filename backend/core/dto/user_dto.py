from pydantic import BaseModel


class BaseUserModel(BaseModel):
    id: int
    username: str
    email: str | None = None
    avatar: str | None = None


class UserTeamModel(BaseModel):
    user: BaseUserModel
    role: str