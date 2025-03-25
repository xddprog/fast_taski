from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.auth_methods import AuthMethod
from backend.infrastructure.database.models.user import User


class UserRepository(SqlAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def register_external_service_user(self, username: str, email: str, **kwargs):
        user = User(username=username, email=email)
        auth_method = AuthMethod(user=user, **kwargs)

        self.session.add_all([user, auth_method])
        await self.session.commit()
        await self.session.refresh(user)
        return user
