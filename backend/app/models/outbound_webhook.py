"""Outbound webhook configuration and delivery log models."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

class OutboundWebhookDeliveryStatus(str, Enum):
    """Delivery states for outbound webhook attempts."""

    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"


class OutboundDeliveryChannel(str, Enum):
    """Transport selected by the durable outbound delivery worker."""

    WEBHOOK = "webhook"
    EMAIL = "email"


class OutboundWebhookTarget(Base):
    """Configurable subscriber for outbound domain events."""

    __tablename__ = "outbound_webhook_targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    enabled: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
    subscribed_events_json: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    secret: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    headers_json: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
        index=True,
    )

    deliveries: Mapped[list["OutboundWebhookDelivery"]] = relationship(
        "OutboundWebhookDelivery",
        back_populates="target",
        passive_deletes=True,
        order_by="OutboundWebhookDelivery.created_at.desc(), OutboundWebhookDelivery.id.desc()",
    )


class OutboundWebhookEvent(Base):
    """Normalized domain event available for webhook delivery."""

    __tablename__ = "outbound_webhook_events"
    __table_args__ = (
        UniqueConstraint("event_id", name="uq_outbound_webhook_events_event_id"),
        Index("ix_outbound_webhook_events_type_time", "event_type", "occurred_at"),
        Index("ix_outbound_webhook_events_entity", "entity_type", "entity_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    payload_json: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        nullable=False,
        index=True,
    )

    deliveries: Mapped[list["OutboundWebhookDelivery"]] = relationship(
        "OutboundWebhookDelivery",
        back_populates="event",
        cascade="all, delete-orphan",
        order_by="OutboundWebhookDelivery.created_at.desc(), OutboundWebhookDelivery.id.desc()",
    )


class OutboundWebhookDelivery(Base):
    """One delivery attempt log for one target and event."""

    __tablename__ = "outbound_webhook_deliveries"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'delivered', 'failed')",
            name="ck_outbound_webhook_deliveries_status",
        ),
        CheckConstraint(
            "channel IN ('webhook', 'email')",
            name="ck_outbound_webhook_deliveries_channel",
        ),
        Index("ix_outbound_webhook_deliveries_target_status", "target_id", "status"),
        Index(
            "ix_outbound_webhook_deliveries_due",
            "status",
            "next_retry_at",
            "lease_expires_at",
        ),
        Index("ix_outbound_webhook_deliveries_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("outbound_webhook_targets.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("outbound_webhook_events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    channel: Mapped[str] = mapped_column(
        String(30),
        default=OutboundDeliveryChannel.WEBHOOK.value,
        nullable=False,
        index=True,
    )
    payload_json: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default=OutboundWebhookDeliveryStatus.PENDING.value,
        nullable=False,
        index=True,
    )
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    last_http_status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_response_body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_attempt_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    next_retry_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    lease_token: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    lease_expires_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    terminal_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
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

    target: Mapped[Optional[OutboundWebhookTarget]] = relationship(
        "OutboundWebhookTarget",
        back_populates="deliveries",
    )
    event: Mapped[OutboundWebhookEvent] = relationship(
        "OutboundWebhookEvent",
        back_populates="deliveries",
    )
