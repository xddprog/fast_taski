from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.database.models.base import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")