"""Project schemas."""
from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.team import TeamMemberOptionResponse, TeamMemberProfileCompact


class ProjectStatus(str, Enum):
    """Project lifecycle status."""
    PROPOSED = "proposed"
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELED = "canceled"


class ProjectHealth(str, Enum):
    """Project delivery health."""
    UNKNOWN = "unknown"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"


class ProjectTargetDateRisk(str, Enum):
    """Target-date risk for project delivery."""
    UNKNOWN = "unknown"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"


class ProjectUpdateFreshness(str, Enum):
    """Freshness state for project stakeholder updates."""
    FRESH = "fresh"
    STALE = "stale"
    MISSING = "missing"
    NOT_REQUIRED = "not_required"


class ProjectMilestoneStatus(str, Enum):
    """Explicit lifecycle status for a project milestone."""
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELED = "canceled"


STALE_PROJECT_UPDATE_DAYS = 7


class InitiativeCreate(BaseModel):
    """Schema for creating an initiative."""
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    owner_id: Optional[int] = None
    owner_profile_id: Optional[int] = None
    health: ProjectHealth = ProjectHealth.UNKNOWN
    target_date: Optional[date] = None


class InitiativeUpdate(BaseModel):
    """Schema for updating an initiative."""
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    owner_id: Optional[int] = None
    owner_profile_id: Optional[int] = None
    health: Optional[ProjectHealth] = None
    target_date: Optional[date] = None


class InitiativeResponse(BaseModel):
    """Schema for initiative responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    owner_id: Optional[int] = None
    owner: Optional[TeamMemberOptionResponse] = None
    owner_profile_id: Optional[int] = None
    owner_profile: Optional[TeamMemberProfileCompact] = None
    health: str
    target_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime


class ProjectInitiativeSummary(BaseModel):
    """Compact initiative identity embedded in project responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    owner_id: Optional[int] = None
    owner: Optional[TeamMemberOptionResponse] = None
    owner_profile_id: Optional[int] = None
    owner_profile: Optional[TeamMemberProfileCompact] = None
    health: str
    target_date: Optional[date] = None


class ProjectCreate(BaseModel):
    """Schema for creating a project."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNED
    health: ProjectHealth = ProjectHealth.UNKNOWN
    owner_id: Optional[int] = None
    owner_profile_id: Optional[int] = None
    initiative_id: Optional[int] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    sort_order: int = 0


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    health: Optional[ProjectHealth] = None
    owner_id: Optional[int] = None
    owner_profile_id: Optional[int] = None
    initiative_id: Optional[int] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    sort_order: Optional[int] = None


class ProjectUpdateEntryCreate(BaseModel):
    """Schema for creating an append-only project update."""
    model_config = ConfigDict(extra="forbid")

    health: ProjectHealth
    summary: str = Field(..., min_length=1)
    progress_text: Optional[str] = None
    risks_text: Optional[str] = None
    decisions_text: Optional[str] = None
    next_steps_text: Optional[str] = None


class ProjectUpdateEntryResponse(BaseModel):
    """Schema for project update responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    health: str
    summary: str
    progress_text: Optional[str] = None
    risks_text: Optional[str] = None
    decisions_text: Optional[str] = None
    next_steps_text: Optional[str] = None
    created_by_session_id: Optional[int] = None
    created_by_actor_id: Optional[int] = None
    evidence_json: dict[str, Any] = Field(default_factory=dict)
    correlation_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    created_at: datetime


class ProjectMilestoneCreate(BaseModel):
    """Schema for creating a project milestone."""
    model_config = ConfigDict(extra="forbid")

    project_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    sort_order: int = 0
    status: ProjectMilestoneStatus = ProjectMilestoneStatus.PLANNED


class ProjectMilestoneCreateRequest(BaseModel):
    """API request for creating a project-scoped milestone."""
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    sort_order: int = 0
    status: ProjectMilestoneStatus = ProjectMilestoneStatus.PLANNED


class ProjectMilestoneUpdate(BaseModel):
    """Schema for updating a project milestone."""
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    target_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    sort_order: Optional[int] = None
    status: Optional[ProjectMilestoneStatus] = None


