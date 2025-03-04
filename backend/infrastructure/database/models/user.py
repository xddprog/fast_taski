from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.database.models.base import Base
from backend.infrastructure.database.models.auth_methods import AuthMethod


class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    
    auth_methods = relationship("AuthMethod", back_populates="user", cascade="all, delete-orphan")
