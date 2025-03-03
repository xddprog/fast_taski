import hashlib
import hmac
import json
from datetime import datetime, timedelta

from h11 import Request
from jwt import InvalidTokenError, encode, decode
from passlib.context import CryptContext

from backend.core.config.oauth_configs import load_jwt_config
from backend.dto.auth_dto import ExternalServiceUserData, LoginForm, RegisterForm
from backend.dto.user_dto import BaseUserModel
from backend.database.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.services.base_service import BaseService
from backend.errors.auth_errors import (
    InvalidLoginData,
    InvalidToken,
    UserAlreadyNotRegister,
    UserAlreadyRegister,
)


class AuthService(BaseService):
    repository: UserRepository

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__config = load_jwt_config()
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.repository.get_by_attribute(
            self.repository.model.username, 
            username
        )
        return None if not user else user[0]
    
    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.repository.get_by_attribute(
            self.repository.model.email, 
            email
        )
        return None if not user else user[0]
    
    async def verify_password(
        self, password: str, hashed_password: str
    ) -> bool:
        return self.context.verify(password, hashed_password)

    async def authenticate_user(self, form: LoginForm, is_external: bool = False) -> User:
        user = await self.get_user_by_username(form.username)
        if not user and is_external:
            return False
        if not user:
            raise UserAlreadyNotRegister
        if not is_external and not await self.verify_password(form.password, user.password):
            raise InvalidLoginData
        return await self.model_dump(user, BaseUserModel)

    async def create_access_token(self, username: str) -> str:
        expire = datetime.now() + timedelta(minutes=self.__config.JWT_ACCESS_TOKEN_TIME)
        data = {"exp": expire, "sub": username}
        token = encode(
            data,
            self.__config.JWT_SECRET, 
            algorithm=self.__config.JWT_ALGORITHM
        )
        return token
    
    async def create_refresh_token(self, username: str ):
        expire = datetime.now() + timedelta(days=self.__config.JWT_REFRESH_TOKEN_TIME)
        data = {"exp": expire, "sub": username}
        return encode(
            data, 
            self.__config.JWT_SECRET, 
            algorithm=self.__config.JWT_ALGORITHM
        )

    async def verify_token(self, token: str) -> str:
        if not token:
            raise InvalidToken
        try:
            payload = decode(
                token,
                self.__config.JWT_SECRET,
                algorithms=[self.__config.JWT_ALGORITHM],
            )
            username = payload.get("sub")
            if not username or not await self.get_user_by_username(username):
                raise InvalidToken
            return username
        except (InvalidTokenError, AttributeError) as e:
            raise InvalidToken

    async def check_user_exist(self, username: str) -> User:
        user = await self.get_user_by_username(username)
        if user is None:
            raise InvalidToken
        return await self.model_dump(user, BaseUserModel)

    async def register_user(self, form: RegisterForm) -> BaseUserModel:
        user = await self.get_user_by_email(form.email)
        if user:
            raise UserAlreadyRegister

        form.password = self.context.hash(form.password)
        new_user = await self.repository.add_item(**form.model_dump())
        return await self.model_dump(new_user, BaseUserModel)

    async def register_external_service_user(
        self, 
        form: ExternalServiceUserData
    ) -> BaseUserModel:
        user = await self.get_user_by_username(form.username)
        if user:
            return user

        new_user = await self.repository.register_external_service_user(
            **form.model_dump(),
        )
        return await self.model_dump(new_user, BaseUserModel)

    async def auth_extarnal_service_user(self, form: RegisterForm) -> BaseUserModel:
        user_registered = await self.authenticate_user(form, is_external=True)
        if not user_registered:
            return await self.register_external_service_user(form)
        return user_registered

    async def check_user_in_app(self, form: RegisterForm | LoginForm, is_register: bool) -> bool:
        user = await self.get_user_by_email(form.email)
        if user and is_register:
            raise UserAlreadyRegister
        return user.username if user else False