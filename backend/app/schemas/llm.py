"""LLM integration schemas."""
from typing import Any, Optional
from pydantic import BaseModel, Field


class FormalizeRequest(BaseModel):
    """Request for task formalization via LLM."""
    context: Optional[str] = Field(default=None, description="Optional project context")


class FormalizeDraftRequest(BaseModel):
    """Request for formalizing unsaved task form data."""
    title: str = Field(..., min_length=1, description="Current unsaved task title")
    description: Optional[str] = Field(default=None, description="Current unsaved task description")
    context: Optional[str] = Field(default=None, description="Optional project context")


class SuggestedSubtask(BaseModel):
    """Suggested subtask from LLM."""
    title: str
    effort_days: float


class FormalizeResponse(BaseModel):
    """Response from task formalization."""
    original_title: str
    formalized_title: str
    suggested_description: str
    language: str = "en"
    suggested_effort_days: Optional[float] = None
    suggested_subtasks: list[SuggestedSubtask] = Field(default_factory=list)


class ImproveDescriptionRequest(BaseModel):
    """Request for improving task description."""
    current_description: str
    context: Optional[str] = None


class ImproveDescriptionResponse(BaseModel):
    """Response from description improvement."""
    improved_description: str
    language: str = "en"


class GroundedFact(BaseModel):
    """Fact or claim tied to an explicit source in the AI context pack."""

    claim: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)


class GroundedAISuggestionResponse(BaseModel):
    """Advisory AI task draft separated into grounded and suggested parts."""

    provider: Optional[str] = None
    model: Optional[str] = None
    language: str = "en"
    is_fallback: bool = False
    finish_reason: Optional[str] = None
    is_truncated: bool = False
    suggested_title: Optional[str] = None
    suggested_description: str = ""
    acceptance_criteria: list[str] = Field(default_factory=list)
    implementation_notes: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    grounded_facts: list[GroundedFact] = Field(default_factory=list)
    ungrounded_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class TaskAISuggestRequest(BaseModel):
    """Request for grounded advisory task AI suggestions."""

    title: str = Field(default="", max_length=500)
    description: Optional[str] = None
    priority: Optional[int] = Field(default=None, ge=1, le=10)
    effort_days: Optional[float] = Field(default=None, ge=0)
    effort_hours: Optional[float] = Field(default=None, ge=0)
    assignee_id: Optional[int] = None
    project_id: Optional[int] = None
    milestone_id: Optional[int] = None
    parent_id: Optional[int] = None
    depends_on: list[int] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    is_optional: Optional[bool] = None
    is_deferred: Optional[bool] = None
    min_start_date: Optional[str] = None
    max_end_date: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    external_key: Optional[str] = None
    template_id: Optional[int] = None
    user_context: Optional[str] = None
    extra_context: dict[str, Any] = Field(default_factory=dict)


class ExplainScheduleRequest(BaseModel):
    """Request for schedule explanation."""
    detail_level: str = Field(default="full", pattern="^(brief|full)$")


class ScheduleDecisionExplanation(BaseModel):
    """Human-readable explanation for a scheduling decision."""
    task_id: int
    task_title: str
    decision_type: str
    explanation: str


class WorkloadAnalysis(BaseModel):
    """Analysis of team workload."""
    balanced: bool
    issues: list[str] = Field(default_factory=list)


class ExplainScheduleResponse(BaseModel):
    """Response with schedule explanation."""
    summary: str
    decisions: list[ScheduleDecisionExplanation] = Field(default_factory=list)
    workload_analysis: WorkloadAnalysis
    provider: Optional[str] = None
    model: Optional[str] = None
    language: str = "en"
    is_fallback: bool = False
    finish_reason: Optional[str] = None
    is_truncated: bool = False
    warnings: list[str] = Field(default_factory=list)
