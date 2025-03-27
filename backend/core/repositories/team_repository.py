from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.task import Task
from backend.infrastructure.database.models.team import Team


class TeamRepository(SqlAlchemyRepository[Team]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Team)