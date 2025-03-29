from dns import query, update
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.team import Team, UserTeam
from backend.utils.enums import TeamRoles


class TeamRepository(SqlAlchemyRepository[Team]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Team)

    async def add_member(self, team_id: int, user_id: int, role: TeamRoles):
        self.session.add(UserTeam(team_id=team_id, user_id=user_id, role=role))
        await self.session.commit()

    async def get_user_teams(self, user_id: int):
        query = (
            select(Team)
            .join(UserTeam)
            .where(UserTeam.user_id == user_id)
            .options(
                selectinload(Team.owner),
                selectinload(Team.members),
                selectinload(Team.columns) 
            )
        )
        items = await self.session.execute(query)
        return items.scalars().all()
        
    async def get_item(self, item_id: int) -> Team:
        query = (
            select(Team)
            .where(Team.id == item_id)
            .options(
                selectinload(Team.owner),
                selectinload(Team.members),
                selectinload(Team.columns) 
            )
        )
        item = await self.session.execute(query)
        return item.scalar_one_or_none()
    
    async def update_member(self, team_id: int, user_id: int, **kwargs):
        query = (
            update(UserTeam)
            .where(UserTeam.team_id == team_id , UserTeam.user_id == user_id)
            .values(**kwargs)
            .returning(UserTeam)
        )