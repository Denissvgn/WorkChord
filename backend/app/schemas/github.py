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


class GitHubSubmissionReview(BaseModel):
    """One review assignment bound to a submitted commit."""

    assignment_id: int
    actor_id: Optional[int] = None
    state: str


class GitHubPullSubmission(BaseModel):
    """One run's submitted commit for a pull request, with the review that saw it."""

    run_id: int
    commit_sha: str
    commit_url: Optional[str] = None
    pr_url: Optional[str] = None
    submitted_at: Optional[datetime] = None
    reviews: list[GitHubSubmissionReview] = Field(default_factory=list)


class GitHubPullChecks(BaseModel):
    """Checks GitHub reported for the observed head commit."""

    state: Optional[str] = None
    total: Optional[int] = None
    sha: Optional[str] = None
    error: Optional[str] = None


class GitHubPullReview(BaseModel):
    """The WorkChord review state of the task, decided only by the independent reviewer."""

    accepted: bool
    state: str


class GitHubPullReconciliation(BaseModel):
    """A linked pull request compared with what the task submitted."""

    link_id: int
    url: Optional[str] = None
    title: Optional[str] = None
    state: str
    submitted_sha: Optional[str] = None
    submissions: list[GitHubPullSubmission] = Field(default_factory=list)
    observed_head_sha: Optional[str] = None
    target_branch: Optional[str] = None
    checks: GitHubPullChecks
    merged: bool
    merge_commit_sha: Optional[str] = None
    merged_at: Optional[str] = None
    closed_at: Optional[str] = None
    observed_at: Optional[datetime] = None
    observation_source: Optional[str] = None
    observation_error: Optional[str] = None
    review: GitHubPullReview
    differences: list[str] = Field(default_factory=list)
    next_owner: str
    next_action: str


class GitHubReplacementRole(BaseModel):
    """The replacement disposition the task takes part in."""

    role: Literal["original", "replacement"]
    original_task_id: int
    replacement_task_id: int


class GitHubSuccessor(BaseModel):
    """The task that replaced this one, with its own pull requests."""

    task_id: int
    status: str
    pull_requests: list[GitHubPullReconciliation] = Field(default_factory=list)


class GitHubReconciliationResponse(BaseModel):
    """What a task submitted against what GitHub shows now, and who acts next."""

    task_id: int
    task_status: str
    accepted: bool
    replacement: Optional[GitHubReplacementRole] = None
    successor: Optional[GitHubSuccessor] = None
    pull_requests: list[GitHubPullReconciliation] = Field(default_factory=list)
