from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.database.models.base import Base


class Tag(Base):
    __tablename__ = "tags"

    name: Mapped[str]
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    
    tasks = relationship("Task", back_populates="tags", secondary="task_tags")
    team = relationship("Team", back_populates="tags")


class TaskTag(Base):
    __tablename__ = "task_tags"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False)