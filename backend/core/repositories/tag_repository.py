from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.tag import Tag


class TagRepository(SqlAlchemyRepository[Tag]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Tag)

    async def get_team_tags(self, team_id: int):
        query = select(Tag).where(Tag.team_id == team_id)
        return (await self.session.execute(query)).scalars().all()
    
    async def get_tags_by_ids(self, ids: list[int], team_id: int):
        query = select(Tag).where(Tag.id.in_(ids), Tag.team_id == team_id)
        return (await self.session.execute(query)).scalars().all()