from ctypes import ARRAY
from sqlalchemy import ARRAY, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.database.models.base import Base


class Note(Base):
    __tablename__ = "notes"

    title: Mapped[str]
    text: Mapped[str]
    files: Mapped[list[str]] = mapped_column("files", ARRAY(String), nullable=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    team = relationship("Team", back_populates="notes")
    creator = relationship("User", back_populates="created_notes", lazy="selectin")
    members = relationship(
        "User",
        secondary="user_notes",
        back_populates="notes",
        uselist=True,
    )


class UserNote(Base):
    __tablename__ = "user_notes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), primary_key=True)