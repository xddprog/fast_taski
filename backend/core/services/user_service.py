from uuid import uuid4
from pydantic import UUID4

from backend.core.repositories.user_repository import UserRepository
from backend.infrastructure.interfaces.service import DbModelServiceInterface


class UserService(DbModelServiceInterface):
    repository: UserRepository