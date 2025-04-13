from backend.core.dto.tag_dto import TagModel
from backend.core.repositories.tag_repository import TagRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.tag import Tag
from backend.infrastructure.errors.tag_erros import TagNotFound


class TagService(BaseDbModelService[Tag]):
    repository: TagRepository

    async def get_tags_by_ids(self, ids: list[int], team_id: int):
        tags = await self.repository.get_tags_by_ids(ids, team_id)
        if len(tags) != len(ids):
            raise TagNotFound
        return tags

    async def check_tag_exist(self, tag_id: int):
        tag = await self.repository.get_item(tag_id)
        if tag is None:
            raise TagNotFound
        
    async def create_tag(self, form: Tag, team_id: int) -> TagModel:
        tag = await self.repository.add_item(**form.model_dump(), team_id=team_id)
        return TagModel.model_validate(tag, from_attributes=True)
    
    async def delete_tag(self, tag_id: int):
        tag = await self.repository.get_item(tag_id)
        if tag is None:
            raise TagNotFound
        await self.repository.delete_item(tag)