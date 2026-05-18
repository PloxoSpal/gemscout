from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Enum as SAEnum
from sqlalchemy import Integer, String, Boolean, DateTime

from src.database import Base


class Role(Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(80), unique=True)

    hash_password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[Role] = mapped_column(SAEnum(Role), nullable=False, default=Role.USER)

    is_2fa_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    totp_secret: Mapped[str | None] = mapped_column(String(255))

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        return f"User id={self.id}, email={self.email}, phone={self.phone}, role={self.role}"