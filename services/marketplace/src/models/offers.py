from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Boolean, DateTime, Float
from sqlalchemy import Enum as SAEnum
from sqlalchemy import func

from src.database import Base
from src.models.enums import QuantityType, OfferType

class OfferOrm(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    request_id: Mapped[int] = mapped_column(Integer, ForeignKey('requests.id'))

    # BUY, если заявку от покупателя к продавцу, SELL если продавец отвечает на запрос
    request_type: Mapped[OfferType] = mapped_column(SAEnum(OfferType), nullable=False)

    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_types.id'))
    shape_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_shapes.id'))
    color_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_colors.id'))
    origin_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_origins.id'))

    quantity: Mapped[QuantityType] = mapped_column(SAEnum(QuantityType), nullable=False)

    weight: Mapped[int] = mapped_column(Integer)
    dimension: Mapped[int] = mapped_column(Integer)

    clarity_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_clarities.id'))
    inclusion_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_inclusions.id'))
    treatment_id: Mapped[int] = mapped_column(Integer, ForeignKey('gem_treatments.id'))

    price: Mapped[float] = mapped_column(Float())
    price_total: Mapped[float] = mapped_column(Float())

    gem_location: Mapped[str] = mapped_column(String(255))

    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    request: Mapped["RequestOrm"] = relationship(
        back_populates="offers"
    )

    images: Mapped[list["OfferImageOrm"]] = relationship(
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

class OfferImageOrm(Base):
    __tablename__ = 'offer_images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    offer_id: Mapped[int] = mapped_column(Integer, ForeignKey('offers.id', ondelete="CASCADE"))

    image_url: Mapped[str] = mapped_column(String(500))

    request: Mapped[OfferOrm] = relationship(
        back_populates="images",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        return f"RequestImage id={self.id}, request_id={self.request_id}, file_url={self.image_url}"
