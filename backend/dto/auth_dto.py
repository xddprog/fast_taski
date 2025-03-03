from datetime import datetime
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field

from backend.core.enums import AuthServices
from backend.dto.user_dto import BaseUserModel


class RegisterForm(BaseModel):
    username: str
    password: str
    email: str


class LoginForm(BaseModel):
    email: str
    password: str


class ExternalServiceUserData(BaseModel):
    username: str
    email: str | None = None
    external_id: int
    service: AuthServices