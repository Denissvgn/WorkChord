"""Triage item schemas."""
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.task import TaskResponse


class TriageItemStatus(str, Enum):
    """Triage item lifecycle status."""
    NEW = "new"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    DUPLICATE = "duplicate"
    SNOOZED = "snoozed"
    CONVERTED = "converted"


class TriageItemCreate(BaseModel):
    """Schema for creating a triage item."""
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    source: Optional[str] = Field(default=None, max_length=100)
    source_url: Optional[str] = Field(default=None, max_length=1000)
    external_key: Optional[str] = Field(default=None, max_length=255)
    status: TriageItemStatus = TriageItemStatus.NEW
    priority_hint: Optional[int] = Field(default=None, ge=1, le=10)
    assignee_hint: Optional[str] = Field(default=None, max_length=255)
    project_hint_id: Optional[int] = None
    iteration_hint_id: Optional[int] = None
    labels: list[str] = Field(default_factory=list)
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    snoozed_until: Optional[datetime] = None
    duplicate_of_id: Optional[int] = None
    duplicate_task_id: Optional[int] = None
    converted_task_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_duplicate_target(self):
        """Reject ambiguous duplicate targets."""
        if self.duplicate_of_id is not None and self.duplicate_task_id is not None:
            raise ValueError("Use either duplicate_of_id or duplicate_task_id, not both.")
        return self


class TriageItemUpdate(BaseModel):
    """Schema for updating a triage item."""
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = None
    source: Optional[str] = Field(default=None, max_length=100)
    source_url: Optional[str] = Field(default=None, max_length=1000)
    external_key: Optional[str] = Field(default=None, max_length=255)
    status: Optional[TriageItemStatus] = None
    priority_hint: Optional[int] = Field(default=None, ge=1, le=10)
    assignee_hint: Optional[str] = Field(default=None, max_length=255)
    project_hint_id: Optional[int] = None
    iteration_hint_id: Optional[int] = None
    labels: Optional[list[str]] = None
    metadata_json: Optional[dict[str, Any]] = None
    snoozed_until: Optional[datetime] = None
    duplicate_of_id: Optional[int] = None
    duplicate_task_id: Optional[int] = None
    converted_task_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_duplicate_target(self):
        """Reject ambiguous duplicate targets."""
        if self.duplicate_of_id is not None and self.duplicate_task_id is not None:
            raise ValueError("Use either duplicate_of_id or duplicate_task_id, not both.")
        return self


class TriageItemResponse(BaseModel):
    """Schema for triage item response."""
    id: int
    title: str
    description: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    external_key: Optional[str] = None
    status: str
    priority_hint: Optional[int] = None
    assignee_hint: Optional[str] = None
    project_hint_id: Optional[int] = None
    iteration_hint_id: Optional[int] = None
    labels: list[str] = Field(default_factory=list)
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    snoozed_until: Optional[datetime] = None
    duplicate_of_id: Optional[int] = None
    duplicate_task_id: Optional[int] = None
    converted_task_id: Optional[int] = None
    request_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TriageActionRequest(BaseModel):
    """Request for simple triage status actions."""
    reason: Optional[str] = Field(default=None, max_length=500)


class TriageSnoozeRequest(BaseModel):
    """Request for snoozing a triage item."""
    snoozed_until: datetime
    reason: Optional[str] = Field(default=None, max_length=500)


class TriageDuplicateRequest(BaseModel):
    """Request for marking a triage item as duplicate."""
    duplicate_of_id: Optional[int] = None
    duplicate_task_id: Optional[int] = None
    link_request_to_duplicate_task: bool = False
    reason: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_duplicate_target(self):
        """Require exactly one duplicate target."""
        has_item = self.duplicate_of_id is not None
        has_task = self.duplicate_task_id is not None
        if has_item == has_task:
            raise ValueError("Set exactly one of duplicate_of_id or duplicate_task_id.")
        return self


