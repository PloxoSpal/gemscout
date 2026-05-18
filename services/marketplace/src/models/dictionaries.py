from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Integer, String, Boolean, DateTime

from src.database import Base


class TimestampMixin:
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

class DictionaryMixin(TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    short_description: Mapped[str | None] = mapped_column(String(255), nullable=True)

class GemTypeOrm(DictionaryMixin, Base):
    __tablename__ = 'gem_types'

    image: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"GemType id={self.id}, name={self.name}"

class GemShapeOrm(DictionaryMixin, Base):
    __tablename__ = 'gem_shapes'

    def __repr__(self) -> str:
        return f"GemShape id={self.id}, name={self.name}"

class GemOriginOrm(DictionaryMixin, Base):
    __tablename__ = 'gem_origins'

    def __repr__(self) -> str:
        return f"GemOrigin id={self.id}, name={self.name}"

class GemColorOrm(DictionaryMixin, Base):
    __tablename__ = 'gem_colors'

    def __repr__(self) -> str:
        return f"GemColor id={self.id}, name={self.name}"

class GemClarityOrm(DictionaryMixin, Base):
    __tablename__ = 'gem_clarities'

    def __repr__(self) -> str:
        return f"GemClarity id={self.id}, name={self.name}"

class GemInclusionOrm(DictionaryMixin, Base):
    __tablename__ = 'gem_inclusions'

    def __repr__(self) -> str:
        return f"GemInclusion id={self.id}, name={self.name}"


class GemTreatmentOrm(DictionaryMixin, Base):
    __tablename__ = 'gem_treatments'

    def __repr__(self) -> str:
        return f"GemTreatment id={self.id}, name={self.name}"






