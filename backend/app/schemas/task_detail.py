"""Bounded UI projections with explicit completeness and deterministic cursors."""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.schemas.task import TaskResponse
from app.schemas.task_domain import TaskActionAvailability
from app.schemas.task_postponement import TaskPostponementRecord


class TaskReference(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    version: int
    status: str
    # The stored status, or canceled / superseded for withdrawn work (which keeps its old stored status).
    displayed_state: str | None = None
    project_id: int | None
    iteration_id: int | None
    parent_id: int | None
    owner_profile_id: int | None
    project_name: str | None = None
    iteration_name: str | None = None
    blocked_reason: str | None = None
    canceled_at: datetime | None = None
    acceptance_current: bool = False
    # Display name of the agent holding the live review assignment, if any.
    reviewer_name: str | None = None


class TaskReferencePage(BaseModel):
    items: list[TaskReference]
    has_more: bool
    next_after_id: int | None
    limit: int
    consistency: str = "live"


class TaskDetailResponse(BaseModel):
    task: TaskResponse
    ancestors: list[TaskReference]
    ancestors_complete: bool
    children: TaskReferencePage
    dependencies: TaskReferencePage
    execution_context_complete: bool = False
    reviewer_name: str | None = None
    postponement: TaskPostponementRecord | None = Field(
        default=None, description="The open postponement of postponed work, with each reactivation requirement and whether it is met.")


class HumanWorkReference(TaskReference):
    actions: list[TaskActionAvailability]


class HumanWorkResponse(BaseModel):
    state: str
    queues: dict[str, list[HumanWorkReference]]
    # The person's postponed, canceled and superseded work: shown as such, never as actionable work in a queue.
    stopped: list[HumanWorkReference] = Field(default_factory=list)
    # More stopped work exists than the first page lists (newest first).
    stopped_has_more: bool = False
    has_more: bool
    next_after_id: int | None
