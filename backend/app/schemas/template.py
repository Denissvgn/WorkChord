"""Reusable work template schemas."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class TemplateType(str, Enum):
    """Template target type."""
    TASK = "task"
    PROJECT = "project"
    TRIAGE = "triage"


class WorkTemplateCreate(BaseModel):
    """Schema for creating a reusable work template."""
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    template_type: TemplateType
    default_title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    default_description: Optional[str] = None
    default_priority: Optional[int] = Field(default=None, ge=1, le=10)
    default_effort_days: Optional[float] = Field(default=None, ge=0.1)
    default_labels: list[str] = Field(default_factory=list)
    default_checklist: list[str] = Field(default_factory=list)
    default_payload: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    sort_order: int = 0


class WorkTemplateUpdate(BaseModel):
    """Schema for updating a reusable work template."""
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    template_type: Optional[TemplateType] = None
    default_title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    default_description: Optional[str] = None
    default_priority: Optional[int] = Field(default=None, ge=1, le=10)
    default_effort_days: Optional[float] = Field(default=None, ge=0.1)
    default_labels: Optional[list[str]] = None
    default_checklist: Optional[list[str]] = None
    default_payload: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class WorkTemplateResponse(BaseModel):
    """Schema for reusable work template responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    seed_key: Optional[str] = None
    template_type: str
    default_title: Optional[str] = None
    default_description: Optional[str] = None
    default_priority: Optional[int] = None
    default_effort_days: Optional[float] = None
    default_labels: list[str] = Field(default_factory=list)
    default_checklist: list[str] = Field(default_factory=list)
    default_payload: dict[str, Any] = Field(default_factory=dict)
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
