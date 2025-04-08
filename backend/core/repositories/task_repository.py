from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.task import Task
from backend.infrastructure.database.models.team import Team


class TaskRepository(SqlAlchemyRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Team)

    async def get_team_tasks(self, team_id: int, offset: int, limit: int):
        query = (
            select(Task, count(Task.comments))
            .where(Task.team_id == team_id)
            .offset(offset)
            .limit(limit)
        )
        return (await self.session.execute(query)).all()

    async def get_item(self, item_id: int) -> tuple[Task, int]:
        query = (
            select(
                Task, 
                count(Task.comments), 
                count(Task.sub_tasks)
            )
            .where(Task.id == item_id)
            .options(
                selectinload(Task.creator),
                selectinload(Task.assignees),
                selectinload(Task.tags)
            )
        )
        item = await self.session.execute(query)
        return item.first()