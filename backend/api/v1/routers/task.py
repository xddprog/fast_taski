import asyncio
from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, services
from backend.core.dto.task_dto import CreateTaskModel, UpdateTaskModel
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
    assignees = await user_service.get_users_by_emails(form.assignees)
    tags = await tag_service.get_tags_by_ids(form.tags, form.team_id)
    return await task_service.create(form, assignees, tags, current_user)


@router.get("/{task_id}")
@inject
@cache.get(namespace="task", expire=60)
async def get_task(
    request: Request,
    team_id: int,
    task_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService]
):
    await task_service.check_task_exist(task_id, team_id)
    await team_service.check_user_rights(team_id, current_user.id, check_member=True)
    return await task_service.get_task(task_id, current_user.id)


@router.delete("/{task_id}")
@inject
@cache.clear(namespaces=["task", "tasks"])
async def delete_task(
    request: Request,
    team_id: int,
    task_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService]
):
    await task_service.check_task_exist(task_id, team_id)
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await task_service.delete(task_id)


@router.put("/{task_id}")
@inject
@cache.clear(namespaces=["task", "tasks"])
async def update_task(
    request: Request,
    form: UpdateTaskModel,
    team_id: int,
    task_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService]
):
    await task_service.check_task_exist(team_id)
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await task_service.update(task_id, form)


@router.delete("/{task_id}/assignees/{user_id}")
@inject
@cache.clear(namespaces=["task"])
async def delete_task_assignee(
    request: Request,
    team_id: int,
    task_id: int,
    user_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService]
) -> JSONResponse:
    await team_service.check_task_exist(task_id)
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await task_service.delete_assignee(task_id, user_id)


@router.post("/{task_id}/assignees/{user_id}")
@inject
@cache.clear(namespaces=["task"])
async def add_task_assignee(
    request: Request,
    team_id: int,
    task_id: int,
    user_id: int,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService]
) -> JSONResponse:
    await team_service.check_task_exist(task_id)
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    return await task_service.add_assignee(task_id, user_id)