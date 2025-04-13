from uuid import uuid4

from fastapi.responses import JSONResponse
import orjson
from backend.core.dto.team_dto import BaseTeamModel, CreateTeamModel, InviteMembersModel, TeamModel, UpdateTeamModel
from backend.core.dto.user_dto import BaseUserModel
from backend.core.repositories import TeamRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.team import Team
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.auth_errors import InvalidToken
from backend.infrastructure.errors.team_errors import TeamAlreadyExist, TeamNotFound, UserAlreadyInTeam, UserNotFoundRights, UserNotInTeam
from backend.infrastructure.errors.user_errors import UserNotFound
from backend.infrastructure.interfaces import repository
from backend.utils.enums import TeamRoles


class TeamService(BaseDbModelService[Team]):
    repository: TeamRepository
    
    async def check_team_exist(self, name: str):
        team = await self.repository.get_by_attribute("name", name)
        if team:
            raise TeamAlreadyExist
        
    async def check_user_rights(
        self, 
        team_id: int, 
        current_user_id: int, 
        check_member: bool = False,
        check_owner: bool = False,
        check_admin: bool = False,
        full_load: bool = False
    ):
        team = await self.repository.get_item(team_id, full_load)
        if team is None:
            raise TeamNotFound
        if check_owner and team.owner_id != current_user_id:
            raise UserNotFoundRights
        if check_admin and not await self.repository.check_admin(team_id, current_user_id):
            raise UserNotFoundRights
        if check_member and not await self.repository.check_member(team_id, current_user_id):
            raise UserNotInTeam
        return team
        
    async def create_team(self, form: CreateTeamModel, current_user: BaseUserModel, members: list[int]):
        if form.avatar:
            self.tasks_manager.add_base_task(
                func=self.aws_client.upload_one_file,
                namespace=f"team_{form.name}",
                task_name="upload_team_avatar",
                func_args=(form.avatar, f"teams/{form.name}/{form.avatar.filename}"),
            )
            form.avatar = await self.aws_client.get_url(f"teams/{form.name}/{form.avatar.filename}")

        new_team = await self.repository.add_item(
            name=form.name, 
            description=form.description, 
            avatar=form.avatar, 
            owner_id=current_user.id
        )
        await self.repository.add_members(new_team.id, members, TeamRoles.OWNER)
        await self.repository.refresh_item(new_team)
        await self.repository.add_members(new_team.id, [current_user.id], TeamRoles.OWNER)
        await self.repository.refresh_item(new_team)
        return BaseTeamModel.model_validate(new_team, from_attributes=True)
    
    async def get_team(self, team_id: int, current_user_id: int = None):
        team = await self.check_user_rights(team_id, current_user_id, True, full_load=True)
        return TeamModel.model_validate(team, from_attributes=True) 
    
    async def get_user_teams(self, user_id: int):
        teams = await self.repository.get_user_teams(user_id)
        return [BaseTeamModel.model_validate(team, from_attributes=True) for team in teams]
    
    async def update_team(self, team_id: int, item: UpdateTeamModel, current_user_id: int):
        if item.name:
            await self.check_team_exist(item.name)
            
        team = await self.check_user_rights(team_id, current_user_id, check_owner=True)

        if item.avatar:
            self.tasks_manager.add_base_task(
                func=self.aws_client.upload_one_file,
                namespace="team",
                task_name="upload_team_avatar",
                func_args=(item.avatar, f"teams/{team.name}/{item.avatar.filename}"),
            )
            item.avatar = await self.aws_client.get_url(f"teams/{team.name}/{item.avatar.filename}")
            
        team = await self.repository.update_item(team_id, **item.model_dump())
        return BaseTeamModel.model_validate(team, from_attributes=True)
    
    async def delete_team(self, team_id: int, current_user_id: int):
        team = await self.check_user_rights(team_id, current_user_id, check_owner=True)
        await self.repository.delete_item(team)
        return JSONResponse(content={"detail": f"Команда {team.name} успешно удалена"})
    
    async def change_owner(self, team_id: int, user_id: int, current_user_id: int):
        team = await self.check_user_rights(team_id, current_user_id, check_admin=True)
        await self.repository.check_member(team_id, user_id)        
        await self.repository.update_member(team_id, user_id, role=TeamRoles.OWNER)
        await self.repository.update_member(team_id, current_user_id, role=TeamRoles.ADMIN)
        await self.repository.refresh_item(team)
        return TeamModel.model_validate(team, from_attributes=True)
    
    async def invite_members(self, team_id: int, form: InviteMembersModel, current_user_id: int):
        team = await self.check_user_rights(team_id, current_user_id, check_admin=True)
        
        tokens = [uuid4() for _ in range(len(form.emails))]
        for email, token in zip(form.emails, tokens):
            await self.redis_client.set(f"{team_id}:{token}", email, ttl=1000000)
            await self.tasks_manager.add_base_task(
                func=self.smtp_clients.invite_members,
                namespace=f"team_{team_id}",
                task_name="send_verification_code",
                func_args=([email], team.id, team.name, token),
            )
        return JSONResponse(content={"detail": "Запросы успешно отправлены"})
    
    async def accept_invite(self, team_id: int, token: str, current_user: BaseUserModel):
        code_email = (await self.redis_client.get(f"{team_id}:{token}")).decode()
        
        if code_email is None:
            raise UserNotFoundRights
        if code_email != current_user.email:
            raise InvalidToken
        if await self.repository.check_member(team_id, current_user.id):
            raise UserAlreadyInTeam
        
        await self.redis_client.delete_by_key(f"{team_id}:{token}")
        return await self.repository.add_members(team_id, [current_user.id], TeamRoles.MEMBER)
    
    async def delete_member(self, team_id: int, user_id: int, current_user_id: int):
        team = await self.check_user_rights(team_id, current_user_id, check_admin=True)
        if team.owner_id == user_id:
            raise UserNotFoundRights
        
        await self.repository.delete_member(team_id, user_id)

        team = await self.repository.get_item(team_id, full_load=True)
        return TeamModel.model_validate(team, from_attributes=True)