from backend.core.dto.column_dto import BaseColumnModel, ColumnModel, CreateColumnModel
from backend.core.repositories.column_repository import ColumnRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.column import Column
from backend.infrastructure.errors.column_errors import ColumnAlreadyExist, ColumnNotFound


class ColumnService(BaseDbModelService[Column]):
    repository: ColumnRepository

    async def check_column_exist(self, column_id: int):
        column = await self.repository.get_item(column_id)
        if column is None:
            raise ColumnNotFound
        return column

    async def create_column(self, team_id: int, form: CreateColumnModel):
        column = await self.repository.get_by_attribute("name", form.name)
        if column:
            raise ColumnAlreadyExist
        new_column = await self.repository.add_item(team_id=team_id, **form.model_dump())
        return ColumnModel(
            id=new_column.id, 
            name=new_column.name, 
            color=new_column.color, 
            tasks=[]
        )

    async def update_column(self, team_id: int, form: BaseColumnModel):
        column = await self.check_column_exist(team_id)
        if await self.repository.get_by_attribute("name", form.name):
            raise ColumnAlreadyExist
        updated_column = await self.repository.update_item(column.id, **form.model_dump())
        return ColumnModel.model_validate(updated_column, from_attributes=True)

    async def delete_column(self, column_id: int):
        column = await self.check_column_exist(column_id)
        return await self.repository.delete_item(column)
    
    async def get_by_team(self, team_id: int):
        columns = await self.repository.get_team_dashboard(team_id)
        return [ColumnModel.model_validate(column, from_attributes=True) for column in columns]