"""Short-lived browser consent for a proof-bound native session."""

from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class NativeConnection(Base):
    __tablename__ = "native_connections"
    __table_args__ = (
        CheckConstraint("requested_access IN ('full', 'observe')", name="ck_native_connections_requested_access"),
    )

    request_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    code_challenge: Mapped[str] = mapped_column(String(43), nullable=False)
    verification_code: Mapped[str] = mapped_column(String(9), nullable=False)
    request_ip_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, index=True)
    approved_session_id: Mapped[int | None] = mapped_column(ForeignKey("user_sessions.id", ondelete="CASCADE"))
    consumed_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    # What the device asked for; the approving browser sees it before consenting.
    requested_access: Mapped[str] = mapped_column(String(16), nullable=False, default="full", server_default="full")
    client_label: Mapped[str | None] = mapped_column(String(80), nullable=True)
