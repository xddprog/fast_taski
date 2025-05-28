import asyncio
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
@cache.clear(namespaces=["dashboard"], queries=["team_id"], by_key=True)
async def create_task(
    request: Request,
    form: CreateTaskModel,
    team_id: int,
    task_service: FromDishka[services.TaskService],
    user_service: FromDishka[services.UserService],
    tag_service: FromDishka[services.TagService],
    team_service: FromDishka[services.TeamService],
    column_service: FromDishka[services.ColumnService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_member=True)
    await column_service.check_column_exist(form.column_id)
    if not form.assignees:
        assignees = [await user_service.get_user(current_user.id)]
    else:
        assignees = await user_service.get_users_by_ids(form.assignees)
    tags = await tag_service.get_tags_by_ids(form.tags, team_id)
    return await task_service.create_task(form, assignees, tags, current_user.id)


@router.get("/{task_id}")
@inject
@cache.get(namespace="task", expire=60, queries=["task_id"])
async def get_task(
    request: Request,
    team_id: int,
    task_id: int,
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_member=True)
    await task_service.check_task_exist(task_id)
    return await task_service.get_task(task_id, current_user.id)


@router.delete("/{task_id}")
@inject
@cache.clear(namespaces=["task", "dashboard"], queries={"task": "task_id", "dashboard": "team_id"}, by_key=True)
async def delete_task(
    request: Request,
    team_id: int,
    task_id: int,
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    await task_service.check_task_exist(task_id)
    return await task_service.delete_task(task_id)


@router.put("/{task_id}")
@inject
@cache.clear(
    namespaces=["task", "dashboard"], 
    queries={"task": "task_id", "team": "team_id"}, 
    by_key=True,
    set_after=True
)
async def update_task(
    request: Request,
    form: UpdateTaskModel,
    team_id: int,
    task_id: int,
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    await task_service.check_task_exist(task_id)
    return await task_service.update_task(task_id, form)


@router.delete("/{task_id}/assignees/{user_id}")
@inject
@cache.clear(namespaces=["task"], queries=["task_id"], by_key=True, set_after=True)
async def delete_task_assignee(
    request: Request,
    team_id: int,
    task_id: int,
    user_id: int,
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
) -> JSONResponse:
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    await team_service.check_user_rights(team_id, user_id, check_admin=True)
    await team_service.check_task_exist(task_id) 
    return await task_service.delete_assignee(task_id, user_id)


@router.post("/{task_id}/assignees/{user_id}")
@inject
@cache.clear(namespaces=["task"], queries=["task_id"], by_key=True, set_after=True)
async def add_task_assignee(
    request: Request,
    team_id: int,
    task_id: int,
    user_id: int,
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
) -> JSONResponse:
    await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    await team_service.check_user_rights(team_id, user_id, check_member=True)
    await task_service.check_task_exist(task_id)
    return await task_service.add_assignee(task_id, user_id)


@router.delete("/{task_id}/tags/{tag_id}")
@inject
@cache.clear(namespaces=["task"], queries=["task_id"], by_key=True, set_after=True)
async def delete_task_tag(
    request: Request,
    team_id: int,
    task_id: int,
    tag_id: int,
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService],
    tag_service: FromDishka[services.TagService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
) -> None:
    await team_service.check_user_rights(team_id, current_user.id, check_member=True)
    await task_service.check_task_exist(task_id)
    await tag_service.check_tag_exist(tag_id)
    return await task_service.delete_tag(task_id, tag_id)


@router.post("/{task_id}/tags/{tag_id}")
@inject
@cache.clear(namespaces=["task"], queries=["task_id"], by_key=True, set_after=True)
async def add_task_tag(
    request: Request,
    team_id: int,
    task_id: int,
    tag_id: int,
    task_service: FromDishka[services.TaskService],
    team_service: FromDishka[services.TeamService],
    tag_service: FromDishka[services.TagService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
) -> None:
    await team_service.check_user_rights(team_id, current_user.id, check_member=True)
    await task_service.check_task_exist(task_id)
    await tag_service.check_tag_exist(tag_id)
    return await task_service.add_tag(task_id, tag_id)