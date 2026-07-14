"""GitHub integration schemas."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

GitHubAutomationEventType = Literal[
    "github_pr_opened",
    "github_pr_reopened",
    "github_pr_ready_for_review",
    "github_pr_synchronize",
    "github_pr_closed",
    "github_pr_merged",
]
GitHubAutomationFromStatus = Literal["planned", "active", "resolved", "closed"]
GitHubAutomationTargetStatus = Literal["active", "resolved", "closed"]
GitHubAutomationOutcome = Literal["applied", "skipped", "failed"]


class GitHubStatusAutomationRuleBase(BaseModel):
    """Shared GitHub status automation rule fields."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    enabled: bool = False
    github_event_type: GitHubAutomationEventType
    from_status: Optional[GitHubAutomationFromStatus] = None
    target_status: GitHubAutomationTargetStatus
    reason_template: Optional[str] = None
    sort_order: int = 0


class GitHubStatusAutomationRuleCreate(GitHubStatusAutomationRuleBase):
    """Create a GitHub status automation rule."""


class GitHubStatusAutomationRuleUpdate(BaseModel):
    """Update a GitHub status automation rule."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    enabled: Optional[bool] = None
    github_event_type: Optional[GitHubAutomationEventType] = None
    from_status: Optional[GitHubAutomationFromStatus] = None
    target_status: Optional[GitHubAutomationTargetStatus] = None
    reason_template: Optional[str] = None
    sort_order: Optional[int] = None


class GitHubStatusAutomationRuleResponse(GitHubStatusAutomationRuleBase):
    """Response for one GitHub status automation rule."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GitHubStatusAutomationResult(BaseModel):
    """Result of applying one GitHub status automation rule."""

    rule_id: int
    outcome: GitHubAutomationOutcome
    from_status: str
    target_status: str
    reason: Optional[str] = None
    error: Optional[str] = None


class GitHubWebhookResponse(BaseModel):
    """Response returned after receiving a GitHub webhook delivery."""

    accepted: bool
    event: str
    action: Optional[str] = None
    matched: bool = False
    external_link_id: Optional[int] = None
    task_id: Optional[int] = None
    triage_item_id: Optional[int] = None
    ignored_reason: Optional[str] = None
    automation_results: list[GitHubStatusAutomationResult] = Field(default_factory=list)
