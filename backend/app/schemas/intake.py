"""Schemas for controlled external intake endpoints."""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class WebIntakeRequest(BaseModel):
    """External web/form intake payload."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    source: Optional[str] = Field(default="web", max_length=100)
    source_url: Optional[str] = Field(default=None, max_length=1000)
    external_key: Optional[str] = Field(default=None, max_length=255)
    priority_hint: Optional[int] = Field(default=None, ge=1, le=10)
    assignee_hint: Optional[str] = Field(default=None, max_length=255)
    project_hint_id: Optional[int] = None
    iteration_hint_id: Optional[int] = None
    labels: list[str] = Field(default_factory=list)
    metadata_json: dict[str, Any] = Field(default_factory=dict)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        """Reject blank titles after trimming."""
        title = value.strip()
        if not title:
            raise ValueError("title must not be blank")
        return title

    @field_validator("description", "source_url", "external_key", "assignee_hint")
    @classmethod
    def normalize_optional_text(cls, value: Optional[str]) -> Optional[str]:
        """Trim optional text fields."""
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @field_validator("source")
    @classmethod
    def normalize_source(cls, value: Optional[str]) -> str:
        """Default blank source values to web."""
        if value is None:
            return "web"
        source = value.strip()
        return source or "web"

    @field_validator("labels")
    @classmethod
    def normalize_labels(cls, value: list[str]) -> list[str]:
        """Trim labels and remove duplicates while preserving order."""
        labels: list[str] = []
        seen: set[str] = set()
        for raw_label in value or []:
            label = str(raw_label).strip()
            if label and label not in seen:
                labels.append(label)
                seen.add(label)
        return labels

    @model_validator(mode="after")
    def validate_metadata(self):
        """Keep metadata JSON object-shaped for predictable storage."""
        if not isinstance(self.metadata_json, dict):
            raise ValueError("metadata_json must be a JSON object")
        return self


class WebIntakeRateLimitInfo(BaseModel):
    """Rate-limit details returned on rejection."""

    retry_after_seconds: int
    limit: int
    window_seconds: int
    client_ip: str
    reset_at: datetime
