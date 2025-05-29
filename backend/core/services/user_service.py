from backend.core.dto.user_dto import UpdateUserModel
from backend.core.repositories.user_repository import UserRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.auth_errors import UserAlreadyExists
from backend.infrastructure.errors.user_errors import UserNotFound


class UserService(BaseDbModelService[User]):
    repository: UserRepository

    async def check_user_exist(self, user_id: int):
        user = await self.repository.get_item(user_id)
        if user is None:
            raise UserNotFound
        return user
    
    async def get_users_by_ids(self, ids: list[int]) -> list[User]:
        return await self.repository.get_by_ids(ids)
    
    async def get_users_by_emails(self, emails: list[str], only_ids: bool = False) -> list[User]:
        return await self.repository.get_by_emails(emails, only_ids)
    
    async def get_user(self, user_id: int) -> User:
        return await self.repository.get_item(user_id)
    
    async def update_user(self, user_id: int, form: UpdateUserModel):
        if form.email:
            user = await self.repository.get_by_attribute("email", form.email)
            if user:
                raise UserAlreadyExists
            
        await self.repository.update_item(user_id, **form.model_dump(exclude_none=True))
        return await self.get_user(user_id)
    
    async def delete_user(self, user_id: int):
        user = await self.check_user_exist(user_id)
        await self.repository.delete_item(user)