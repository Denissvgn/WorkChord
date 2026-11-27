"""Postpone and reactivate commands and the postponement record they return."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.task import TaskResponse

RequirementKind = Literal["predecessor_accepted", "date", "owner_decision", "linked_resolved"]

MAX_REACTIVATION_REQUIREMENTS = 20


def _stripped(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        raise ValueError("A non-empty value is required")
    return value


class ReactivationRequirementInput(BaseModel):
    """One condition that must hold before postponed work resumes.

    - ``predecessor_accepted``: ``task_id`` names a task that must be accepted.
    - ``date``: ``on_date`` is a day after today in the task's working time zone.
    - ``owner_decision``: ``description`` says what the owner must decide.
    - ``linked_resolved``: ``task_id`` or ``triage_item_id`` names work that must be resolved.
    """

    model_config = ConfigDict(extra="forbid")

    kind: RequirementKind
    task_id: int | None = Field(default=None, ge=1)
    triage_item_id: int | None = Field(default=None, ge=1)
    on_date: date | None = None
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("description")
    @classmethod
    def _description(cls, value: str | None) -> str | None:
        return _stripped(value)

    @model_validator(mode="after")
    def _shape(self):
        given = {name for name in ("task_id", "triage_item_id", "on_date") if getattr(self, name) is not None}
        if self.kind == "predecessor_accepted" and given != {"task_id"}:
            raise ValueError("A predecessor_accepted requirement names exactly one task_id")
        if self.kind == "date" and given != {"on_date"}:
            raise ValueError("A date requirement takes exactly one on_date")
        if self.kind == "owner_decision" and (given or self.description is None):
            raise ValueError("An owner_decision requirement takes a description of the decision and no task, triage item or date")
        if self.kind == "linked_resolved" and given not in ({"task_id"}, {"triage_item_id"}):
            raise ValueError("A linked_resolved requirement names exactly one task_id or triage_item_id")
        return self


class TaskPostponeRequest(BaseModel):
    """Stop planned, active or resolved work until its reactivation requirements are met.

    Postponing work with a live claim, assignment or run releases them. Supply the
    current claim generation, running run IDs and live assignment IDs from
    ``GET /api/tasks/{task_id}/actions``, as for cancellation.
    """

    model_config = ConfigDict(extra="forbid")

    expected_version: int = Field(ge=1)
    reason: str = Field(min_length=1, max_length=2000)
    requirements: list[ReactivationRequirementInput] = Field(min_length=1, max_length=MAX_REACTIVATION_REQUIREMENTS)
    expected_claim_generation: int | None = Field(default=None, ge=0)
    expected_running_run_ids: list[int] = Field(default_factory=list, max_length=100)
    expected_live_assignment_ids: list[int] = Field(default_factory=list, max_length=100)

    @field_validator("reason")
    @classmethod
    def _reason(cls, value: str) -> str:
        return _stripped(value)


class TaskReactivateRequest(BaseModel):
    """Return postponed work to planned, or to resolved when it was postponed after resolution."""

    model_config = ConfigDict(extra="forbid")

    expected_version: int = Field(ge=1)
    reason: str = Field(min_length=1, max_length=2000)

    @field_validator("reason")
    @classmethod
    def _reason(cls, value: str) -> str:
        return _stripped(value)


class OwnerDecisionRequest(BaseModel):
    """Record that the owner made the decision an owner_decision requirement waits for.

    Only the workspace owner can record it, and the postponed work returns to its
    lifecycle when this was the last unmet requirement.
    """

    model_config = ConfigDict(extra="forbid")

    expected_version: int = Field(ge=1)
    decision: str = Field(min_length=1, max_length=2000, description="What the owner decided.")

    @field_validator("decision")
    @classmethod
    def _decision(cls, value: str) -> str:
        return _stripped(value)


class ReactivationRequirementResponse(BaseModel):
    id: int
    position: int
    kind: RequirementKind
    task_id: int | None = Field(default=None, description="The task this requirement names; null if it was deleted.")
    triage_item_id: int | None = Field(default=None, description="The triage item this requirement names; null if it was deleted.")
    on_date: date | None = None
    description: str | None = None
    met: bool = Field(description="Whether the requirement is met. A met requirement stays met.")
    met_at: datetime | None = Field(default=None, description="When the requirement was evaluated as met; null while unmet.")


class PostponementRelease(BaseModel):
    """Execution ownership the postponement ended through the fenced release."""

    claim_actor_id: int | None = None
    claim_generation: int | None = None
    assignment_ids: list[int] = Field(default_factory=list)
    run_ids: list[int] = Field(default_factory=list)


class TaskPostponementRecord(BaseModel):
    id: int
    task_id: int
    open: bool
    from_status: Literal["planned", "active", "resolved"]
    reason: str
    postponed_at: datetime
    postponed_by_principal_id: int | None = None
    postponed_by_actor_id: int | None = None
    task_version: int
    released: PostponementRelease
    requirements: list[ReactivationRequirementResponse]
    reactivated_at: datetime | None = None
    reactivated_to_status: Literal["planned", "resolved"] | None = None
    reactivation_trigger: str | None = Field(
        default=None, description="'command' for an explicit reactivation, 'requirements_met' when the last requirement was met, "
                                  "'supersession' when the postponed task was superseded by delivered work.")
    reactivation_reason: str | None = None
    reactivated_by_principal_id: int | None = None
    reactivated_by_actor_id: int | None = None


class TaskPostponementResponse(BaseModel):
    task: TaskResponse
    postponement: TaskPostponementRecord | None = Field(
        description="The open or most recent postponement; null only for work reactivated from a postponed state that had no record.",
    )
