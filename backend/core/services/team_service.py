from backend.core.dto.team_dto import CreateTeamModel, TeamModel
from backend.core.repositories import TeamRepository
from backend.core.services.base import BaseDbModelService
from backend.core.tasks_manager.tasks import BaseTask
from backend.infrastructure.database.models.team import Team


class TeamService(BaseDbModelService[Team]):
    async def create(self, form: CreateTeamModel):
        if form.avatar:
            self.tasks_manager.add_base_task(
                func=self.aws_client.upload_one_file,
                namespace="team",
                task_name="upload_team_avatar",
                func_args=(form.avatar, f"teams/{form.name}/{form.avatar.filename}"),
            )
            form.avatar = await self.aws_client.get_url(f"teams/{form.name}/{form.avatar.filename}")

        return await super().create(form)
    
    async def get_team(self, team_id: int):
        team = await self.repository.get_one(team_id)
        return TeamModel.model_validate(team, from_attributes=True)