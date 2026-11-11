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
    project_id: Optional[int] = None
    start_date: date
    end_date: date
    manager_email: Optional[str] = Field(default=None, max_length=255)


class IterationUpdate(PlanningInputRevisions):
    """Schema for updating an iteration."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    calendar_id: Optional[int] = None
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


class IterationPlanningReadinessSummary(BaseModel):
    """Compact planning inputs used by persistent navigation."""
    iteration_id: int
    team_member_count: int
    # Capacity rows whose profile is an agent; the rest are people (decision: agents count as capacity).
    team_agent_count: int = 0
    team_capacity_hours: float
    team_members_no_capacity: int
    task_count: int
    tasks_without_assignee: int
    tasks_without_effort: int
    # Planned leaves an agent is working on that have no capacity row.
    tasks_agent_without_capacity: int = 0
    has_schedule: bool
    risk_count: int
    checkpoints: list[PlanCheckpoint] = Field(default_factory=list)
    checkpoints_done: int = 0
    checkpoints_total: int = 6


class IterationPage(BaseModel):
    items: list[IterationResponse]
    has_more: bool
    next_after_id: int | None
    upper_id: int
    consistency: str = "live_bounded_id_order"
