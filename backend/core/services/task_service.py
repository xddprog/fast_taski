from uuid import uuid4
from pydantic import Tag
from backend.core.dto.tag_dto import TagModel
from backend.core.dto.task_dto import BaseTaskModel, CreateTaskModel, TaskModel
from backend.core.repositories import TaskRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.task import Task
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.tag_erros import TagNotFound
from backend.infrastructure.errors.task_errors import TaskNotFound


class TaskService(BaseDbModelService[Task]):
    repository: TaskRepository

    async def create_task(self, form: CreateTaskModel, assignees: list[User], tags: list[Tag], current_user: int):
        form.assignees = assignees
        form.tags = tags

        if form.files:
            paths = [
                f'teams/{form.column_id}/tasks/{uuid4()}.{file.content_type.split("/")[1]}'
                for file in form.files
            ]
            await self.tasks_manager.add_base_task(
                func=self.aws_client.upload_many_files,
                namespace=f"upload_task_files_{form.column_id}",
                task_name=str(uuid4()),
                func_args=(form.files, paths),
            )
            form.files = paths

        task = await self.repository.add_item(**form.model_dump(), creator_id=current_user)
        return BaseTaskModel.model_validate(task, from_attributes=True)
    
    async def get_task(self, task_id: int, current_user_id: int):
        task = await self.repository.get_item(task_id)
        if task is None:
            raise TaskNotFound
        return TaskModel.model_validate(task, from_attributes=True)
    
    async def check_task_exist(self, task_id: int):
        task = await self.repository.check_task_exist(task_id)
        if task is None:
            raise TaskNotFound
        return task
    
    async def delete_assignee(self, task_id: int, user_id: int):
        await self.repository.delete_assignee(task_id, user_id)

    async def add_assignee(self, task_id: int, user_id: int):
        await self.repository.add_assignee(task_id, user_id)
        
    async def delete_tag(self, task_id: int, tag_id: int):
        tag = await self.repository.delete_tag(task_id, tag_id)
        if not tag:
            raise TagNotFound

    async def add_tag(self, task_id: int, tag_id: int):
        tag = await self.repository.check_task_tag_exist(task_id, tag_id)
        if not tag:
            raise TagNotFound
        return TagModel.model_validate(tag, from_attributes=True)
    
    async def update_task(self, task_id: int, form: CreateTaskModel):
        task = await self.repository.update_item(task_id, **form.model_dump(exclude_none=True))
        task = await self.repository.get_item(task_id)
        return TaskModel.model_validate(task, from_attributes=True)