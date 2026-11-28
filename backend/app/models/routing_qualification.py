"""A deployment's declared qualification keys and their append-only revisions."""

from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

QUALIFICATION_KEY_STATES = ("active", "retired")
QUALIFICATION_KEY_ACTIONS = ("declare", "revise", "retire")


class RoutingQualificationKey(Base):
    """One deployment-declared key that catalog entries and task requirements may name.

    The key name never changes. Retiring keeps the row and its history, so a
    later declaration under the same name continues the revision sequence.
    """

    __tablename__ = "routing_qualification_keys"
    __table_args__ = (
        CheckConstraint("state IN ('active', 'retired')", name="ck_routing_qualification_keys_state"),
        CheckConstraint("revision >= 1", name="ck_routing_qualification_keys_revision"),
        CheckConstraint("length(trim(key)) > 0", name="ck_routing_qualification_keys_key_not_blank"),
        CheckConstraint("key = lower(trim(key))", name="ck_routing_qualification_keys_key_canonical"),
        CheckConstraint("length(trim(label)) > 0", name="ck_routing_qualification_keys_label_not_blank"),
        UniqueConstraint("key", name="uq_routing_qualification_keys_key"),
        Index("ix_routing_qualification_keys_state", "state"),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(120), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    state: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )
    retired_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)

    revisions: Mapped[list["RoutingQualificationKeyRevision"]] = relationship(
        "RoutingQualificationKeyRevision",
        back_populates="qualification_key",
        order_by="RoutingQualificationKeyRevision.revision",
    )


class RoutingQualificationKeyRevision(Base):
    """The state a key had after one declare, revise or retire command, and why."""

    __tablename__ = "routing_qualification_key_revisions"
    __table_args__ = (
        UniqueConstraint(
            "qualification_key_id",
            "revision",
            name="uq_routing_qualification_key_revisions_revision",
        ),
        CheckConstraint(
            "action IN ('declare', 'revise', 'retire')",
            name="ck_routing_qualification_key_revisions_action",
        ),
        CheckConstraint(
            "state IN ('active', 'retired')",
            name="ck_routing_qualification_key_revisions_state",
        ),
        CheckConstraint(
            "length(trim(reason)) > 0",
            name="ck_routing_qualification_key_revisions_reason_not_blank",
        ),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    qualification_key_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("routing_qualification_keys.id", ondelete="RESTRICT"),
        nullable=False,
    )
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    state: Mapped[str] = mapped_column(String(20), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    actor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agent_actors.id"), nullable=True
    )
    correlation_id: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)

    qualification_key: Mapped[RoutingQualificationKey] = relationship(
        RoutingQualificationKey,
        back_populates="revisions",
    )
