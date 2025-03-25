from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi import Depends

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import services
from backend.core.dto.team_dto import BaseTeamModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.get("/teams")
@inject
async def get_team(
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    user_service: FromDishka[services.UserService]
) -> list[BaseTeamModel]:
    return await user_service.get_user_teams(current_user.id)
