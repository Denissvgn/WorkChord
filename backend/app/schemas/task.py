"""Task schemas."""
from datetime import date, datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.schemas.external_link import ExternalLinkResponse
from app.schemas.team import AssigneeRecommendationResponse
from app.utils.url_policy import URLPolicyError, normalize_stored_display_url

MAX_TASK_TEXT_IMPORT_CHARS = 200_000


def _normalize_optional_url(value: Optional[str]) -> Optional[str]:
    if value is None or not str(value).strip():
        return None
    try:
        return normalize_stored_display_url(value)
    except URLPolicyError as exc:
        raise ValueError(str(exc)) from exc


class TaskStatus(str, Enum):
    """Task status enumeration for work tracking.

    Workflow: PLANNED -> ACTIVE -> RESOLVED -> CLOSED
    """
    PLANNED = "planned"
    ACTIVE = "active"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TaskCreate(BaseModel):
    """Schema for creating a task."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    priority: int = Field(default=5, ge=1, le=10)
    effort_days: float = Field(default=1.0, ge=0.1)
    effort_hours: Optional[float] = None  # Auto-calculated if not provided
    assignee_id: Optional[int] = None
    project_id: Optional[int] = None
    milestone_id: Optional[int] = None
    depends_on: list[int] = Field(default_factory=list, description="Task IDs")
    is_optional: bool = False
    is_deferred: bool = False
    tags: list[str] = Field(default_factory=list)
    sort_order: int = 0
    min_start_date: Optional[date] = None
    max_end_date: Optional[date] = None
    external_key: Optional[str] = Field(default=None, max_length=255)
    source: Optional[str] = Field(default=None, max_length=100)
    source_url: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    expected_version: Optional[int] = Field(default=None, ge=1)
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = None
    priority: Optional[int] = Field(default=None, ge=1, le=10)
    effort_days: Optional[float] = Field(default=None, ge=0.1)
    effort_hours: Optional[float] = None
    assignee_id: Optional[int] = None
    project_id: Optional[int] = None
    milestone_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    is_optional: Optional[bool] = None
    is_deferred: Optional[bool] = None
    tags: Optional[list[str]] = None
    sort_order: Optional[int] = None
    depends_on: Optional[list[int]] = Field(default=None, description="Task IDs this task depends on")
    min_start_date: Optional[date] = None
    max_end_date: Optional[date] = None
    external_key: Optional[str] = Field(default=None, max_length=255)
    source: Optional[str] = Field(default=None, max_length=100)
    source_url: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)


class TaskDependencyCreate(BaseModel):
    """Schema for creating a task dependency."""
    depends_on_id: int


class TaskReorder(BaseModel):
    """Schema for reordering tasks."""
    task_ids: list[int]
    iteration_id: Optional[int] = None
    parent_id: Optional[int] = None


class TaskMoveRequest(BaseModel):
    """Schema for moving a task subtree to another iteration."""
    iteration_id: int
    parent_id: Optional[int] = None
    expected_version: Optional[int] = Field(default=None, ge=1)


class TaskAssignee(BaseModel):
    """Brief assignee info for task."""
    id: int
    name: str

    class Config:
        from_attributes = True


class TaskClaimedBy(BaseModel):
    """Brief agent info for task claim state."""
    id: int
    name: str
    display_name: str

    class Config:
        from_attributes = True


class TaskProject(BaseModel):
    """Brief project info for task."""
    id: int
    name: str
    status: str
    health: str

    class Config:
        from_attributes = True


class TaskMilestone(BaseModel):
    """Brief milestone info for task."""
    id: int
    project_id: int
    name: str
    status: str
    target_date: Optional[date] = None

    class Config:
        from_attributes = True


class TaskAgentReadinessCriterion(BaseModel):
    """One deterministic criterion used for agent-readiness evaluation."""
    key: str
    label: str
    passed: bool
    reason: str


class TaskAgentReadiness(BaseModel):
    """Computed advisory readiness for agent execution."""
    is_ready: bool = False
    definition_ready: bool = False
    start_ready: bool = False
    blocker_codes: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    criteria: list[TaskAgentReadinessCriterion] = Field(default_factory=list)


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int
    iteration_id: int
    project_id: Optional[int] = None
    milestone_id: Optional[int] = None
    parent_id: Optional[int]
    title: str
    description: Optional[str]
    priority: int
    effort_days: float
    effort_hours: float
    project: Optional[TaskProject] = None
    milestone: Optional[TaskMilestone] = None
    assignee: Optional[TaskAssignee] = None
    status: str
    start_date: Optional[date]
    end_date: Optional[date]
    actual_start_date: Optional[date] = None  # When status changed to ACTIVE
    actual_end_date: Optional[date] = None    # When status changed to CLOSED
    min_start_date: Optional[date] = None
    max_end_date: Optional[date] = None
    is_overdue: bool = False
    is_delayed: bool = False  # start_date < today and status == PLANNED
    is_composite: bool = False
    is_optional: bool = False
    is_deferred: bool = False
    is_outside_constraints: bool = False
    tags: list[str] = []
    sort_order: int = 0
    external_key: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    external_links: list[ExternalLinkResponse] = Field(default_factory=list)
    request_count: int = 0
    agent_readiness: TaskAgentReadiness = Field(default_factory=TaskAgentReadiness)
    version: int = 1
    claimed_by: Optional[TaskClaimedBy] = None
    claim_expires_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    children: list["TaskResponse"] = []
    dependencies: list[int] = []

    class Config:
        from_attributes = True


class TaskMerge(BaseModel):
    """Request schema for merging tasks under a new parent."""
    task_ids: list[int] = Field(..., min_length=2, description="IDs of tasks to merge (min 2)")
    parent_title: str = Field(..., min_length=1, max_length=500)
    parent_description: Optional[str] = None


class TaskUnmerge(BaseModel):
    """Request schema for unmerging a parent task."""
    delete_parent: bool = Field(default=True, description="Delete the parent task after unmerging")


TaskBulkAction = Literal[
    "set_assignee",
    "clear_assignee",
    "auto_assign",
    "set_project",
    "clear_project",
    "set_milestone",
    "clear_milestone",
    "set_priority",
    "add_labels",
    "remove_labels",
    "set_flags",
    "change_status",
    "delete",
]

TaskBulkOutcome = Literal["updated", "deleted", "skipped", "failed", "would_update", "would_delete"]


class TaskBulkOperationRequest(BaseModel):
    """Request schema for selected-task bulk operations."""
    task_ids: list[int] = Field(..., min_length=1, max_length=200)
    action: TaskBulkAction
    payload: dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = True


class TaskBulkOperationResult(BaseModel):
    """Per-task result returned by a selected-task bulk operation."""
    task_id: int
    outcome: TaskBulkOutcome
    changes: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    error: Optional[str] = None
    task: Optional[TaskResponse] = None
    assignee_recommendation: Optional[AssigneeRecommendationResponse] = None


class TaskBulkOperationResponse(BaseModel):
    """Response for selected-task bulk operations."""
    requested_count: int
    succeeded_count: int
    failed_count: int
    dry_run: bool
    results: list[TaskBulkOperationResult] = Field(default_factory=list)


TaskImportDestination = Literal["tasks", "triage", "auto"]


class TasksImportRequest(BaseModel):
    """Request for importing tasks from text."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=MAX_TASK_TEXT_IMPORT_CHARS,
        description="Text content with tasks",
    )
    destination: TaskImportDestination = Field(
        "tasks",
        description="Where parsed rows should be created: tasks, triage, or auto split.",
    )