class TriageDuplicateSuggestion(BaseModel):
    """Candidate duplicate returned by advisory duplicate search."""
    target_type: Literal["triage_item", "task"]
    target_id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    external_key: Optional[str] = None
    labels: list[str] = Field(default_factory=list)
    project_id: Optional[int] = None
    iteration_id: Optional[int] = None
    score: float
    signals: list[str] = Field(default_factory=list)


class TriageDuplicateSuggestionsResponse(BaseModel):
    """Response for advisory duplicate suggestions."""
    triage_item_id: int
    triage_items: list[TriageDuplicateSuggestion] = Field(default_factory=list)
    tasks: list[TriageDuplicateSuggestion] = Field(default_factory=list)


class TriageClassificationDraft(BaseModel):
    """Internal normalized triage classification draft before persistence."""
    model_config = ConfigDict(extra="ignore")

    suggested_type_label_slug: Optional[str] = Field(default=None, max_length=100)
    suggested_area_label_slug: Optional[str] = Field(default=None, max_length=100)
    suggested_priority: Optional[int] = Field(default=None, ge=1, le=10)
    suggested_label_slugs: list[str] = Field(default_factory=list)
    unmatched_label_text: list[str] = Field(default_factory=list)
    suggested_assignee_id: Optional[int] = None
    suggested_assignee_hint: Optional[str] = Field(default=None, max_length=255)
    suggested_project_id: Optional[int] = None
    duplicate_candidates: list[dict[str, Any]] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0, le=1)
    rationale: Optional[str] = None
    language: str = "en"
    is_fallback: bool = False
    raw_response_json: dict[str, Any] = Field(default_factory=dict)


class TriageClassificationSuggestionResponse(BaseModel):
    """Stored advisory classification suggestion for a triage item."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    triage_item_id: int
    suggested_type_label_slug: Optional[str] = None
    suggested_area_label_slug: Optional[str] = None
    suggested_priority: Optional[int] = None
    suggested_label_slugs: list[str] = Field(default_factory=list)
    unmatched_label_text: list[str] = Field(default_factory=list)
    suggested_assignee_id: Optional[int] = None
    suggested_assignee_hint: Optional[str] = None
    suggested_project_id: Optional[int] = None
    duplicate_candidates: list[dict[str, Any]] = Field(default_factory=list)
    confidence: float = 0.0
    rationale: Optional[str] = None
    language: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    is_fallback: bool = False
    raw_response_json: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class TriageTaskDraftRequest(BaseModel):
    """Request for transient AI-assisted triage task drafting."""
    model_config = ConfigDict(extra="forbid")

    template_id: Optional[int] = None
    classification_suggestion_id: Optional[int] = None
    current_title: Optional[str] = Field(default=None, max_length=500)
    current_description: Optional[str] = None


class TriageTaskDraftResponse(BaseModel):
    """Transient suggested task details for triage conversion."""
    triage_item_id: int
    suggested_title: str
    suggested_description: str
    suggested_checklist: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    template_id: Optional[int] = None
    classification_suggestion_id: Optional[int] = None
    is_fallback: bool = False
    provider: Optional[str] = None
    model: Optional[str] = None
    language: str = "en"
    finish_reason: Optional[str] = None
    is_truncated: bool = False
    grounded_facts: list[dict[str, Any]] = Field(default_factory=list)
    implementation_notes: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    ungrounded_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    rationale: Optional[str] = None


class TriageConvertToTaskRequest(BaseModel):
    """Request for converting a triage item to a task."""
    iteration_id: int
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    priority: Optional[int] = Field(default=None, ge=1, le=10)
    tags: Optional[list[str]] = None
    effort_days: float = Field(default=1.0, ge=0.1)
    effort_hours: Optional[float] = None
    depends_on: list[int] = Field(default_factory=list, description="Task IDs")
    scope: list[str] = Field(default_factory=list)
    out_of_scope: list[str] = Field(default_factory=list)
    suggested_checklist: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    verification: list[str] = Field(default_factory=list)
    expected_artifacts: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    implementation_notes: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)


class TriageConvertToTaskResponse(BaseModel):
    """Response for triage item conversion."""
    triage_item: TriageItemResponse
    task: TaskResponse
