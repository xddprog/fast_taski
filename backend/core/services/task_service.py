from backend.core.dto.task_dto import CreateTaskModel
from backend.core.repositories import TaskRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.task import Task
from backend.infrastructure.interfaces.service import DbModelServiceInterface


class TaskService(BaseDbModelService[Task]):
    async def create(self, form: CreateTaskModel):
        pass