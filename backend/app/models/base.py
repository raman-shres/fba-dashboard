# app/models/base.py

from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy.types import DateTime as SATimestamp


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        SATimestamp(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        SATimestamp(timezone=True), server_default=func.now(), onupdate=func.now()
    )
