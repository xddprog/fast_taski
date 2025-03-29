from pydantic import BaseModel

from backend.core.dto.task_dto import BaseTaskModel


class ColumnModel(BaseModel):
    name: str
    color: str
    tasks: list[BaseTaskModel]