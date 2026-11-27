"""Clean-replacement disposition commands and their auditable projection."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskReplacementCreate(BaseModel):
    """Replace an unaccepted original with a fresh task built from a clean base."""

    model_config = ConfigDict(extra="forbid")

    replacement_task_id: int = Field(..., ge=1)
    expected_original_version: int = Field(..., ge=1)
    expected_replacement_version: int = Field(..., ge=1)
    reason: str = Field(..., min_length=1, max_length=4000)
    owner_decision: str = Field(..., min_length=1, max_length=4000,
                                description="The owner's recorded decision that authorizes this replacement.")
    base_commit_url: str = Field(..., min_length=1, max_length=1000,
                                 description="Immutable GitHub commit the replacement is built from.")
    carried_run_ids: list[int] = Field(..., max_length=50,
                                       description="Original runs whose commits the replacement carries; empty for a clean rebuild.")

    @field_validator("reason", "owner_decision", "base_commit_url")
    @classmethod
    def _stripped(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("A non-empty value is required")
        return value

    @field_validator("carried_run_ids")
    @classmethod
    def _distinct(cls, value: list[int]) -> list[int]:
        if any(item < 1 for item in value) or len(set(value)) != len(value):
            raise ValueError("Carried runs must be distinct positive run IDs")
        return sorted(value)


class TaskSupersessionCreate(BaseModel):
    """Record that work already closed or accepted delivered this original's deliverable."""

    model_config = ConfigDict(extra="forbid")

    successor_task_id: int = Field(..., ge=1, description="Closed or accepted leaf task in the same project.")
    expected_original_version: int = Field(..., ge=1)
    expected_successor_version: int = Field(..., ge=1)
    reason: str = Field(..., min_length=1, max_length=4000,
                        description="Why the successor delivers the original's work.")

    @field_validator("reason")
    @classmethod
    def _stripped(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("A non-empty value is required")
        return value


class ReplacementContributor(BaseModel):
    """One recorded attempt with exactly the attribution the server holds for it."""

    run_id: int | None = None
    actor_id: int | None = None
    profile_id: int | None = None
    publisher_key: str | None = None
    commit_urls: list[str] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)
    attributed: bool
    carried_from_task_id: int | None = None


class ReplacementDecision(BaseModel):
    reason: str
    owner_decision: str | None = None
    decided_at: datetime
    decided_by_principal_id: int | None = None
    decided_by_actor_id: int | None = None


class ReplacementReviewPolicy(BaseModel):
    require_different_review_publisher_at_decision: bool
    require_different_review_publisher: bool


class ReplacementMovedDependency(BaseModel):
    task_id: int
    kind: Literal["schedule", "delivery", "reactivation"]
    action: Literal["moved", "merged", "removed", "converted"]


class ReplacementOriginal(BaseModel):
    task_id: int
    status: str
    canceled: bool
    independently_accepted: Literal[False] = False
    status_at_decision: str
    version_at_decision: int
    attempts: list[ReplacementContributor]
    unattributed_run_ids: list[int]


class ReplacementCandidate(BaseModel):
    base_commit_url: str | None = None
    commit_url: str | None = None
    pr_url: str | None = None
    digest: str | None = None


class ReplacementTask(BaseModel):
    task_id: int
    status: str
    accepted: bool
    recorded_base_commit_url: str | None = None
    candidate: ReplacementCandidate | None = None
    contributors: list[ReplacementContributor]


class ReplacementAcceptance(BaseModel):
    """The deliverable is counted once: only the replacement can be accepted."""

    deliverable_task_id: int
    state: Literal["clean", "held"]
    hold_reasons: list[str]
    unattributed_carried_run_ids: list[int]


class TaskReplacementResponse(BaseModel):
    id: int
    project_id: int
    disposition: Literal["replacement", "supersession"]
    role: Literal["original", "replacement", "successor"]
    original_task_id: int
    replacement_task_id: int
    decision: ReplacementDecision
    review_policy: ReplacementReviewPolicy
    original: ReplacementOriginal
    replacement: ReplacementTask
    carried_contributions: list[ReplacementContributor]
    moved_dependencies: list[ReplacementMovedDependency]
    moved_release_ids: list[int]
    acceptance: ReplacementAcceptance
