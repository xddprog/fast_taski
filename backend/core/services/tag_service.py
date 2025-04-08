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
