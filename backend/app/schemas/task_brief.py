"""Canonical brief inputs and separate execution evidence/review contracts."""

from datetime import datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class BriefCriterion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(default_factory=lambda: uuid4().hex, min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    revision: int = Field(default=1, ge=1)
    text: str = Field(min_length=1, max_length=4000)
    verification: str = Field(default="", max_length=4000)

    @field_validator("text")
    @classmethod
    def meaningful_text(cls, value):
        if not value.strip():
            raise ValueError("Criterion text cannot be blank")
        return value


class TaskBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[1] = 1
    goal: str = Field(default="", max_length=8000)
    context: str = Field(default="", max_length=20000)
    scope: str = Field(default="", max_length=12000)
    exclusions: str = Field(default="", max_length=12000)
    acceptance_criteria: list[BriefCriterion] = Field(default_factory=list, max_length=100)
    verification: str = Field(default="", max_length=12000)
    artifact_expectations: str = Field(default="", max_length=12000)

    @model_validator(mode="after")
    def unique_criteria(self):
        ids = [criterion.id for criterion in self.acceptance_criteria]
        if len(ids) != len(set(ids)):
            raise ValueError("Acceptance criterion IDs must be unique")
        return self


class BriefWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_version: int = Field(ge=1)
    brief: TaskBrief


class BriefConvert(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_version: int = Field(ge=1)
    apply: bool = False


class CriterionProgress(BaseModel):
    model_config = ConfigDict(extra="forbid")
    criterion_id: str = Field(min_length=1, max_length=64)
    criterion_revision: int = Field(ge=1)
    state: Literal["pending", "in_progress", "completed"] = "pending"
    evidence: str = Field(default="", max_length=8000)


class ProgressWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_version: int = Field(ge=1)
    criteria: list[CriterionProgress] = Field(max_length=100)
    artifacts: list[str] = Field(default_factory=list, max_length=50)

    @model_validator(mode="after")
    def validate_evidence(self):
        from app.utils.url_policy import normalize_stored_display_url
        ids = [item.criterion_id for item in self.criteria]
        if len(ids) != len(set(ids)):
            raise ValueError("Progress must contain each criterion at most once")
        self.artifacts = [normalize_stored_display_url(url) for url in self.artifacts]
        return self


class TaskReviewWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_version: int = Field(ge=1)
    brief_revision: int = Field(ge=0)
    artifact_revision: int = Field(ge=0)
    verdict: Literal["accept", "reject"]
    reason: str = Field(min_length=1, max_length=8000)
    evidence: str = Field(default="", max_length=8000)


class TaskReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    task_version: int
    brief_revision: int
    artifact_revision: int
    principal_id: int | None
    verdict: str
    reason: str
    evidence: str
    created_at: datetime
