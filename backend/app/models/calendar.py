"""Calendar model."""
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.iteration import Iteration


class Calendar(Base):
    """Production calendar model.

    Stores holidays and weekend days configuration for a year.
    """
    __tablename__ = "calendars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
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
