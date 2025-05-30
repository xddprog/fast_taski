from fastapi import Form, UploadFile
from pydantic import BaseModel, field_validator

from backend.infrastructure.config.aws_config import AWS_STORAGE_CONFIG


class BaseUserModel(BaseModel):
    id: int
    username: str
    email: str | None = None
    avatar: str | None = None
    phone_number: str | None = None

    @field_validator("avatar")
    def validate_avatar(cls, v):
        if v:
            return f"{AWS_STORAGE_CONFIG.AWS_ENDPOINT_URL}/{AWS_STORAGE_CONFIG.AWS_BUCKET_NAME}/{v}"
        return v


class UserTeamModel(BaseModel):
    user: BaseUserModel
    role: str


class UpdateUserModel(BaseModel):
    username: str | None = Form(None)
    email: str | None = Form(None)
    avatar: UploadFile | None = Form(None)
    phone_number: str | None = Form(None)