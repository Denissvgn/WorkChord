"""Bounded UI projections with explicit completeness and deterministic cursors."""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.schemas.task import TaskResponse
from app.schemas.task_domain import TaskActionAvailability


class TaskReference(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    version: int
    status: str
    project_id: int | None
    iteration_id: int | None
    parent_id: int | None
    owner_profile_id: int | None
    project_name: str | None = None
    iteration_name: str | None = None
    blocked_reason: str | None = None
    canceled_at: datetime | None = None
    acceptance_current: bool = False


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


class HumanWorkReference(TaskReference):
    actions: list[TaskActionAvailability]


class HumanWorkResponse(BaseModel):
    state: str
    queues: dict[str, list[HumanWorkReference]]
    has_more: bool
    next_after_id: int | None
