from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.config.aws_config import AWS_STORAGE_CONFIG
from backend.infrastructure.database.models.base import Base
from backend.infrastructure.database.models.auth_methods import AuthMethod
from backend.infrastructure.database.models.team import UserTeam, Team
from backend.infrastructure.database.models.note import UserNote, Note
from backend.infrastructure.database.models.task import Task, TasksAssignees


class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    _avatar: Mapped[str] = mapped_column("avatar", nullable=True)

    teams = relationship("UserTeam", back_populates="user")    
    created_teams = relationship("Team", back_populates="owner")
    auth_methods = relationship("AuthMethod", back_populates="user")
    created_tasks = relationship("Task", back_populates="creator", cascade="all, delete-orphan")
    assigned_tasks = relationship("Task", secondary="task_assignees", back_populates="assignees")
    time_entries = relationship("TimeEntry", back_populates="user")
    created_notes = relationship("Note", back_populates="creator")
    notes = relationship("Note", back_populates="members", secondary="user_notes")
    comments = relationship("Comment", back_populates="user")

    @hybrid_property
    def avatar(self):
        return f"{AWS_STORAGE_CONFIG.AWS_ENDPOINT_URL}/{AWS_STORAGE_CONFIG.AWS_BUCKET_NAME}/{self._avatar}"