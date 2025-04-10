from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.database.models.base import Base


class Column(Base):
    __tablename__ = "columns"

    name: Mapped[str] 
    color: Mapped[str]
    tasks = relationship("Task", back_populates="column")
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    
    team = relationship("Team", back_populates="columns")