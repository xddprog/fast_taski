from pydantic import BaseModel

from backend.core.dto.task_dto import BaseTaskModel


class BaseColumnModel(BaseModel):
    id: int
    name: str
    color: str

class CreateColumnModel(BaseModel):
    name: str
    color: str

class ColumnModel(BaseColumnModel):
    tasks: list[BaseTaskModel] = []