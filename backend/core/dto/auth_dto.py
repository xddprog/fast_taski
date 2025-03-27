from pydantic import BaseModel, EmailStr

from backend.utils.enums import AuthServices


class RegisterForm(BaseModel):
    username: str
    password: str
    email: EmailStr


class LoginForm(BaseModel):
    email: EmailStr
    password: str


class ExternalServiceUserData(BaseModel):
    username: str
    email: EmailStr | None = None
    external_id: int
    service: AuthServices