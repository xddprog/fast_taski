from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.database.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    deadline: Mapped[datetime]
    max_time: Mapped[int]
    is_completed: Mapped[bool] = mapped_column(default=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))

    team = relationship("Team", back_populates="tasks")
    parent: Mapped['Task'] = relationship(remote_side=[id], lazy="selectin")
    sub_tasks: Mapped[list['Task']] = relationship(        
        back_populates="parent",
        lazy="joined",
        cascade="all, delete-orphan",
        join_depth=100
    )
    creator = relationship("User", back_populates="created_tasks")
    time_entries: Mapped[list["TimeEntry"]] = relationship(back_populates="task")
    assignees = relationship("User", back_populates="assigned_tasks", secondary="task_assignees")
    

class TimeEntry(Base):
    __tablename__ = "time_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
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