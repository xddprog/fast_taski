from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.database.models.base import Base


class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True)

    teams = relationship("UserTeam", back_populates="user")    
    created_teams = relationship("Team", back_populates="owner")
    auth_methods = relationship("AuthMethod", back_populates="user")
    created_tasks = relationship("Task", back_populates="creator", cascade="all, delete-orphan")
    assigned_tasks = relationship("Task", secondary="task_assignees", back_populates="assignees")
    time_entries = relationship("TimeEntry", back_populates="user")
    created_notes = relationship("Note", back_populates="creator")
    notes = relationship("Note", secondary="user_notes", back_populates="members", uselist=True)
    comments = relationship("Comment", back_populates="user")
