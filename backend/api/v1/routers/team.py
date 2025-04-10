from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, services
from backend.core.dto.team_dto import CreateTeamModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.post("/")
@inject
@cache.clear(namespaces=["teams"])
async def create_team(
    request: Request,
    form: CreateTeamModel,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    team_service: FromDishka[services.TeamService],
    user_service: FromDishka[services.UserService]
):
    await team_service.check_team_exist(form.name)
    members = await user_service.get_users_by_ids(form.members)
    return await team_service.create(form, current_user, members)


@router.get("/{team_id}")
@inject
@cache.get(namespace="team", expire=60)
async def get_team(
    request: Request,
    team_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    team_service: FromDishka[services.TeamService]
):
    return await team_service.get(team_id)


@router.delete("/{team_id}")
@inject
@cache.clear(namespaces=["team", "teams"])
async def delete_team(
    request: Request,
    team_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    team_service: FromDishka[services.TeamService]
):
    return await team_service.delete(team_id)


@router.put("/{team_id}")
@inject
async def update_team(
    request: Request,
    team_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    team_service: FromDishka[services.TeamService]
):
    pass
