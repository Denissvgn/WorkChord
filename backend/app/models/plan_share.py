"""Immutable read-only plan snapshots shared through revocable links."""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Index, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.iteration import Iteration
    from app.models.user_session import UserSession


class PlanShare(Base):
    """One immutable iteration plan snapshot owned by a browser session."""

    __tablename__ = "plan_shares"
    __table_args__ = (
        Index(
            "ix_plan_shares_iteration_owner_created",
            "iteration_id",
            "created_by_session_id",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_id: Mapped[str] = mapped_column(
        String(48),
        unique=True,
        index=True,
        nullable=False,
    )
    iteration_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("iterations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    created_by_session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user_sessions.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    snapshot_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        index=True,
        nullable=False,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        UTCDateTime(),
        index=True,
        nullable=True,
    )

    iteration: Mapped["Iteration"] = relationship(
        "Iteration",
        back_populates="plan_shares",
    )
    created_by_session: Mapped["UserSession"] = relationship(
        "UserSession",
        back_populates="plan_shares",
    )
