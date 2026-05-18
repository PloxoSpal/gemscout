from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from sqlalchemy import ForeignKey, String, DateTime

from src.database import Base

from src.models.users import UserOrm


class CertificateOrm(Base):
    __tablename__ = 'certificates'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    file_url: Mapped[str] = mapped_column(String(500))

    user: Mapped["UserOrm"] = relationship(
        back_populates="certificates",

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

