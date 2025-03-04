from unittest.mock import Base
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    
    auth_methods = relationship("AuthMethod", back_populates="user", cascade="all, delete-orphan")
