from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.note import Note


class NoteRepository(SqlAlchemyRepository[Note]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Note)
    