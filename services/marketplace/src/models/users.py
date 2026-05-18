from datetime import date
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Date, Boolean, DateTime
from sqlalchemy import func

from src.database import Base


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

    certificates: Mapped[list["CertificateOrm"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    levels: Mapped["UserLevelOrm"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    restrictions: Mapped["UserRestrictionOrm"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    complaints_sent: Mapped[list["UserComplaintOrm"]] = relationship(
        foreign_keys="UserComplaintOrm.complainant_id",
        back_populates="complainant",
    )

    complaints_received: Mapped[list["UserComplaintOrm"]] = relationship(
        foreign_keys="UserComplaintOrm.defendant_id",
        back_populates="defendant",
    )

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

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )

    def __repr__(self):
        return f"User id={self.id}, email={self.email}"

class UserLevelOrm(Base):

    __tablename__ = "user_levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))

    user: Mapped["UserOrm"] = relationship(
        back_populates="levels",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"UserLevel id={self.id}, user_id={self.user_id}"

class UserRestrictionOrm(Base):

    __tablename__ = "user_restrictions"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))

    no_private_message: Mapped[bool] = mapped_column(Boolean(), default=False)
    no_reply_to_requests : Mapped[bool] = mapped_column(Boolean(), default=False)
    no_create_requests : Mapped[bool] = mapped_column(Boolean(), default=False)
    max_3_messages_per_day : Mapped[bool] = mapped_column(Boolean(), default=False)
    max_1_message_per_day : Mapped[bool] = mapped_column(Boolean(), default=False)

    is_blocked : Mapped[bool] = mapped_column(Boolean(), default=False)

    user: Mapped["UserOrm"] = relationship(
        back_populates="restrictions",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"UserRestriction id={self.id}, user_id={self.user_id}"

class UserComplaintOrm(Base):

    __tablename__ = "user_complaints"

    id: Mapped[int] = mapped_column(primary_key=True)

    complainant_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))
    defendant_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))

    complainant: Mapped["UserOrm"] = relationship(
        foreign_keys=[complainant_id],
        back_populates="complaints_sent",
    )

    defendant: Mapped["UserOrm"] = relationship(
        foreign_keys=[defendant_id],
        back_populates="complaints_received",
    )





