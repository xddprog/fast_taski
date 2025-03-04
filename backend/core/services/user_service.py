from uuid import uuid4
from pydantic import UUID4

from backend.core.repositories.user_repository import UserRepository
from backend.core.services.base_service import BaseService


class UserService(BaseService):
    repository: UserRepository