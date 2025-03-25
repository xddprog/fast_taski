from pydantic import BaseModel


class BaseTaskModel(BaseModel):
    id: int
    name: str
    description: str
    deadline: str