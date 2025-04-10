from pydantic import Tag
from backend.core.dto.task_dto import BaseTaskModel, CreateTaskModel, TaskModel
from backend.core.repositories import TaskRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.task import Task
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.task_errors import TaskNotFound


class TaskService(BaseDbModelService[Task]):
    repository: TaskRepository

    async def create_task(self, form: CreateTaskModel, assignees: list[User], tags: list[Tag], current_user: int):
        form.assignees = assignees
        form.tags = tags
        return await self.repository.add_item(**form.model_dump(), creator_id=current_user)
    
    async def get_task(self, task_id: int, current_user_id: int):
        task, sub_tasks_count = await self.repository.get_item(task_id)
        if task is None:
            raise TaskNotFound
        return TaskModel(
            id=task.id,
            name=task.name,
            description=task.description,
            deadline=task.deadline,
            assignees=task.assignees,
            tags=task.tags,
            sub_tasks_count=sub_tasks_count,
            creator=task.creator,
            time_entries=task.time_entries
        )
    
    async def check_task_exist(self, task_id: int, team_id: int):
        task = await self.repository.check_task_exist(task_id)
        if task is None:
            raise TaskNotFound
        return task
    
    async def delete_assignee(self, task_id: int, user_id: int):
        await self.repository.delete_assignee(task_id, user_id)
        