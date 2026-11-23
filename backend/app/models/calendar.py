"""Calendar model."""
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.iteration import Iteration


iteration_annual_calendars = Table(
    "iteration_annual_calendars", Base.metadata,
    Column("iteration_id", ForeignKey("iterations.id", ondelete="CASCADE"), primary_key=True),
    Column("calendar_id", ForeignKey("calendars.id", ondelete="RESTRICT"), primary_key=True, index=True),
)

profile_annual_calendars = Table(
    "profile_annual_calendars", Base.metadata,
    Column("profile_id", ForeignKey("profile_availability.profile_id", ondelete="CASCADE"), primary_key=True),
    Column("calendar_id", ForeignKey("calendars.id", ondelete="RESTRICT"), primary_key=True, index=True),
)


class Calendar(Base):
    """Production calendar model.

    Stores holidays and weekend days configuration for a year.
    """
    __tablename__ = "calendars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", server_default="UTC", nullable=False)
    nominal_day_hours: Mapped[float] = mapped_column(Float, default=8.0, server_default="8", nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    # List of holiday dates as ISO strings ["2025-01-01", "2025-01-02", ...]
    holidays: Mapped[list[str]] = mapped_column(JSON, default=list)

    # Weekend days: 0=Mon, 1=Tue, ..., 5=Sat, 6=Sun. Default: [5, 6] (Sat, Sun)
    weekend_days: Mapped[list[int]] = mapped_column(JSON, default=[5, 6])

    # Pre-holiday shortened days (working time reduced by 1 hour)
    short_days: Mapped[list[str]] = mapped_column(JSON, default=list)

    # Relationships
    iterations: Mapped[list["Iteration"]] = relationship(
        "Iteration", back_populates="calendar", cascade="all, delete-orphan"
    )

    def get_holidays_as_dates(self) -> list[date]:
        """Convert holiday strings to date objects."""
        return [date.fromisoformat(d) for d in self.holidays]
