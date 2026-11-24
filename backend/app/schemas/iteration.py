"""Iteration schemas."""

from app.schemas.planning_inputs import PlanningInputRevisions, WorkingZone

from app.schemas.work_metrics import WorkMetricSummary
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class IterationCreate(BaseModel):
    """Schema for creating an iteration."""
    name: str = Field(..., min_length=1, max_length=255)
    calendar_id: Optional[int] = None
    additional_calendar_ids: list[int] = Field(default_factory=list, max_length=100)
    project_id: Optional[int] = None
    start_date: date
    end_date: date
    manager_email: Optional[str] = Field(default=None, max_length=255)


class IterationUpdate(PlanningInputRevisions):
    """Schema for updating an iteration."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    calendar_id: Optional[int] = None
    additional_calendar_ids: list[int] | None = Field(default=None, max_length=100)
    project_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    manager_email: Optional[str] = Field(default=None, max_length=255)


class IterationSeriesStop(BaseModel):
    """Stop rule for generating a back-to-back iteration series."""
    mode: Literal["count", "until_date"]
    count: Optional[int] = Field(default=None, ge=1, le=100)
    until_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_stop_rule(self) -> "IterationSeriesStop":
        """Ensure the stop rule carries the field required by its mode."""
        if self.mode == "count" and self.count is None:
            raise ValueError("count is required when mode is 'count'")
        if self.mode == "until_date" and self.until_date is None:
            raise ValueError("until_date is required when mode is 'until_date'")
        return self


class IterationSeriesCreate(BaseModel):
    """Schema for creating multiple back-to-back iterations."""
    base_name: str = Field(..., min_length=1, max_length=255)
    calendar_id: Optional[int] = None
    additional_calendar_ids: list[int] = Field(default_factory=list, max_length=100)
    project_id: Optional[int] = None
    start_date: date
    duration_days: int = Field(default=14, ge=1, le=366)
    stop: IterationSeriesStop
    manager_email: Optional[str] = Field(default=None, max_length=255)


class IterationProjectSummary(BaseModel):
    """Compact project identity embedded in iteration responses."""
    id: int
    name: str
    status: str
    health: str

    class Config:
        from_attributes = True


class IterationResponse(BaseModel):
    nominal_day_hours: float = 8
    """Schema for iteration response."""
    revision: int = 1

    id: int
    name: str
    calendar_id: int
    additional_calendar_ids: list[int] = Field(default_factory=list)
    missing_calendar_years: list[int] = Field(default_factory=list)
    project_id: Optional[int] = None
    project: Optional[IterationProjectSummary] = None
    start_date: date
    end_date: date
    manager_email: Optional[str] = None
    working_days: int = 0  # Computed field

    class Config:
        from_attributes = True


class IterationSeriesResponse(BaseModel):
    """Response returned after creating an iteration series."""
    iterations: list[IterationResponse]


class IterationSummary(WorkMetricSummary):
    """Summary statistics for an iteration."""
    missing_calendar_years: list[int] = Field(default_factory=list)
    id: int
    name: str
    project_id: Optional[int] = None
    project: Optional[IterationProjectSummary] = None
    start_date: date
    end_date: date
    working_days: int
    total_tasks: int
    completed_tasks: int
    total_effort_days: float
    team_capacity_days: float
    overdue_tasks_count: int
    # What "are we on track for the end date?" needs, from the same leaf aggregate.
    status_counts: dict[str, int] = Field(default_factory=dict)
    blocked_tasks: int = 0
    remaining_effort_days: float = 0.0
    scheduled_finish: Optional[date] = None
    remaining_working_days: Optional[int] = None


class PlanCheckpoint(BaseModel):
    """One of the six plan checkpoints, in the order people and the PM work them."""
    id: Literal["iteration", "team", "work", "blockers", "schedule", "review"]
    state: Literal["done", "warn", "todo", "blocked"]
    reason_codes: list[str] = Field(default_factory=list)
    counts: dict[str, int] = Field(default_factory=dict)


class InvertedDependency(BaseModel):
    """A saved dependency whose dates start the dependent on or before its prerequisite's last day."""
    task_id: int
    task_title: str
    task_start_date: date
    prerequisite_id: int
    prerequisite_title: str
    prerequisite_end_date: date