class ProjectMilestoneResponse(BaseModel):
    """Schema for project milestone responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    description: Optional[str] = None
    target_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    sort_order: int
    status: str
    created_at: datetime
    updated_at: datetime


class RoadmapMilestonePage(BaseModel):
    """Cursor page of milestones used by the portfolio roadmap."""
    items: list[ProjectMilestoneResponse] = Field(default_factory=list)
    next_cursor: Optional[int] = None


class ProjectMilestoneDeleteResponse(BaseModel):
    """Response returned after deleting a project milestone."""
    success: bool
    message: str
    detached_task_count: int = 0


class ProjectMilestoneSummary(BaseModel):
    """Compact milestone identity for project task grouping."""
    id: int
    project_id: int
    name: str
    status: str
    target_date: Optional[date] = None
    sort_order: int = 0


class ProjectMilestoneTaskGroup(BaseModel):
    """Task progress metrics grouped under one milestone or unassigned work."""
    milestone_id: Optional[int] = None
    milestone: Optional[ProjectMilestoneSummary] = None
    name: str
    task_count: int = 0
    completed_tasks: int = 0
    completion_percent: float = 0.0
    status_counts: dict[str, int] = Field(
        default_factory=lambda: {
            "planned": 0,
            "active": 0,
            "resolved": 0,
            "closed": 0,
        }
    )
    total_effort_days: float = 0.0
    remaining_effort_days: float = 0.0


class ProjectResponse(BaseModel):
    """Schema for project response."""
    id: int
    name: str
    description: Optional[str] = None
    status: str
    health: str
    owner_id: Optional[int] = None
    owner: Optional[TeamMemberOptionResponse] = None
    owner_profile_id: Optional[int] = None
    owner_profile: Optional[TeamMemberProfileCompact] = None
    initiative_id: Optional[int] = None
    initiative: Optional[ProjectInitiativeSummary] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    sort_order: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectPortfolioSummary(BaseModel):
    """Compact project signals for portfolio tables."""
    project_id: int
    total_tasks: int = 0
    completed_tasks: int = 0
    total_effort_days: float = 0.0
    remaining_effort_days: float = 0.0
    blocked_tasks: int = 0
    overdue_tasks: int = 0
    target_date_risk: ProjectTargetDateRisk = ProjectTargetDateRisk.UNKNOWN


class ProjectSummary(BaseModel):
    """Summary statistics for a project."""
    id: int
    name: str
    status: str
    health: str
    owner_id: Optional[int] = None
    owner: Optional[TeamMemberOptionResponse] = None
    owner_profile_id: Optional[int] = None
    owner_profile: Optional[TeamMemberProfileCompact] = None
    initiative_id: Optional[int] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    total_tasks: int = 0
    completed_tasks: int = 0
    completion_percent: float = 0.0
    active_tasks: int = 0
    blocked_tasks: int = 0
    overdue_tasks: int = 0
    target_date_risk: ProjectTargetDateRisk = ProjectTargetDateRisk.UNKNOWN
    target_date_risk_reason: Optional[str] = None
    target_date_slip_days: int = 0
    days_until_target: Optional[int] = None
    status_counts: dict[str, int] = Field(
        default_factory=lambda: {
            "planned": 0,
            "active": 0,
            "resolved": 0,
            "closed": 0,
        }
    )
    total_effort_days: float = 0.0
    remaining_effort_days: float = 0.0
    milestone_groups: list[ProjectMilestoneTaskGroup] = Field(default_factory=list)
    request_count: int = 0
    task_start_date: Optional[date] = None
    task_end_date: Optional[date] = None
    latest_update: Optional[ProjectUpdateEntryResponse] = None
    latest_update_at: Optional[datetime] = None
    days_since_latest_update: Optional[int] = None
    update_freshness: ProjectUpdateFreshness = ProjectUpdateFreshness.MISSING
    is_update_stale: bool = True
    stale_update_threshold_days: int = STALE_PROJECT_UPDATE_DAYS
