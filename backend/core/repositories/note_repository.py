from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.note import Note, UserNote


class NoteRepository(SqlAlchemyRepository[Note]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Note)
    
    async def get_team_notes(self, team_id: int):
        query = select(Note).where(Note.team_id == team_id)
        return (await self.session.execute(query)).scalars().all()

    async def add_member(self, note_id: int, user_id: int):
        query = insert(UserNote).values(note_id=note_id, user_id=user_id).returning(UserNote.user)
        new_member = await self.session.execute(query)
        await self.session.commit()
        new_member = new_member.scalars().all()[0]
        await self.session.refresh(new_member)
        return new_member