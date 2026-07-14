"""Runtime system settings model."""
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import Boolean, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class SystemSetting(Base):
    """One catalogued runtime configuration value.

    Non-secret settings store their JSON scalar/object in ``value_json``.
    Secret settings store encrypted payloads in ``secret_ciphertext``.
    """

    __tablename__ = "system_settings"
    __table_args__ = (
        UniqueConstraint("key", name="uq_system_settings_key"),
        Index("ix_system_settings_category_key", "category", "key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    value_json: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    secret_ciphertext: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_secret: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
