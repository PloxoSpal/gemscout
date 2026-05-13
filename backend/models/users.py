from datetime import date
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date, DateTime
from sqlalchemy import func

from backend.database import Base


class UserOrm(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    hash_password: Mapped[str] = mapped_column(String(255))

    date_of_birth: Mapped[date] = mapped_column(Date())
    country: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    organization: Mapped[str] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(String(255), unique=True)
    experience_years: Mapped[int] = mapped_column(Integer())

    profile_image: Mapped[str | None] = mapped_column(String())
    passport_photo: Mapped[str | None] = mapped_column(String())

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

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"User id={self.id}, email={self.email}"





