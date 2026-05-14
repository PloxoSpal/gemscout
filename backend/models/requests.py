from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Boolean, DateTime, Float
from sqlalchemy import Enum as SAEnum
from sqlalchemy import func

from backend.database import Base
from backend.models.certificates import CertificateOrm
from backend.models.enums import QuantityType, RequestType, RequestDuration

class RequestOrm(Base):
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    request_type: Mapped[RequestType] = mapped_column(SAEnum(RequestType), nullable=False)

    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_types.id'))
    shape_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_shapes.id'))
    color_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_colors.id'))
    origin_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_origins.id'))

    quantity: Mapped[QuantityType] = mapped_column(SAEnum(QuantityType), nullable=False)

    weight_from: Mapped[int] = mapped_column(Integer)
    weight_to: Mapped[int] = mapped_column(Integer)
    dimension_from: Mapped[int] = mapped_column(Integer)
    dimension_to: Mapped[int] = mapped_column(Integer)

    clarity_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_clarities.id'))
    inclusion_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_inclusions.id'))
    inclusion_note: Mapped[str | None] = mapped_column(String(500))
    treatment_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_treatments.id'))

    price_from: Mapped[float] = mapped_column(Float())
    price_to: Mapped[float] = mapped_column(Float())
    price_total_from: Mapped[float] = mapped_column(Float())
    price_total_to: Mapped[float] = mapped_column(Float())

    additional_information: Mapped[str | None] = mapped_column(String(1000))

    gem_location: Mapped[str] = mapped_column(String(255))
    certificate: Mapped["CertificateOrm"] = mapped_column(ForeignKey(CertificateOrm.id), nullable=True)

    request_duration: Mapped[RequestDuration] = mapped_column(SAEnum(RequestDuration), nullable=False)

    is_hide_profile: Mapped[bool] = mapped_column(Boolean, default=False)

    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    offers: Mapped[list["OfferOrm"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    images: Mapped[list["RequestImageOrm"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        passive_deletes=True,
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

    def __repr__(self) -> str:
        return f"Request id={self.id}, self"


class RequestImageOrm(Base):
    __tablename__ = 'request_images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(Integer, ForeignKey('requests.id', ondelete="CASCADE"))

    image_url: Mapped[str] = mapped_column(String(500))

    request: Mapped[RequestOrm] = relationship(
        back_populates="images",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        return f"RequestImage id={self.id}, request_id={self.request_id}, file_url={self.image_url}"




