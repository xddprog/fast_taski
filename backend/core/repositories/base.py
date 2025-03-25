from typing import Any
from pydantic import UUID4
from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedColumn
from backend.infrastructure.interfaces.repository import RepositoryInterface


class SqlAlchemyRepository[ModelType](RepositoryInterface[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model

    async def get_item(self, item_id: int | UUID4 | str) -> ModelType:
        item = await self.session.get(self.model, item_id)
        return item

    async def get_all_items(self) -> list[ModelType]:
        query = select(self.model)
        items: Result = await self.session.execute(query)
        return items.scalars().all()

    async def get_by_attribute(
        self, attribute: MappedColumn[Any], value: str | UUID4 | int
    ) -> list[ModelType] | None:
        query = select(self.model).where(attribute == value)
        items: Result = await self.session.execute(query)
        return items.scalars().all()

    async def add_item(self, **kwargs: int | str | UUID4) -> ModelType:
        item = self.model(**kwargs)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_item(self, item: ModelType) -> None:
        await self.session.delete(item)
        await self.session.commit()

    async def update_item(
        self, item_id: int | str | UUID4, **update_values
    ) -> ModelType:
        query = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(update_values)
            .returning(self.model)
        )
        item: Result = await self.session.execute(query)
        await self.session.commit()
        return item.scalars().all()[0]

    async def get_model(self, **kwargs: int | str | UUID4) -> ModelType:
        return self.model(**kwargs)
