from uuid import uuid4
from backend.core.dto.note_dto import CreateNoteModel, NoteModel
from backend.core.dto.user_dto import BaseUserModel
from backend.core.repositories import NoteRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.note import Note
from backend.infrastructure.errors.note_errors import NoteNotFound
from backend.infrastructure.errors.team_errors import UserNotFoundRights


class NoteService(BaseDbModelService[Note]):
    repository: NoteRepository

    async def check_user_rights(self, note_id: int, user_id: int, is_admin: bool = False):
        note = await self.repository.get_item(note_id)
        print(note)
        if note is None:
            raise NoteNotFound
        elif note.creator_id != user_id and not is_admin:
            raise UserNotFoundRights
        return note
    
    async def get_note(self, note_id: int) -> NoteModel:
        note = await self.repository.get_item(note_id)
        if note is None:
            raise NoteNotFound
        return NoteModel.model_validate(note, from_attributes=True)
    
    async def create_note(self, form: CreateNoteModel, team_id: int, user_id: int):
        if form.files:
            paths = [
                f'teams/{team_id}/notes/{uuid4()}.{file.content_type.split("/")[-1]}'
                for file in form.files
            ]
            await self.tasks_manager.add_base_task(
                func=self.aws_client.upload_many_files,
                namespace=f"upload_note_files_{team_id}",
                task_name=str(uuid4()),
                func_args=(form.files, paths),
            )
            form.files = paths
        
        note = await self.repository.add_item(team_id=team_id, creator_id=user_id, **form.model_dump())
        return NoteModel.model_validate(note, from_attributes=True)
    
    async def get_team_notes(self, team_id: int):
        notes = await self.repository.get_team_notes(team_id)
        return [NoteModel.model_validate(note, from_attributes=True) for note in notes]
    
    async def delete_note(self, note_id: int, user_id: int, is_admin: bool):
        if not is_admin:
            await self.check_user_rights(note_id, user_id)

        note = await self.get_note(note_id)
        await self.repository.delete_item(note)

    async def update_note(self, note_id: int, form: CreateNoteModel, user_id: int, is_admin: bool):
        if not is_admin:
            await self.check_user_rights(note_id, user_id)

        note = await self.repository.update_item(note_id, **form.model_dump(exclude_none=True))
        return NoteModel.model_validate(note, from_attributes=True)
    
    async def add_member(self, note_id: int, user_id: int, current_user_id: int, is_admin: bool):
        if not is_admin:
            await self.check_user_rights(note_id, current_user_id)

        await self.repository.add_member(note_id, user_id)

        note = await self.get_note(note_id)
        return NoteModel.model_validate(note, from_attributes=True)