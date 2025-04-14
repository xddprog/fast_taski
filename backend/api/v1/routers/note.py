from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, services
from backend.core.dto.note_dto import CreateNoteModel
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.post("/")
@inject
@cache.clear(namespaces=["notes"], queries=["team_id"])
async def create_note(
    request: Request,
    form: CreateNoteModel,
    team_id: int,
    team_service: FromDishka[services.TeamService],
    note_service: FromDishka[services.NoteService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_member=True)
    return await note_service.create_note(form, team_id, current_user.id)


@router.put("/{note_id}")
@inject
@cache.clear(namespaces=["notes", "note"], queries={"note": "note_id", "notes": "team_id"}, by_key=True)
async def update_note(
    request: Request,
    form: CreateNoteModel,
    note_id: int,
    team_id: int,
    note_service: FromDishka[services.NoteService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    is_admin = await team_service.check_user_rights(team_id, current_user.id, check_member=True)
    return await note_service.update_note(note_id, form, current_user.id, is_admin)


@router.get("/{note_id}")
@inject
@cache.get(namespace="note", expire=60, queries=["note_id"])
async def get_note(
    request: Request,
    note_id: int,
    team_id: int,
    note_service: FromDishka[services.NoteService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    await team_service.check_user_rights(team_id, current_user.id, check_member=True)
    return await note_service.get_note(note_id, current_user.id)


@router.delete("/{note_id}")
@inject
@cache.clear(namespaces=["notes", "note"], queries={"note": "note_id", "notes": "team_id"}, by_key=True)
async def delete_note(
    request: Request,
    note_id: int,
    team_id: int,
    note_service: FromDishka[services.NoteService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    is_admin = await team_service.check_user_rights(
        team_id, 
        current_user.id, 
        check_admin=True, 
        check_owner=True
    )
    return await note_service.delete_note(note_id, is_admin, current_user.id)


@router.patch("/{note_id}/members/add/{user_id}")
@inject
@cache.clear(namespaces=["note"], queries=["note_id"], by_key=True)
async def add_note_member(
    request: Request,
    note_id: int,
    user_id: int,
    team_id: int,
    note_service: FromDishka[services.NoteService],
    team_service: FromDishka[services.TeamService],
    current_user: BaseUserModel = Depends(get_current_user_dependency)
):
    is_admin = await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
    await team_service.check_user_rights(team_id, user_id, check_member=True)
    return await note_service.add_member(note_id, user_id, current_user.id, is_admin)


# @router.patch("/{note_id}/members/remove/{user_id}")
# @inject
# @cache.clear(namespaces=["note"], queries=["note_id"], by_key=True)
# async def delete_note_member(
#     request: Request,
#     note_id: int,
#     user_id: int,
#     team_id: int,
#     note_service: FromDishka[services.NoteService],
#     team_service: FromDishka[services.TeamService],
#     current_user: BaseUserModel = Depends(get_current_user_dependency)
# ):
#     await team_service.check_user_rights(team_id, current_user.id, check_admin=True)
#     return await note_service.delete_member(note_id, user_id, current_user.id)
    