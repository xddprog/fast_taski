from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.column import Column


class ColumnRepository(SqlAlchemyRepository[Column]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Column)
    
    async def get_team_dashboard(self, team_id: int):
        query = select(Column).where(Column.team_id == team_id).options(selectinload(Column.tasks))
        return (await self.session.execute(query)).scalars().all()