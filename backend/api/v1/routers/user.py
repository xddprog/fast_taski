import time
from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Form, Request
from fastapi import Depends
import orjson

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, services
from backend.core.clients.redis_client import RedisClient
from backend.core.dto.team_dto import BaseTeamModel
from backend.core.dto.user_dto import BaseUserModel, UpdateUserModel


router = APIRouter()


@router.get("/teams")
@inject
@cache.get(namespace="teams", expire=60, queries=["user_id"])
async def get_user_teams(
    request: Request,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    team_service: FromDishka[services.TeamService],
    user_service: FromDishka[services.UserService]
) -> list[BaseTeamModel]:
    await user_service.check_user_exist(current_user.id)
    return await team_service.get_user_teams(current_user.id)


#todo
@router.put("/")
@inject
async def update_user(
    user_service: FromDishka[services.UserService],
    form: UpdateUserModel,
    current_user: BaseUserModel = Depends(get_current_user_dependency),
):
    await user_service.check_user_exist(current_user.id)
    return await user_service.update_user(current_user.id, form)


@router.delete("/")
@inject
async def delete_user(
    request: Request, 
    user_service: FromDishka[services.UserService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    return await user_service.delete_user(current_user.id)