class TaskImportTriageItemResponse(BaseModel):
    """Triage item shape returned by task import endpoints."""
    id: int
    title: str
    description: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    external_key: Optional[str] = None
    status: str
    priority_hint: Optional[int] = None
    assignee_hint: Optional[str] = None
    project_hint_id: Optional[int] = None
    iteration_hint_id: Optional[int] = None
    labels: list[str] = Field(default_factory=list)
    snoozed_until: Optional[datetime] = None
    duplicate_of_id: Optional[int] = None
    duplicate_task_id: Optional[int] = None
    converted_task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TasksImportResponse(BaseModel):
    """Response for task import."""
    imported_count: int
    task_count: int = 0
    triage_count: int = 0
    tasks: list[TaskResponse] = Field(default_factory=list)
    triage_items: list[TaskImportTriageItemResponse] = Field(default_factory=list)


class TaskStatusChange(BaseModel):
    """Request for changing task status."""
    status: TaskStatus
    reason: Optional[str] = Field(default=None, max_length=500, description="Reason for status change")
    expected_version: Optional[int] = Field(default=None, ge=1)


class TaskStatusLogResponse(BaseModel):
    """Response for task status log entry."""
    id: int
    task_id: int
    task_title: Optional[str] = None
    from_status: str
    to_status: str
    changed_at: datetime
    reason: Optional[str] = None
    triggered_by: str = "user"
    affected_task_ids: list[int] = []


class TaskStatusStats(BaseModel):
    """Response for status transition statistics (aggregated)."""
    from_status: str
    to_status: str
    count: int


class CascadeUpdateInfo(BaseModel):
    """Information about cascading date updates."""
    task_id: int
    task_title: str
    old_start_date: Optional[date]
    new_start_date: Optional[date]
    old_end_date: Optional[date]
    new_end_date: Optional[date]


class TaskStatusChangeResponse(BaseModel):
    """Response for status change with cascade info."""
    task: TaskResponse
    cascade_updates: list[CascadeUpdateInfo] = []
    notifications_sent: bool = False


class TaskBatchUpdateItem(BaseModel):
    """Schema for a single task update item in a batch."""
    task_id: int
    update: TaskUpdate
    status_reason: Optional[str] = None
    expected_version: Optional[int] = Field(default=None, ge=1)


class TaskBatchUpdateRequest(BaseModel):
    """Schema for updating multiple tasks in a single request."""
    tasks: list[TaskBatchUpdateItem]


class TaskBatchUpdateResponseItem(BaseModel):
    """Schema for a single task update response inside a batch response."""
    task_id: int
    success: bool
    error: Optional[str] = None


class TaskBatchUpdateResponse(BaseModel):
    """Response schema for a batch task update."""
    results: list[TaskBatchUpdateResponseItem]
    updated_tasks: list[TaskResponse]
    schedule_result: Optional[Any] = None


# Enable forward references
TaskResponse.model_rebuild()
