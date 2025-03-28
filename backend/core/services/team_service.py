from backend.core.dto.team_dto import BaseTeamModel, CreateTeamModel, TeamModel, UpdateTeamModel
from backend.core.dto.user_dto import BaseUserModel
from backend.core.repositories import TeamRepository
from backend.core.services.base import BaseDbModelService
from backend.core.tasks_manager.tasks import BaseTask
from backend.infrastructure.database.models.team import Team
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.team_errors import TeamAlreadyExist, TeamNotFound
from backend.infrastructure.interfaces import repository
from backend.utils.enums import TeamRoles


class TeamService(BaseDbModelService[Team]):
    repository: TeamRepository
    
    async def check_team_exist(self, name: str):
        team = await self.repository.get_by_attribute("name", name)
        if team:
            raise TeamAlreadyExist
        
    async def create(self, form: CreateTeamModel, current_user: BaseUserModel, members: list[User]):
        form.members = members

        if form.avatar:
            self.tasks_manager.add_base_task(
                func=self.aws_client.upload_one_file,
                namespace="team",
                task_name="upload_team_avatar",
                func_args=(form.avatar, f"teams/{form.name}/{form.avatar.filename}"),
            )
            form.avatar = await self.aws_client.get_url(f"teams/{form.name}/{form.avatar.filename}")

        new_team = await self.repository.add_item(**form.model_dump(), owner_id=current_user.id)
        await self.repository.add_member(new_team.id, current_user.id, TeamRoles.OWNER)
        await self.repository.refresh_item(new_team)
        return BaseTeamModel.model_validate(new_team, from_attributes=True)
    
    async def get(self, team_id: int):
        team = await self.repository.get_item(team_id)
        if team is None:
            return TeamNotFound
        return TeamModel.model_validate(team, from_attributes=True) 
    
    async def get_user_teams(self, user_id: int):
        teams = await self.repository.get_user_teams(user_id)
        return [TeamModel.model_validate(team, from_attributes=True) for team in teams]
    
    async def update(self, item_id: int, item: UpdateTeamModel):
        team = await self.repository.get_item(item_id)
        if team is None:
            return TeamNotFound

        if item.avatar:
            self.tasks_manager.add_base_task(
                func=self.aws_client.upload_one_file,
                namespace="team",
                task_name="upload_team_avatar",
                func_args=(item.avatar, f"teams/{team.name}/{item.avatar.filename}"),
            )
            item.avatar = await self.aws_client.get_url(f"teams/{team.name}/{item.avatar.filename}")
        return await self.repository.update_item(item_id, **item.model_dump())