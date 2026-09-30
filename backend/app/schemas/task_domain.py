"""Explicit task commands and typed action availability."""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


TaskAction = Literal["start_manual", "resolve_manual", "block", "unblock", "cancel", "reopen", "commit", "uncommit"]


class TaskActionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: TaskAction
    expected_version: int = Field(ge=1)
    reason: str = Field(min_length=1, max_length=2000)
    iteration_id: int | None = Field(default=None, ge=1)
    expected_revisions: dict[int, int] = Field(default_factory=dict)
    expected_claim_generation: int | None = Field(default=None, ge=0)
    expected_running_run_ids: list[int] = Field(default_factory=list, max_length=100)
    expected_live_assignment_ids: list[int] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def schedule_destination(self):
        if self.action == "commit" and self.iteration_id is None:
            raise ValueError("iteration_id is required for schedule commitment")
        if not self.reason.strip():
            raise ValueError("A reason is required")
        return self


class TaskActionBlocker(BaseModel):
    code: str
    message: str


class TaskActionAvailability(BaseModel):
    action: str
    allowed: bool
    blockers: list[TaskActionBlocker] = Field(default_factory=list)


class TaskActionsResponse(BaseModel):
    task_id: int
    version: int
    actions: list[TaskActionAvailability]
    claim_generation: int
    running_run_ids: list[int]
    live_assignment_ids: list[int]


class BacklogRestoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_versions: dict[int, int]
    reason: str = Field(min_length=1, max_length=2000)
