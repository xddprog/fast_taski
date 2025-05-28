from sqlalchemy import insert, select, update
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
        query = insert(UserNote).values(note_id=note_id, user_id=user_id)
        await self.session.execute(query)
        await self.session.commit()
    
    async def add_item(self, **kwargs: int) -> Note:
        query = insert(Note).values(**kwargs).returning(Note).options(selectinload(Note.members))
        item = await self.session.execute(query)
        await self.session.commit()
        note = item.scalar_one()
        await self.session.refresh(note)
        return note
    
    async def get_item(self, note_id: int) -> Note:
        query = select(Note).where(Note.id == note_id).options(selectinload(Note.members))
        item = await self.session.execute(query)
        return item.scalar_one_or_none()
    
    async def update_item(self, note_id: int, **kwargs: int) -> Note:
        query = update(Note).where(Note.id == note_id).values(**kwargs).returning(Note).options(selectinload(Note.members))
        item = await self.session.execute(query)
        await self.session.commit()
        note = item.scalar_one_or_none()
        await self.session.refresh(note)
        return note