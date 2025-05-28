from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, services
from backend.core.dto.column_dto import CreateColumnModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.post("/")
@inject
@cache.clear(namespaces=["team"], queries=["team_id"], by_key=True, set_after=True)
async def create_column(
    request: Request,
    team_id: int,
    form: CreateColumnModel,
    column_service: FromDishka[services.ColumnService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency),
) :
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await column_service.create_column(team_id, form)



@router.put("/{column_id}")
@inject
@cache.clear(namespaces=["dashboard"], queries=["team_id"], by_key=True, set_after=True)
async def update_column(
    request: Request,
    team_id: int,
    form: CreateColumnModel,
    column_service: FromDishka[services.ColumnService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await column_service.update_column(team_id, form)


@router.delete("/{column_id}")
@inject
@cache.clear(namespaces=["dashboard"], queries=["team_id"], by_key=True, set_after=True) 
async def delete_column(
    request: Request,
    team_id: int,
    column_id: int,
    column_service: FromDishka[services.ColumnService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await column_service.delete_column(column_id)