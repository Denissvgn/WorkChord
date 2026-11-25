"""Request bodies shared by the delivery prerequisite REST routes and MCP tools."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DeliveryDependencyInput(BaseModel):
    """Record a task or milestone prerequisite, optionally on a target branch."""

    kind: Literal["task", "milestone"]
    target_id: int = Field(gt=0)
    expected_version: int = Field(gt=0)
    target_branch: str | None = Field(default=None, max_length=255)


class DeliveryDependencyRetarget(BaseModel):
    """Change the target branch of an existing task prerequisite; null keeps only the acceptance gate."""

    model_config = ConfigDict(extra="forbid")

    expected_version: int = Field(gt=0)
    target_branch: str | None = Field(max_length=255)
