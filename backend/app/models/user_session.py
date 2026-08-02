from datetime import datetime
import secrets
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.database import Base
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.plan_share import PlanShare
    from app.models.project import ProjectUpdateEntry
    from app.models.saved_view import SavedView

class UserSession(Base):
    """Opaque browser identity with non-authoritative request audit metadata."""
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(
        String(24),
        unique=True,
        index=True,
        default=lambda: secrets.token_hex(6),
    )
    session_token_hash: Mapped[str | None] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=True,
    )
    ip_address: Mapped[str] = mapped_column(String, index=True)
    user_agent: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)
    last_seen_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now)
    expires_at: Mapped[datetime | None] = mapped_column(UTCDateTime(), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(UTCDateTime(), nullable=True)
    saved_views: Mapped[list["SavedView"]] = relationship(
        "SavedView",
        back_populates="created_by_session",
    )
    project_updates: Mapped[list["ProjectUpdateEntry"]] = relationship(
        "ProjectUpdateEntry",
        back_populates="created_by_session",
    )
    plan_shares: Mapped[list["PlanShare"]] = relationship(
        "PlanShare",
        back_populates="created_by_session",
    )

    def __repr__(self) -> str:
        return f"<UserSession(public_id={self.public_id}, last_seen={self.last_seen_at})>"

    @property
    def display_name(self) -> str:
        """Return a privacy-safe stable label without exposing IP or token data."""
        return f"Guest {self.public_id[-6:].upper()}"
