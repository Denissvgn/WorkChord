"""Snapshot restore API schemas."""

from pydantic import BaseModel, Field


class SnapshotRestoreRequest(BaseModel):
    """Explicit acknowledgement required before destructive snapshot restore."""

    confirm: bool = False
    expected_revision: int | None = Field(default=None, ge=1)


class SnapshotRestoreResponse(BaseModel):
    """Recoverable and auditable result of a completed snapshot restore."""

    message: str
    success: bool = True
    source_snapshot: str
    pre_restore_snapshot: str
    restored_count: int
    audit_event_id: int
