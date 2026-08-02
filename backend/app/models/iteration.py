"""Iteration model."""
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.calendar import Calendar
    from app.models.plan_share import PlanShare
    from app.models.project import Project
    from app.models.team_member import TeamMember
    from app.models.task import Task


class Iteration(Base):
    """Development iteration (sprint) model."""
    __tablename__ = "iterations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Manager email for notifications (optional)
    manager_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Foreign keys
    calendar_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("calendars.id"), nullable=False
    )
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="SET NULL", use_alter=True),
        nullable=True,
        index=True,
    )

    # Relationships
    calendar: Mapped["Calendar"] = relationship("Calendar", back_populates="iterations")
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="iterations")
    team_members: Mapped[list["TeamMember"]] = relationship(
        "TeamMember", back_populates="iteration"  # No cascade delete - keep team members for reuse
    )
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="iteration", cascade="all, delete-orphan"
    )
    plan_shares: Mapped[list["PlanShare"]] = relationship(
        "PlanShare",
        back_populates="iteration",
        cascade="all, delete-orphan",
    )
