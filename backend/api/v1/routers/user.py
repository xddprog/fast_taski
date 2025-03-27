import time
from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request
from fastapi import Depends

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, services
from backend.core.dto.team_dto import BaseTeamModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.get("/teams")
@inject
@cache.get(namespace="teams", expire=60)
async def get_team(
    request: Request,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    team_service: FromDishka[services.TeamService]
) -> list[BaseTeamModel]:
    return await team_service.get_user_teams(current_user.id)
