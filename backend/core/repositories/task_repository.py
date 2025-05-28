from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload
from sqlalchemy.sql.functions import count
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.tag import TaskTag
from backend.infrastructure.database.models.task import Task, TasksAssignees
from backend.infrastructure.database.models.comment import Comment


class TaskRepository(SqlAlchemyRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Task)

    async def get_team_tasks(self, team_id: int, offset: int, limit: int):
        query = (
            select(Task, count(Task.comments))
            .where(Task.team_id == team_id)
            .offset(offset)
            .limit(limit)
        )
        return (await self.session.execute(query)).all()

    async def get_item(self, item_id: int) -> Task:
        comments_count_subquery = (
            select(func.count(Comment.id))
            .where(Comment.task_id == Task.id)
            .correlate(Task)
            .scalar_subquery()
            .label("comment_count")
        )

        SubTask = aliased(Task)
        sub_tasks_count_subquery = (
            select(func.count(SubTask.id))
            .where(SubTask.parent_id == Task.id)
            .correlate(Task)
            .scalar_subquery()
            .label("sub_task_count")
        )

        query = (
            select(
                Task,
                comments_count_subquery,
                sub_tasks_count_subquery
            )
            .where(Task.id == item_id)
            .options(
                selectinload(Task.creator),
                selectinload(Task.assignees),
                selectinload(Task.tags),
                selectinload(Task.time_entries),
            )
        )

        result = await self.session.execute(query)
        task_with_counts = result.first()
        if task_with_counts is None:
            return None

        task, comment_count, sub_tasks_count = task_with_counts
        task.comments_count = comment_count
        task.sub_tasks_count = sub_tasks_count
        return task
    
    async def check_task_exist(self, task_id: int):
        query = select(Task).where(Task.id == task_id)
        return (await self.session.execute(query)).scalar_one_or_none()
    
    async def delete_tag(self, task_id: int, tag_id: int):
        query = delete(TaskTag).where(TaskTag.task_id == task_id, TaskTag.tag_id == tag_id)
        item = await self.session.execute(query)
        await self.session.commit()

    async def add_tag(self, task_id: int, tag_id: int):
        tag = TaskTag(task_id=task_id, tag_id=tag_id)
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag
    
    async def delete_assignee(self, task_id: int, user_id: int):
        query = select(TasksAssignees).where(TasksAssignees.task_id == task_id, TasksAssignees.user_id == user_id)
        await self.session.execute(query)
        await self.session.commit()

    async def add_assignee(self, task_id: int, user_id: int):
        assignee = TasksAssignees(task_id=task_id, user_id=user_id)
        self.session.add(assignee)
        await self.session.commit()

    async def check_tag_exist(self, task_id: int, tag_id: int):
        query = select(TaskTag).where(TaskTag.tag_id == tag_id, TaskTag.task_id == task_id)
        return (await self.session.execute(query)).scalar_one_or_none()