"""Durable person availability and a serialization point for shared planning."""

from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PlanningState(Base):
    __tablename__ = "planning_state"
    __table_args__ = (CheckConstraint("id = 1 AND revision >= 0", name="ck_planning_state_singleton"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    revision: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ProfileAvailability(Base):
    __tablename__ = "profile_availability"
    __table_args__ = (CheckConstraint("version >= 1", name="ck_profile_availability_version"),)

    profile_id: Mapped[int] = mapped_column(ForeignKey("team_member_profiles.id", ondelete="CASCADE"), primary_key=True)
    calendar_id: Mapped[int | None] = mapped_column(ForeignKey("calendars.id", ondelete="RESTRICT"))
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    provenance: Mapped[str] = mapped_column(String(40), nullable=False, default="explicit")
    calendar_conflicts: Mapped[list] = mapped_column(JSON, nullable=False, default=list)


class ProfileAbsence(Base):
    __tablename__ = "profile_absences"
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="ck_profile_absence_dates"),
        CheckConstraint("version >= 1", name="ck_profile_absence_version"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("team_member_profiles.id", ondelete="CASCADE"), index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    deleted: Mapped[bool] = mapped_column(nullable=False, default=False)
    provenance: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
