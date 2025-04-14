from ctypes import ARRAY
from sqlalchemy import ARRAY, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.config.aws_config import AWS_STORAGE_CONFIG
from backend.infrastructure.database.models.base import Base


class Note(Base):
    __tablename__ = "notes"

    title: Mapped[str]
    text: Mapped[str]
    _files: Mapped[list[str]] = mapped_column("files", ARRAY(String), nullable=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    team = relationship("Team", back_populates="notes")
    creator = relationship("User", back_populates="created_notes", lazy="selectin")
    members = relationship("User", back_populates="notes", secondary="user_notes", lazy="selectin")

    @hybrid_property
    def files(self):
        return [
            f"{AWS_STORAGE_CONFIG.AWS_ENDPOINT_URL}/{AWS_STORAGE_CONFIG.AWS_BUCKET_NAME}/{file}" 
            for file in self._files
        ]
    

class UserNote(Base):
    __tablename__ = "user_notes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), nullable=False)

    user = relationship("User", back_populates="notes")
    note = relationship("Note", back_populates="members")