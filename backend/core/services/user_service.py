from backend.core.dto.team_dto import BaseTeamModel
from backend.core.repositories.user_repository import UserRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.user import User
from backend.infrastructure.interfaces.service import DbModelServiceInterface


class UserService(BaseDbModelService[User]):
    repository: UserRepository
    async def get_users_by_ids(self, ids: list[int]):
        return await self.repository.get_by_ids(ids)