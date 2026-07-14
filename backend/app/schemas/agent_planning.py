"""Schemas for idempotent, agent-authenticated PM setup commands."""

from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentPlanningCommandContext(BaseModel):
    """Required audit metadata carried by every PM setup command."""

    model_config = ConfigDict(extra="forbid")

    idempotency_key: str = Field(..., min_length=1, max_length=255)
    rationale: str = Field(..., min_length=1, max_length=2000)
    correlation_id: str = Field(..., min_length=1, max_length=255)

    @field_validator("idempotency_key", "rationale", "correlation_id")
    @classmethod
    def validate_log_safe_text(cls, value: str) -> str:
        """Reject outer whitespace and control characters in audit metadata."""
        if value != value.strip() or any(
            ord(character) < 32 or ord(character) == 127 for character in value
        ):
            raise ValueError(
                "Command metadata must not contain control characters or outer whitespace"
            )
        return value


class AgentPlanningReceipt(BaseModel):
    """Exact durable response stored for one PM setup mutation."""

    model_config = ConfigDict(extra="forbid")

    operation: str
    actor_id: int
    target_type: str
    target_id: int
    idempotency_key: str
    rationale: str
    correlation_id: str
    result: dict[str, Any]


class AgentScheduleCommand(BaseModel):
    """Optimistic scheduling command bound to observed task versions."""

    model_config = ConfigDict(extra="forbid")

    expected_task_versions: dict[int, int] = Field(default_factory=dict)
    expected_input_digest: str = Field(
        ...,
        min_length=64,
        max_length=64,
        pattern=r"^[0-9a-f]{64}$",
    )

    @field_validator("expected_task_versions")
    @classmethod
    def validate_versions(cls, value: dict[int, int]) -> dict[int, int]:
        """Require positive task ids and non-negative optimistic versions."""
        if any(task_id <= 0 for task_id in value):
            raise ValueError("expected_task_versions keys must be positive task ids")
        if any(version < 0 for version in value.values()):
            raise ValueError("expected_task_versions values must be non-negative")
        return value


class AgentScheduleTaskState(BaseModel):
    """One task state produced by schedule preview or apply."""

    task_id: int
    version: int
    start_date: date | None = None
    end_date: date | None = None
    calculated_effort_days: float | None = None


class AgentScheduleResult(BaseModel):
    """Schedule outcome plus the complete optimistic task-version token set."""

    success: bool
    decisions: list[dict[str, Any]] = Field(default_factory=list)
    workload_balanced: bool = True
    workload_issues: list[dict[str, Any]] = Field(default_factory=list)
    input_digest: str = Field(..., min_length=64, max_length=64)
    task_states: list[AgentScheduleTaskState] = Field(default_factory=list)
