"""Bounded, non-executable evidence prepared for one review of an immutable candidate."""

from typing import Annotated, Literal

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

Positive = Annotated[int, Field(strict=True, ge=1)]
Sha256 = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class ReviewTestEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=180, pattern=r"^[A-Za-z0-9_][A-Za-z0-9_.:/-]*$")
    result_sha256: Sha256

    @field_validator("name")
    @classmethod
    def require_local_identifier(cls, name):
        if any(part in {"", ".", ".."} for part in name.split("/")):
            raise ValueError("Use a test identifier relative to the reviewed source.")
        return name


class ReviewEvidenceIssue(BaseModel):
    """The operator attests to the manifest of material delivered to the specified verifier."""

    model_config = ConfigDict(extra="forbid")
    action: Literal["issue"]
    expected_task_version: Positive
    expected_assessment_id: Positive
    expected_brief_revision: Annotated[int, Field(strict=True, ge=0)]
    expected_artifact_revision: Annotated[int, Field(strict=True, ge=0)]
    commit_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    reviewer_actor_id: Positive
    binding_id: Positive
    expected_binding_revision: Positive
    method: Literal["source_only", "source_and_tests"]
    packet_sha256: Sha256
    tests: list[ReviewTestEvidence] = Field(default_factory=list, max_length=32)
    expires_at: AwareDatetime

    @model_validator(mode="after")
    def check_evidence_set(self):
        if bool(self.tests) != (self.method == "source_and_tests"):
            raise ValueError("Only source_and_tests evidence includes named test results.")
        if len({t.name for t in self.tests}) != len(self.tests):
            raise ValueError("Named test evidence must be unique.")
        return self


class ReviewEvidenceRevocation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["revoke"]
    evidence_id: Positive


ReviewEvidenceCommand = Annotated[
    ReviewEvidenceIssue | ReviewEvidenceRevocation, Field(discriminator="action")
]


class ScopedReviewEvidence(BaseModel):
    """Compact owner and validity information returned by a scoped verification preview."""

    model_config = ConfigDict(extra="forbid")
    id: Positive
    digest: Sha256
    candidate_digest: Sha256
    packet_sha256: Sha256
    method: Literal["source_only", "source_and_tests"]
    reviewer_actor_id: Positive
    binding_id: Positive
    binding_revision: Positive
    expires_at: AwareDatetime
    assignment_id: Positive | None = Field(default=None, exclude_if=lambda value: value is None)
    assignment_state: Literal["queued", "accepted"] | None = Field(
        default=None, exclude_if=lambda value: value is None
    )
