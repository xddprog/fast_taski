from datetime import datetime
from sqlalchemy import ARRAY, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.config.aws_config import AWS_STORAGE_CONFIG
from backend.infrastructure.database.models.base import Base
from backend.infrastructure.database.models.column import Column
from backend.infrastructure.database.models.comment import Comment


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    deadline: Mapped[datetime]
    _files: Mapped[list[str]] = mapped_column("files", ARRAY(String), nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id"), nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=True)

    parent: Mapped['Task'] = relationship(remote_side=[id], back_populates="sub_tasks")
    sub_tasks: Mapped[list['Task']] = relationship(back_populates="parent", cascade="all, delete-orphan",)
    time_entries: Mapped[list["TimeEntry"]] = relationship(back_populates="task")
    column: Mapped['Column'] = relationship(back_populates="tasks")
    creator = relationship("User", back_populates="created_tasks")
    assignees = relationship("User", back_populates="assigned_tasks", secondary="task_assignees")
    tags = relationship("Tag", back_populates="tasks", secondary="task_tags")
    comments: Mapped[list[Comment]] = relationship("Comment", back_populates="task")

    @hybrid_property
    def files(self):
        return [
            f"{AWS_STORAGE_CONFIG.AWS_ENDPOINT_URL}/{AWS_STORAGE_CONFIG.AWS_BUCKET_NAME}/{file}" 
            for file in self._files
        ]
    

class TimeEntry(Base):
    __tablename__ = "time_entries"

    duration_minutes: Mapped[int] = mapped_column(nullable=False) 
    comment: Mapped[str] = mapped_column(nullable=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    task = relationship("Task", back_populates="time_entries")
    user = relationship("User", back_populates="time_entries")


class TasksAssignees(Base):
    __tablename__ = "task_assignees"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)