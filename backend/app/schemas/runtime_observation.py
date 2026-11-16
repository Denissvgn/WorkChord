"""Advisory runtime observation contracts."""

from datetime import datetime, timedelta
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.agent import check_harness_identity
from app.utils.time import as_utc, utc_now

ObservationKind = Literal["session_active", "session_idle", "session_ended", "model_observed"]


class AgentRuntimeObservationCreate(BaseModel):
    """One thing an independent observer saw of a runtime session.

    ``model_observed`` carries the model the observer saw the session use;
    the other kinds describe the session's state.
    """

    model_config = ConfigDict(extra="forbid")

    kind: ObservationKind
    harness_kind: str = Field(min_length=1, max_length=40)
    harness_session_id: str = Field(min_length=1, max_length=255)
    observed_at: datetime
    idempotency_key: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$")
    task_id: Optional[int] = Field(default=None, ge=1)
    run_id: Optional[int] = Field(default=None, ge=1)
    subject_actor_id: Optional[int] = Field(default=None, ge=1)
    observed_model: Optional[str] = Field(default=None, min_length=1, max_length=255)

    @field_validator("observed_at")
    @classmethod
    def bounded_observation_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("observed_at must include a time zone")
        now = utc_now()
        if not now - timedelta(days=7) <= as_utc(value) <= now + timedelta(minutes=5):
            raise ValueError("observed_at must be within the last seven days")
        return value

    @model_validator(mode="after")
    def consistent_observation(self) -> "AgentRuntimeObservationCreate":
        check_harness_identity(self.harness_kind, self.harness_session_id, label="harness")
        if (self.kind == "model_observed") != (self.observed_model is not None):
            raise ValueError("observed_model is required for model_observed and only for it")
        if self.observed_model is not None and not self.observed_model.isprintable():
            raise ValueError("observed_model must be plain text")
        return self


class AgentRuntimeObservationResponse(BaseModel):
    """A recorded observation. It is advisory and never affects dispatch."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: ObservationKind
    harness_kind: str
    harness_session_id: str
    task_id: Optional[int] = None
    run_id: Optional[int] = None
    subject_actor_id: Optional[int] = None
    observed_model: Optional[str] = None
    observer_label: Optional[str] = None
    observed_at: datetime
    received_at: datetime
    advisory: Literal[True] = True
    affects_dispatch: Literal[False] = False


class AgentRuntimeObservationCleanupResponse(BaseModel):
    removed: int
    retention_days: int
    limit: int
