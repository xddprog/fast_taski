from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, clients, services
from backend.core.dto.team_dto import CreateTeamModel, InviteMembersModel, UpdateTeamModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.post("/")
@inject
@cache.clear(namespaces=["teams"])
async def create_team(
    request: Request,
    form: CreateTeamModel,
    team_service: FromDishka[services.TeamService],
    user_service: FromDishka[services.UserService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_team_exist(form.name)
    members = await user_service.get_users_by_emails(form.members, only_ids=True)
    return await team_service.create_team(form, current_user, members)


@router.get("/{team_id}")
@inject
@cache.get(namespace="team", expire=60, queries=["team_id"])
async def get_team(
    request: Request,
    team_id: int,
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    return await team_service.get_team(team_id, current_user.id)


@router.get("/{team_id}/dashboard")
@inject
@cache.get(namespace="dashboard", expire=60, queries=["team_id"])
async def get_team_dashboard(
    request: Request,
    team_id: int,
    column_service: FromDishka[services.ColumnService],
    current_user: BaseUserModel = Depends(get_current_user_dependency),
):
    return await column_service.get_by_team(team_id)


@router.delete("/{team_id}")
@inject
@cache.clear(namespaces=["team", "dashboard"], queries=["team_id"])
async def delete_team(
    request: Request,
    team_id: int,
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    return await team_service.delete_team(team_id, current_user.id)


@router.patch("/{team_id}/owner/{user_id}")
@inject
@cache.clear(namespaces=["team"], queries=["team_id"], set_after=True)
async def change_team_owner(
    request: Request,
    team_id: int,
    user_id: int,
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    return await team_service.change_owner(team_id, user_id, current_user.id)


@router.put("/{team_id}")
@inject
@cache.clear(namespaces=["team", "teams"], queries=["team_id"], set_after=True)
async def update_team(
    request: Request,
    form: UpdateTeamModel,
    team_id: int,
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    return await team_service.update_team(team_id, form, current_user.id)


@router.post("/{team_id}/members")
@inject
async def add_team_members(
    form: InviteMembersModel,
    team_id: int,
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
) -> JSONResponse:
    return await team_service.invite_members(team_id, form, current_user.id)


@router.patch("/{team_id}/members/{token}")
@inject
@cache.clear(namespaces=["team"], queries=["team_id"], set_after=True)
async def accept_invite(
    request: Request, 
    team_id: int, 
    token: str, 
    team_service: FromDishka[services.TeamService],
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)]
):
    return await team_service.accept_invite(team_id, token, current_user)


@router.delete("/{team_id}/members/{user_id}")
@inject
@cache.clear(namespaces=["team", "teams"], queries=["team_id"])
async def delete_team_member(
    request: Request,
    team_id: int,
    user_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    team_service: FromDishka[services.TeamService]
):
    return await team_service.delete_member(team_id, user_id, current_user.id)
