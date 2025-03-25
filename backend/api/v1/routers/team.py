from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import services
from backend.core.dto.team_dto import CreateTeamModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.post("/")
@inject
async def create_team(
    form: CreateTeamModel,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    team_service: FromDishka[services.TeamService]
):
    return await team_service.create(form)


@router.get("/{team_id}")
@inject
async def get_team():
    pass


@router.delete("/{team_id}")
@inject
async def delete_team():
    pass


@router.put("/{team_id}")
@inject
async def update_team():
    pass
