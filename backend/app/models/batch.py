# app/models/batch.py

from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, ForeignKey

# use absolute import so editor + runtime resolve it
from app.models.base import Base, TimestampMixin


class Batch(Base, TimestampMixin):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128))


class BatchItem(Base, TimestampMixin):
    __tablename__ = "batch_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id", ondelete="CASCADE"))
    asin: Mapped[str] = mapped_column(String(20))

    cost: Mapped[float | None] = mapped_column(Float)
    price: Mapped[float | None] = mapped_column(Float)
    roi: Mapped[float | None] = mapped_column(Float)
    profit_per_unit: Mapped[float | None] = mapped_column(Float)
    risk_band: Mapped[str | None] = mapped_column(String(16))
