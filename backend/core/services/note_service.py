from backend.core.repositories import NoteRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.note import Note


class NoteService(BaseDbModelService[Note]):
    pass