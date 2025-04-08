from uuid import uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.database.models.base import Base
from backend.utils.enums import TeamRoles


class Team(Base):
    __tablename__ = "teams"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    invite_code: Mapped[str] = mapped_column(default=uuid4())
    
    members: Mapped[list['UserTeam']] = relationship(
        back_populates="team", 
        uselist=True, 
        cascade="all, delete-orphan"
    )
    owner = relationship("User", back_populates="created_teams")
    columns = relationship("Column",back_populates="team", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="team", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="team", cascade="all, delete-orphan")
    

class UserTeam(Base):
    __tablename__ = "user_teams"

    role: Mapped[str] = mapped_column(default=TeamRoles.MEMBER)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    team: Mapped['Team'] = relationship(back_populates="members")
    user = relationship("User", back_populates="teams")
