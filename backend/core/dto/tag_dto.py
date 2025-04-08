from pydantic import BaseModel


class TagModel(BaseModel):
    id: int
    name: str