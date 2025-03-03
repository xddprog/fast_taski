from backend.database.models.auth_methods import AuthMethod
from backend.repositories.base import SqlAlchemyRepository
from backend.database.models.user import User


class UserRepository(SqlAlchemyRepository):
    model = User

    async def register_external_service_user(self, username: str, email: str, **kwargs):
        user = User(username=username, email=email)
        auth_method = AuthMethod(user=user, **kwargs)

        self.session.add_all([user, auth_method])
        await self.session.commit()
        await self.session.refresh(user)
        return user
