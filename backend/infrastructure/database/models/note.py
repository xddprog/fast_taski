from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.database.models.base import Base


class Note(Base):
    __tablename__ = "notes"

    name: Mapped[str]
    text: Mapped[str]
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    team = relationship("Team", back_populates="notes")
    creator = relationship("User", back_populates="created_notes")
    members = relationship("User", back_populates="notes", secondary="user_notes")


class UserNote(Base):
    __tablename__ = "user_notes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), nullable=False)