class IterationPlanningReadinessSummary(BaseModel):
    """Compact planning inputs used by persistent navigation."""
    iteration_id: int
    calendar_name: str | None = None
    additional_calendar_ids: list[int] = Field(default_factory=list)
    missing_calendar_years: list[int] = Field(default_factory=list)
    team_member_count: int
    # Capacity rows whose profile is an agent; the rest are people (decision: agents count as capacity).
    team_agent_count: int = 0
    team_capacity_hours: float
    # Effort of the iteration's planning leaves, and the part assigned to a capacity row.
    planned_hours: float = 0.0
    assigned_hours: float = 0.0
    team_members_no_capacity: int
    task_count: int
    tasks_without_assignee: int
    tasks_without_effort: int
    # Planned leaves an agent is working on that have no capacity row.
    tasks_agent_without_capacity: int = 0
    has_schedule: bool
    risk_count: int
    # Saved dependency pairs placed out of order; a schedule preview shows the corrected dates.
    inverted_dependencies: list[InvertedDependency] = Field(default_factory=list)
    checkpoints: list[PlanCheckpoint] = Field(default_factory=list)
    checkpoints_done: int = 0
    checkpoints_total: int = 6


class IterationPage(BaseModel):
    items: list[IterationResponse]
    has_more: bool
    next_after_id: int | None
    upper_id: int
    consistency: str = "live_bounded_id_order"


class IterationDateMoveRequest(PlanningInputRevisions):
    """A proposed iteration start, end and calendar to check against shared capacity."""

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    calendar_id: Optional[int] = None
    additional_calendar_ids: list[int] | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_proposal(self) -> "IterationDateMoveRequest":
        proposed = self.model_fields_set & {"start_date", "end_date", "calendar_id", "additional_calendar_ids"}
        if not proposed:
            raise ValueError("Propose a start date, an end date or a calendar")
        for name in sorted(proposed):
            if getattr(self, name) is None:
                raise ValueError(f"{name} cannot be null; leave it out to keep the current value")
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date must be before or equal to end_date")
        return self

    def as_update(self) -> IterationUpdate:
        """The iteration update that applies this proposal."""
        return IterationUpdate(**self.model_dump(exclude_unset=True))


class IterationPeriod(BaseModel):
    """An iteration's dates and annual calendars."""

    start_date: date
    end_date: date
    calendar_id: int
    additional_calendar_ids: list[int] = Field(default_factory=list)
    working_days: int
    missing_calendar_years: list[int] = Field(default_factory=list)


class DateMoveBooking(BaseModel):
    """Hours one other iteration books from the same person on one date."""

    iteration_id: int
    project_id: Optional[int] = None
    hours: float


class DateMoveShortfall(BaseModel):
    """One person and date where the proposed period requests more than the person has."""

    profile_id: int
    member_ids: list[int]
    date: date
    available_hours: float
    requested_hours: float
    booked_elsewhere_hours: float
    # Hours booked in iterations the caller cannot read, without naming them.
    private_booked_hours: float = 0.0
    bookings: list[DateMoveBooking] = Field(default_factory=list)
    overallocated_hours: float
    shortfall_hours: float
    current_overallocated_hours: Optional[float] = None


class DateMoveProfile(BaseModel):
    """How the proposed period fits one person of the iteration team."""

    profile_id: int
    member_ids: list[int]
    shortfall_days: int
    shortfall_hours: float
    first_shortfall_date: Optional[date] = None
    calendar_uncertain: bool = False
    missing_calendar_years: list[int] = Field(default_factory=list)


class IterationDateMovePreview(BaseModel):
    """Shared capacity for a proposed iteration period. Nothing is saved."""

    applied: bool = False
    iteration_id: int
    current: IterationPeriod
    proposed: IterationPeriod
    profiles: list[DateMoveProfile]
    shortfalls: list[DateMoveShortfall]
    shortfalls_truncated: bool = False
    max_shortfalls: int
    unlinked_member_ids: list[int] = Field(default_factory=list)
    expected_revisions: dict[int, int]
    planning_revision: Optional[int] = None
    apply_with: str = (
        "Update the iteration with the same start_date, end_date and calendar fields and these "
        "expected_revisions; a changed iteration is refused. Bookings in other iterations are not "
        "fenced by that update: preview again if planning_revision has changed."
    )
    formula: str = (
        "requested = this iteration's capacity rows: person calendar hours after absence × the row's percentage "
        "on that date; booked elsewhere = the same for every other row of the person; "
        "overallocated = requested + booked elsewhere − available; shortfall = min(requested, overallocated)"
    )
