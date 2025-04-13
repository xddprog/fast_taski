from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, services
from backend.core.dto.tag_dto import CreateTagModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.post("/")
@inject
@cache.clear(namespaces=["tags"], queries=["team_id"])
async def create_tag(
    request: Request,
    team_id: int,
    form: CreateTagModel,
    tag_servics: FromDishka[services.TagService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await tag_servics.create_tag(form, team_id)


@router.delete("/{tag_id}")
@inject
@cache.clear(namespaces=["tags"], queries=["team_id"])
async def delete_tag(
    request: Request,
    team_id: int,
    tag_id: int,
    tag_servics: FromDishka[services.TagService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await tag_servics.delete_tag(tag_id)