from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import ScalarResult

from backend.repositories import BaseRepository


class BaseService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @staticmethod
    async def check_item(item, error: HTTPException) -> None:
        if not item:
            raise error

    @staticmethod
    async def model_dump(db_model: ScalarResult, dto_model: BaseModel) -> BaseModel:
        return dto_model.model_validate(db_model, from_attributes=True)

    async def dump_items(
        self, db_models: list[ScalarResult], dto_model: BaseModel
    ) -> list[BaseModel] | list:
        return [await self.model_dump(model, dto_model) for model in db_models]
