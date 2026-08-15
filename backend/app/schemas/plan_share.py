"""Schemas for immutable read-only plan shares."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PlanShareResponse(BaseModel):
    """A revocable plan snapshot link and its immutable captured data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    public_id: str
    iteration_id: int
    iteration_name: str
    created_by_display: str
    snapshot_data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    revoked_at: datetime | None = None
