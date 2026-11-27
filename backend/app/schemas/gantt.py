"""Gantt chart schemas."""

from app.schemas.work_metrics import TaskMetricSignals
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.iteration import InvertedDependency, IterationResponse
from app.schemas.task import TaskBatchUpdateItem


class GanttAssignee(BaseModel):
    """Assignee info for Gantt task."""
    id: int
    name: str
    kind: Optional[Literal["human", "agent", "hybrid"]] = Field(
        default=None,
        description="Kind of the assignee's profile. Read-only; null when it is not known.",
    )


class GanttMilestone(BaseModel):
    """Milestone info for Gantt task editing."""
    id: int
    project_id: int
    name: str
    status: str
    target_date: Optional[date] = None


class GanttTask(TaskMetricSignals):
    """Task representation for Gantt chart."""
    id: int
    title: str
    project_id: Optional[int] = None
    milestone_id: Optional[int] = None
    start_date: Optional[date]
    end_date: Optional[date]
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    min_start_date: Optional[date] = None
    max_end_date: Optional[date] = None
    status: Optional[str] = None  # planned, active, resolved, closed
    # The stored status, or canceled / superseded for withdrawn work, which keeps the status it had.
    displayed_state: Optional[str] = None
    milestone: Optional[GanttMilestone] = None
    assignee: Optional[GanttAssignee] = None
    assignees: list[GanttAssignee] = []  # For composite tasks
    priority: int
    progress: float = 0.0
    effort_days: Optional[float]
    calculated_effort_days: Optional[float] = None  # Effort after applying coefficients
    effort_hours: Optional[float]
    version: int = 1  # Optimistic-concurrency version for batch apply from the Gantt
    is_overdue: bool = False
    is_delayed: bool = False  # start_date passed but still in PLANNED status
    tags: list[str] = []
    is_composite: bool = False
    is_optional: bool = False
    is_outside_constraints: bool = False
    # True when this task's saved start is on or before a prerequisite's saved end.
    has_inverted_dependency: bool = False
    children: list["GanttTask"] = []
    dependencies: list[int] = []


class SchedulingDecision(BaseModel):
    """Explanation for a scheduling decision."""
    task_id: int
    task_title: str
    decision_type: Literal["scheduled", "reordered", "delayed", "overdue", "unavailable"]
    reason: str
    affected_tasks: list[int] = []


UnscheduledReason = Literal[
    "no_assignee",
    "assignee_not_in_iteration",
    "no_estimate",
    "no_capacity",
    "prerequisites_pending",
    "predecessor_unscheduled",
    "predecessor_postponed",
    "deferred",
    "blocked",
    "not_placed",
]


DateRule = Literal[
    "dates_incomplete",
    "dates_inverted",
    "outside_iteration",
    "before_min_start_date",
]


class WaitingOnTask(BaseModel):
    """A task a planned task waits on: postponed work, or the prerequisite behind idle days."""
    task_id: int
    task_title: str


def _no_waits(tasks: list[WaitingOnTask]) -> bool:
    return not tasks


class UnscheduledTask(BaseModel):
    """A planned task the scheduler left without dates, and what would change that."""
    task_id: int
    task_title: str
    reason: UnscheduledReason
    message: str
    # The task held dates before this run and the run removed them.
    dates_cleared: bool = False
    # The rule the removed dates broke (only a half-dated task loses its dates); None otherwise.
    date_rule: DateRule | None = Field(default=None, exclude_if=lambda rule: rule is None)
    # Causes of its own that keep it undated once the main reason is resolved.
    also: list[UnscheduledReason] = []
    # The postponed work it waits on (reason predecessor_postponed); omitted otherwise.
    waiting_on: list[WaitingOnTask] = Field(default_factory=list, exclude_if=_no_waits)


class KeptDatesTask(BaseModel):
    """A planned task the scheduler could not place; it keeps the dates it already had."""
    task_id: int
    task_title: str
    reason: UnscheduledReason
    message: str
    start_date: date
    end_date: date
    # The rule the kept dates break, when they break one; the task still has these dates.
    date_rule: DateRule | None = Field(default=None, exclude_if=lambda rule: rule is None)
    # Causes of its own that stop the scheduler from placing it once the main reason is resolved.
    also: list[UnscheduledReason] = []
    # The postponed work it waits on (reason predecessor_postponed); omitted otherwise.
    waiting_on: list[WaitingOnTask] = Field(default_factory=list, exclude_if=_no_waits)


