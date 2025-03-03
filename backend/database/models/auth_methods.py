from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.models.base import Base


class AuthMethod(Base):
    __tablename__ = "auth_methods"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    service: Mapped[str]
    external_id: Mapped[int]

    user = relationship("User", back_populates="auth_methods")
    