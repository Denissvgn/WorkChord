"""Requests for coordinated control-plane maintenance windows."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class MaintenanceWindowCreate(BaseModel):
    """Announce one bounded window; it closes admission for new work at once."""

    model_config = ConfigDict(extra="forbid")

    release_label: str = Field(..., min_length=1, max_length=120)
    reason: str = Field(..., min_length=1, max_length=4000)
    planned_start_at: datetime
    planned_end_at: datetime
    max_outage_seconds: int = Field(..., ge=1, le=3600)
    expiry_margin_seconds: int = Field(default=900, ge=60, le=86400)


class MaintenanceWindowNotice(BaseModel):
    """An operator's record that a PM was told through another channel."""

    model_config = ConfigDict(extra="forbid")

    actor_id: int = Field(..., ge=1)
    channel: str = Field(..., min_length=1, max_length=60)
    reference: str = Field(..., min_length=1, max_length=500)


class MaintenanceWindowClose(BaseModel):
    """Close a begun window after the restart, or after a rollback."""

    model_config = ConfigDict(extra="forbid")

    outcome: Literal["completed", "rolled_back"]
    note: Optional[str] = Field(default=None, max_length=4000)


class MaintenanceWindowCancel(BaseModel):
    """Withdraw an announced window before it begins."""

    model_config = ConfigDict(extra="forbid")

    note: Optional[str] = Field(default=None, max_length=4000)


class MaintenanceOwnerAcknowledgement(BaseModel):
    """The live claim owner's acknowledgement, bound to its current fence."""

    model_config = ConfigDict(extra="forbid")

    task_id: int = Field(..., ge=1)
    claim_id: str = Field(..., min_length=16, max_length=64)
    claim_generation: int = Field(..., ge=1)
    run_id: Optional[int] = Field(default=None, ge=1)
