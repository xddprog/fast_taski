from backend.core.dto.team_dto import BaseTeamModel
from backend.core.repositories.user_repository import UserRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.user import User
from backend.infrastructure.interfaces.service import DbModelServiceInterface


class UserService(BaseDbModelService[User]):
    async def get_user_teams(self, user_id: int) -> list[BaseTeamModel]:
        user = await self.get_one(user_id)
        return [BaseTeamModel.model_validate(team, from_attributes=True) for team in user.teams]