from datetime import datetime
from uuid import uuid4
from pydantic import UUID4, BaseModel, EmailStr, Field

from backend.core.enums import AuthServices
from backend.dto.user_dto import BaseUserModel


class RegisterForm(BaseModel):
    username: str
    password: str
    email: EmailStr


class LoginForm(BaseModel):
    email: str
    password: str
    username: None = None


class ExternalServiceUserData(BaseModel):
    username: str
    email: EmailStr | None = None
    external_id: int
    service: AuthServices