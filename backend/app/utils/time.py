"""Timezone-safe UTC helpers and SQLAlchemy datetime normalization."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import TypeDecorator


def utc_now() -> datetime:
    """Return the current time as an aware UTC datetime."""
    return datetime.now(UTC)


def as_utc(value: datetime) -> datetime:
    """Normalize an aware or legacy-naive UTC datetime to aware UTC.

    Historical SQLite rows contain naive values even when the model declared a
    timezone-aware column. Those values represent UTC by project convention;
    attaching UTC is therefore the compatibility-safe normalization.
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


class UTCDateTime(TypeDecorator[datetime]):
    """Persist UTC datetimes and always return aware UTC values.

    SQLite drops timezone offsets from its datetime representation, so values
    are stored there as naive UTC and normalized on read. Dialects with native
    timezone support receive aware UTC values and a timezone-aware column type.
    """

    impl = DateTime
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> Any:
        return dialect.type_descriptor(DateTime(timezone=True))

    def process_bind_param(
        self,
        value: datetime | None,
        dialect: Dialect,
    ) -> datetime | None:
        if value is None:
            return None
        normalized = as_utc(value)
        if dialect.name == "sqlite":
            return normalized.replace(tzinfo=None)
        return normalized

    def process_result_value(
        self,
        value: datetime | None,
        _dialect: Dialect,
    ) -> datetime | None:
        return as_utc(value) if value is not None else None
