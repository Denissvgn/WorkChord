"""Request source schemas."""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.utils.url_policy import URLPolicyError, normalize_stored_display_url


def _normalize_optional_url(value: Optional[str]) -> Optional[str]:
    if value is None or not str(value).strip():
        return None
    try:
        return normalize_stored_display_url(value)
    except URLPolicyError as exc:
        raise ValueError(str(exc)) from exc


class RequestSourceType(str, Enum):
    """Supported lightweight request intake source types."""

    CUSTOMER = "customer"
    INTERNAL = "internal"
    SUPPORT = "support"
    EMAIL = "email"
    WEB = "web"
    IMPORT = "import"


class RequestSourceTargetType(str, Enum):
    """Supported request-source link target types."""

    TASK = "task"
    PROJECT = "project"
    TRIAGE_ITEM = "triage_item"


class RequestSourceCreate(BaseModel):
    """Schema for creating a request source."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    source_type: RequestSourceType
    source_name: Optional[str] = Field(default=None, max_length=255)
    source_url: Optional[str] = Field(default=None, max_length=1000)
    external_key: Optional[str] = Field(default=None, max_length=255)
    priority_hint: Optional[int] = Field(default=None, ge=1, le=10)

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)


class RequestSourceUpdate(BaseModel):
    """Schema for updating a request source."""

    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = None
    source_type: Optional[RequestSourceType] = None
    source_name: Optional[str] = Field(default=None, max_length=255)
    source_url: Optional[str] = Field(default=None, max_length=1000)
    external_key: Optional[str] = Field(default=None, max_length=255)
    priority_hint: Optional[int] = Field(default=None, ge=1, le=10)

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)


class RequestSourceResponse(BaseModel):
    """Schema for request source responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    source_type: str
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    external_key: Optional[str] = None
    priority_hint: Optional[int] = None
    created_at: datetime


class RequestSourceLinkCreate(BaseModel):
    """Schema for linking one request source to one target."""

    model_config = ConfigDict(extra="forbid")

    request_source_id: int
    triage_item_id: Optional[int] = None
    task_id: Optional[int] = None
    project_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_single_target(self):
        """Require exactly one target entity."""
        target_count = sum(
            value is not None
            for value in (self.triage_item_id, self.task_id, self.project_id)
        )
        if target_count != 1:
            raise ValueError("Exactly one link target must be provided")
        return self


class RequestSourceLinkResponse(BaseModel):
    """Schema for request source link responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    request_source_id: int
    triage_item_id: Optional[int] = None
    task_id: Optional[int] = None
    project_id: Optional[int] = None
    created_at: datetime


class RequestSourceLinkCreateRequest(BaseModel):
    """API request for linking an existing or new request source to a target."""

    model_config = ConfigDict(extra="forbid")

    target_type: RequestSourceTargetType
    target_id: int
    request_source_id: Optional[int] = None
    request_source: Optional[RequestSourceCreate] = None

    @model_validator(mode="after")
    def validate_source_choice(self):
        """Require exactly one source input."""
        has_source_id = self.request_source_id is not None
        has_source_payload = self.request_source is not None
        if has_source_id == has_source_payload:
            raise ValueError("Set exactly one of request_source_id or request_source")
        return self


class RequestSourceLinkWithSourceResponse(RequestSourceLinkResponse):
    """Request-source link response with embedded source details."""

    request_source: RequestSourceResponse
