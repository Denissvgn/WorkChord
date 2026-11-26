"""Attributable execution provenance for resolved work that never ran through recorded runs."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ManualProvenanceExecutor(BaseModel):
    """The human or agent that actually executed the work."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["human", "agent"]
    principal_id: int | None = Field(default=None, ge=1, description="The human who executed the work; required for kind human.")
    actor_id: int | None = Field(default=None, ge=1, description="The agent actor that executed the work; required for kind agent.")
    model_binding_id: int | None = Field(default=None, ge=1, description=(
        "The agent's model binding used for the work; its default binding when omitted. Only for kind agent."))

    @model_validator(mode="after")
    def _one_identity(self):
        if self.kind == "human" and (self.principal_id is None or self.actor_id is not None or self.model_binding_id is not None):
            raise ValueError("A human executor names principal_id only")
        if self.kind == "agent" and (self.actor_id is None or self.principal_id is not None):
            raise ValueError("An agent executor names actor_id and optionally model_binding_id")
        return self


class ManualProvenanceWrite(BaseModel):
    """Record who executed one resolved task and the exact repository candidate they delivered."""

    model_config = ConfigDict(extra="forbid")

    expected_version: int = Field(..., ge=1)
    artifact_revision: int = Field(..., ge=0, description="The task's current artifact revision; the record applies to it only.")
    executor: ManualProvenanceExecutor
    head_commit_url: str = Field(..., min_length=1, max_length=1000,
                                 description="Immutable GitHub commit URL of the delivered head.")
    commit_urls: list[str] = Field(default_factory=list, max_length=250, description=(
        "Every GitHub commit the executor contributed to the candidate. The head commit is always included."))
    pr_url: str | None = Field(default=None, max_length=1000, description="The GitHub pull request that carries the head commit.")
    base_commit_url: str | None = Field(default=None, max_length=1000, description=(
        "Immutable GitHub commit the work started from, for a commit range without a pull request."))
    reason: str = Field(..., min_length=1, max_length=2000,
                        description="Why the work was executed outside recorded runs and how the record was established.")

    @field_validator("reason", "head_commit_url")
    @classmethod
    def _stripped(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("A non-empty value is required")
        return value

    @field_validator("pr_url", "base_commit_url")
    @classmethod
    def _optional_stripped(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Omit the field instead of sending an empty value")
        return value

    @field_validator("commit_urls")
    @classmethod
    def _commits(cls, value: list[str]) -> list[str]:
        value = [item.strip() for item in value]
        if any(not item or len(item) > 1000 for item in value):
            raise ValueError("Commit URLs must be non-empty GitHub commit URLs")
        return value

    @model_validator(mode="after")
    def _candidate_shape(self):
        if self.pr_url is None and self.base_commit_url is None:
            raise ValueError("Name the pull request or the base commit so the candidate can be verified")
        return self


class ManualProvenanceExecutorRecord(BaseModel):
    kind: Literal["human", "agent"]
    principal_id: int | None = None
    actor_id: int | None = None
    profile_ids: list[int] = Field(default_factory=list, description="Profiles that count as the executor's for review independence.")
    binding_id: int | None = None
    catalog_key: str | None = None
    publisher_key: str | None = Field(default=None, description="The agent executor's model publisher at the time of the record.")


class ManualProvenanceResponse(BaseModel):
    """The recorded provenance as it appears on the task timeline."""

    event_id: int
    task_id: int
    task_version: int
    brief_revision: int
    artifact_revision: int
    executor: ManualProvenanceExecutorRecord
    head_commit_url: str
    commit_urls: list[str]
    pr_url: str | None = None
    base_commit_url: str | None = None
    reason: str
    recorded_by_principal_id: int | None = None
    recorded_by_actor_id: int | None = None
    recorded_at: datetime | None = None
