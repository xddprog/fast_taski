from backend.core.dto.team_dto import CreateTeamModel, TeamModel
from backend.core.dto.user_dto import BaseUserModel
from backend.core.repositories import TeamRepository
from backend.core.services.base import BaseDbModelService
from backend.core.tasks_manager.tasks import BaseTask
from backend.infrastructure.database.models.team import Team
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.team_errors import TeamAlreadyExist


class TeamService(BaseDbModelService[Team]):
    async def check_team_exist(self, name: str):
        team = await self.repository.get_by_attribute(self.repository.model.name, name)
        if team:
            raise TeamAlreadyExist
        
    async def create(self, form: CreateTeamModel, current_user: BaseUserModel, members: list[User]):
        if form.avatar:
            self.tasks_manager.add_base_task(
                func=self.aws_client.upload_one_file,
                namespace="team",
                task_name="upload_team_avatar",
                func_args=(form.avatar, f"teams/{form.name}/{form.avatar.filename}"),
            )
            form.avatar = await self.aws_client.get_url(f"teams/{form.name}/{form.avatar.filename}")

        form.members = members
        new_team = await super().create(**form.model_dump(), owner_id=current_user.id)
        return TeamModel.model_validate(new_team, from_attributes=True)
    
    async def get_team(self, team_id: int):
        team = await self.repository.get_one(team_id)
        return TeamModel.model_validate(team, from_attributes=True) 