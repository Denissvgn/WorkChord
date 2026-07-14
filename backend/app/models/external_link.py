"""External link model for delivery traceability."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import CheckConstraint, Index, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class ExternalLinkEntityType(str, Enum):
    """Supported internal entity types for external links."""
    TASK = "task"
    PROJECT = "project"
    RELEASE = "release"


class ExternalLinkProvider(str, Enum):
    """Supported external link providers."""
    GITHUB = "github"
    GITLAB = "gitlab"
    FIGMA = "figma"
    SENTRY = "sentry"
    CUSTOM = "custom"


class ExternalLink(Base):
    """Generic link from an internal entity to an external delivery artifact."""
    __tablename__ = "external_links"
    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('task', 'project', 'release')",
            name="ck_external_links_entity_type",
        ),
        CheckConstraint(
            "provider IN ('github', 'gitlab', 'figma', 'sentry', 'custom')",
            name="ck_external_links_provider",
        ),
        Index("ix_external_links_entity", "entity_type", "entity_id"),
        Index("ix_external_links_provider_key", "provider", "external_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    external_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True, index=True)
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
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
        index=True,
    )