IdleReason = Literal[
    "waits_for_prerequisite",
    "earliest_start",
    "fixed_dates",
    "uninterrupted_slot",
]


class IdleGap(BaseModel):
    """Working days an assignee is left idle before the task that follows them on the row."""
    start_date: date
    end_date: date
    working_days: int
    # The task that starts after these days and the reason it starts no earlier.
    task_id: int
    task_title: str
    reason: IdleReason
    # The prerequisite it waits for (reason waits_for_prerequisite); omitted otherwise.
    waiting_on: WaitingOnTask | None = Field(default=None, exclude_if=lambda value: value is None)
    # The earliest start date that holds it (reason earliest_start); omitted otherwise.
    earliest_start: date | None = Field(default=None, exclude_if=lambda value: value is None)
    message: str


class AssigneeIdleDays(BaseModel):
    """An assignee's working days left idle inside the scheduled span, before the row's last work."""
    member_id: int
    member_name: str
    idle_working_days: int
    gaps: list[IdleGap]


class WorkloadIssue(BaseModel):
    """Workload issue for a team member."""
    member_id: int
    member_name: str
    issue: str


class AssignmentSelectionRefresh(BaseModel):
    task_id: int
    assignment_id: int
    actor_id: int
    from_task_version: int
    to_task_version: int
    action: Literal["refresh_model_selection"]


class ScheduleResult(BaseModel):
    """Result of scheduling operation."""
    success: bool
    planning_revision: int | None = None
    capacity_issues: list[dict] = []
    assignment_refreshes: list[AssignmentSelectionRefresh] = Field(default_factory=list, exclude_if=lambda rows: not rows)
    decisions: list[SchedulingDecision] = []
    workload_balanced: bool = True
    workload_issues: list[WorkloadIssue] = []
    # Planned leaf tasks still without dates after this run, each with its cause.
    unscheduled: list[UnscheduledTask] = []
    # Planned leaf tasks the run could not place that keep the dates they already had.
    kept_dates: list[KeptDatesTask] = Field(default_factory=list, exclude_if=lambda rows: not rows)
    # Each assignee's remaining idle working days before its last work, with the task that follows them.
    idle_days: list[AssigneeIdleDays] = Field(default_factory=list, exclude_if=lambda rows: not rows)


class GanttResponse(BaseModel):
    """Full Gantt chart response."""
    iteration: IterationResponse
    tasks: list[GanttTask]
    overdue_task_ids: list[int] = []
    # Saved dependency pairs whose dates are inverted; correct them with a schedule preview, then apply.
    inverted_dependencies: list[InvertedDependency] = []
    holidays: list[date] = []
    weekends: list[date] = []
    member_vacations: dict[int, list[date]] = {}  # member_id -> vacation dates
    schedule_result: Optional[ScheduleResult] = None


class ScheduleApplyRequest(BaseModel):
    expected_revision: Optional[int] = None
    expected_planning_revision: Optional[int] = None
    rebaseline_reason: Optional[str] = None


class SchedulePreviewRequest(BaseModel):
    """Sandbox edits to dry-run through the real scheduler.

    ``changes`` uses the same item shape as the batch-update endpoint so a
    preview exercises exactly the payload a later apply would send.
    """
    changes: list[TaskBatchUpdateItem] = []
    expected_revision: Optional[int] = None
    expected_planning_revision: Optional[int] = None


class SchedulePreviewResponse(BaseModel):
    """Projected Gantt state after applying changes and rescheduling.

    Produced by the real scheduler inside a rolled-back transaction; nothing
    is persisted.
    """
    input_revision: int
    input_planning_revision: int | None = None
    tasks: list[GanttTask]
    overdue_task_ids: list[int] = []
    schedule_result: Optional[ScheduleResult] = None


# Enable forward references
GanttTask.model_rebuild()
