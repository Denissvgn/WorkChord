"""Gantt chart schemas."""
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel

from app.schemas.iteration import IterationResponse
from app.schemas.task import TaskBatchUpdateItem


class GanttAssignee(BaseModel):
    """Assignee info for Gantt task."""
    id: int
    name: str


class GanttMilestone(BaseModel):
    """Milestone info for Gantt task editing."""
    id: int
    project_id: int
    name: str
    status: str
    target_date: Optional[date] = None


class GanttTask(BaseModel):
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
    milestone: Optional[GanttMilestone] = None
    assignee: Optional[GanttAssignee] = None
    assignees: list[GanttAssignee] = []  # For composite tasks
    priority: int
    progress: float = 0.0
    effort_days: float
    calculated_effort_days: Optional[float] = None  # Effort after applying coefficients
    effort_hours: float
    version: int = 1  # Optimistic-concurrency version for batch apply from the Gantt
    is_overdue: bool = False
    is_delayed: bool = False  # start_date passed but still in PLANNED status
    tags: list[str] = []
    is_composite: bool = False
    is_optional: bool = False
    is_outside_constraints: bool = False
    children: list["GanttTask"] = []
    dependencies: list[int] = []


class SchedulingDecision(BaseModel):
    """Explanation for a scheduling decision."""
    task_id: int
    task_title: str
    decision_type: Literal["scheduled", "reordered", "delayed", "overdue"]
    reason: str
    affected_tasks: list[int] = []


class WorkloadIssue(BaseModel):
    """Workload issue for a team member."""
    member_id: int
    member_name: str
    issue: str


class ScheduleResult(BaseModel):
    """Result of scheduling operation."""
    success: bool
    decisions: list[SchedulingDecision] = []
    workload_balanced: bool = True
    workload_issues: list[WorkloadIssue] = []


class GanttResponse(BaseModel):
    """Full Gantt chart response."""
    iteration: IterationResponse
    tasks: list[GanttTask]
    overdue_task_ids: list[int] = []
    holidays: list[date] = []
    weekends: list[date] = []
    member_vacations: dict[int, list[date]] = {}  # member_id -> vacation dates
    schedule_result: Optional[ScheduleResult] = None


class SchedulePreviewRequest(BaseModel):
    """Sandbox edits to dry-run through the real scheduler.

    ``changes`` uses the same item shape as the batch-update endpoint so a
    preview exercises exactly the payload a later apply would send.
    """
    changes: list[TaskBatchUpdateItem] = []


class SchedulePreviewResponse(BaseModel):
    """Projected Gantt state after applying changes and rescheduling.

    Produced by the real scheduler inside a rolled-back transaction; nothing
    is persisted.
    """
    tasks: list[GanttTask]
    overdue_task_ids: list[int] = []
    schedule_result: Optional[ScheduleResult] = None


# Enable forward references
GanttTask.model_rebuild()
