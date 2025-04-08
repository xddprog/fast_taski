import asyncio
from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, services
from backend.core.dto.task_dto import CreateTaskModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.post("/")
@inject
async def create_task(
    request: Request,
    form: CreateTaskModel,
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService],
    user_service: FromDishka[services.UserService],
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    tag_service: FromDishka[services.TagService]
):
    await team_service.check_team_exist(form.team_id)
    assignees = await user_service.get_users_by_ids(form.assignees)
    tags = await tag_service.get_tags_by_ids(form.tags, form.team_id)
    return await task_service.create(form, assignees, tags, current_user)
