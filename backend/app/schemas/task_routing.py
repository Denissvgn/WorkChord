"""Structured routing of one task: its first rung, escalation ladder and reviewer.

The routing lives in the task's canonical brief, so brief revisions keep its history and the
brief text renders from it. Every rung and the reviewer name a model catalog entry by key; the
server fills the entry's effort, publisher and alias when it saves the routing.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

RoutingConflictMode = Literal["refuse", "warn"]
RoutingResolution = Literal["check", "apply_suggestion"]


class RoutingRung(BaseModel):
    """One model catalog entry that may execute the task."""

    model_config = ConfigDict(extra="forbid")
    catalog_key: str = Field(min_length=1, max_length=120, description="Key of a model catalog entry.")
    harness: str = Field(default="", max_length=120, description="Where the model runs, for people, such as an agent client name.")
    effort: str | None = Field(default=None, max_length=20, description="Filled by the server from the catalog entry.")
    publisher_key: str | None = Field(default=None, max_length=120, description="Filled by the server from the catalog entry.")
    configured_model_alias: str | None = Field(default=None, max_length=255, description="Filled by the server from the catalog entry.")

    @field_validator("catalog_key")
    @classmethod
    def canonical_key(cls, value: str) -> str:
        key = value.strip().lower()
        if not key:
            raise ValueError("A routing rung needs a catalog key")
        return key


class RoutingReviewer(RoutingRung):
    """The model that reviews the task's result, and optionally the reviewer profile to dispatch."""

    profile_id: int | None = Field(default=None, ge=1, description="Reviewer profile passed as reviewer_profile_id at dispatch.")
    instructions: str = Field(default="", max_length=2000, description="What the review checks, for example each criterion against its evidence.")


class TaskRouting(BaseModel):
    """First rung, escalation ladder and reviewer of one task."""

    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[1] = 1
    first_rung: RoutingRung | None = None
    escalation: list[RoutingRung] = Field(default_factory=list, max_length=8)
    escalate_after_failed_runs: int = Field(default=2, ge=1, le=10)
    after_last_rung: str = Field(default="", max_length=2000, description="What happens when the ladder is exhausted.")
    reviewer: RoutingReviewer | None = None
    notes: str = Field(default="", max_length=4000, description="Further routing rules, rendered after the ladder.")
    source_text: list[str] = Field(default_factory=list, max_length=20,
        description="Original sentences a conversion replaced with this structure; kept for audit and never rendered.")

    @field_validator("source_text")
    @classmethod
    def bounded_source(cls, value: list[str]) -> list[str]:
        if any(len(item) > 4000 for item in value):
            raise ValueError("Each converted routing sentence is at most 4000 characters")
        return value

    @model_validator(mode="after")
    def distinct_rungs(self):
        keys = [rung.catalog_key for rung in ([self.first_rung] if self.first_rung else []) + self.escalation]
        if len(keys) != len(set(keys)):
            raise ValueError("A catalog entry appears at most once in the first rung and escalation ladder")
        return self


class RoutingIssue(BaseModel):
    """One inconsistency between a task's routing, its assignee and the project policy."""

    code: str
    severity: Literal["conflict", "warning"]
    field: Literal["first_rung", "escalation", "reviewer", "assignee", "routing"]
    message: str
    catalog_key: str | None = None
    publisher_key: str | None = None


class RoutingCheck(BaseModel):
    """Routing consistency of one task for one assignee, with a consistent replacement."""

    task_id: int | None = None
    assignee_id: int | None = None
    assignee_profile_id: int | None = None
    assignee_publishers: list[str] = Field(default_factory=list)
    assignee_catalog_keys: list[str] = Field(default_factory=list)
    different_publisher_required: bool = False
    conflict_mode: RoutingConflictMode = "refuse"
    structured: bool = Field(default=False, description="The routing is stored as structure in the brief.")
    text_routing: bool = Field(default=False, description="The brief names routing only in free text; convert it to check it.")
    consistent: bool = True
    issues: list[RoutingIssue] = Field(default_factory=list)
    routing: TaskRouting | None = Field(default=None, description="The routing that was checked.")
    suggestion: TaskRouting | None = Field(default=None, description="A routing consistent with the assignee and policy, when it differs.")
    suggested_reviewer: RoutingReviewer | None = None
    applied: bool = Field(default=False, description="The suggestion was saved with this change.")


class RoutingConvert(BaseModel):
    """Preview or apply the conversion of free-text routing into structure."""

    model_config = ConfigDict(extra="forbid")
    expected_version: int = Field(ge=1)
    apply: bool = False
    routing: TaskRouting | None = Field(default=None,
        description="Routing that replaces what the conversion parsed, for example to settle an ambiguous model.")


class RoutingConvertResponse(BaseModel):
    """Result of a routing conversion preview or apply."""

    task_id: int
    already_structured: bool = False
    applied: bool = False
    routing: TaskRouting | None = None
    brief: dict | None = None
    removed: list[str] = Field(default_factory=list, description="Sentences the structured routing replaces.")
    unresolved: list[str] = Field(default_factory=list, description="Routing sentences kept as text because no single catalog entry matched.")
    check: RoutingCheck | None = None
    task_version: int | None = None
