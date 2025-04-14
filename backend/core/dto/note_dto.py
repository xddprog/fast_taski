from datetime import datetime
from fastapi import Form, UploadFile
from pydantic import BaseModel, field_validator

from backend.core.dto.user_dto import BaseUserModel


class BaseNoteModel(BaseModel):
    id: int
    title: str
    creator: BaseUserModel
    created_at: datetime | str
    updated_at: datetime | str

    @field_validator("created_at", "updated_at")
    def convert_to_string(cls, v):
        return v.strftime('%Y-%m-%d %H:%M')


class NoteModel(BaseNoteModel):
    text: str
    files: list[str]
    members: list[BaseUserModel]


class CreateNoteModel(BaseModel):
    title: str = Form()
    text: str = Form()
    files: list[UploadFile] = Form(default=[])
    