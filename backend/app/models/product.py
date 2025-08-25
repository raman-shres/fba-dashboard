# app/models/product.py

from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer

# ✅ use absolute import for consistency
from app.models.base import Base, TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    asin: Mapped[str] = mapped_column(String(20), primary_key=True)
    title: Mapped[str | None] = mapped_column(String(512))
    category: Mapped[str | None] = mapped_column(String(128))
    brand: Mapped[str | None] = mapped_column(String(128))
    bsr: Mapped[int | None] = mapped_column(Integer)
    buybox_price: Mapped[float | None] = mapped_column(Float)
    fba_fees: Mapped[float | None] = mapped_column(Float)
    referral_fee_pct: Mapped[float | None] = mapped_column(Float)
