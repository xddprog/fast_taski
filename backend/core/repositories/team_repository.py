from dns import query, update
from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.column import Column
from backend.infrastructure.database.models.team import Team, UserTeam
from backend.utils.enums import TeamRoles


class TeamRepository(SqlAlchemyRepository[Team]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Team)

    async def add_members(self, team_id: int, users: list[int], role: TeamRoles):
        for user_id in users:
            self.session.add(UserTeam(team_id=team_id, user_id=user_id, role=role))
        await self.session.commit()

    async def get_user_teams(self, user_id: int ):
        query = select(Team).join(UserTeam).where(UserTeam.user_id == user_id)
        items = await self.session.execute(query)
        return items.scalars().all()
        
    async def get_item(self, item_id: int, full_load: bool = False) -> Team:
        query = select(Team).where(Team.id == item_id)
        if full_load:
            query = query.options(
                selectinload(Team.owner),
                selectinload(Team.members).selectinload(UserTeam.user),
            )
        else:
            query = query.options(selectinload(Team.owner))
        item = await self.session.execute(query)
        return item.scalar_one_or_none()
    
    async def update_member(self, team_id: int, user_id: int, **kwargs):
        query = (
            update(UserTeam)
            .where(UserTeam.team_id == team_id , UserTeam.user_id == user_id)
            .values(**kwargs)
            .returning(UserTeam)
        )

    async def delete_member(self, team_id: int, user_id: int):
        await self.session.execute(
            delete(UserTeam).where(UserTeam.team_id == team_id, UserTeam.user_id == user_id)
        )
        await self.session.commit()

    async def check_member(self, team_id: int, user_id: int):
        query = select(UserTeam).where(UserTeam.team_id == team_id, UserTeam.user_id == user_id)
        return (await self.session.execute(query)).scalar_one_or_none()
    
    async def check_admin(self, team_id: int, user_id: int):
        query = (
            select(UserTeam)
            .where(
                UserTeam.team_id == team_id, 
                UserTeam.user_id == user_id, 
                or_(UserTeam.role == TeamRoles.ADMIN, UserTeam.role == TeamRoles.OWNER)
            )
        )
        return (await self.session.execute(query)).scalar_one_or_none()