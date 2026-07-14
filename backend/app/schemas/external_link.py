"""External link schemas."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.url_policy import URLPolicyError, normalize_stored_display_url


def _normalize_optional_url(value: Optional[str]) -> Optional[str]:
    if value is None or not str(value).strip():
        return None
    try:
        return normalize_stored_display_url(value)
    except URLPolicyError as exc:
        raise ValueError(str(exc)) from exc


class ExternalLinkEntityType(str, Enum):
    """Supported internal entity types for external links."""
    TASK = "task"
    PROJECT = "project"
    RELEASE = "release"


class ExternalLinkProvider(str, Enum):
    """Supported external link providers."""
    GITHUB = "github"
    GITLAB = "gitlab"
    FIGMA = "figma"
    SENTRY = "sentry"
    CUSTOM = "custom"


class ExternalLinkFields(BaseModel):
    """Shared external link fields."""
    provider: ExternalLinkProvider
    external_key: Optional[str] = Field(default=None, max_length=255)
    url: Optional[str] = Field(default=None, max_length=1000)
    title: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, max_length=100)
    metadata_json: dict[str, Any] = Field(default_factory=dict)

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)

    @field_validator("metadata_json", mode="before")
    @classmethod
    def validate_metadata_json(cls, value):
        """Require metadata_json to be a JSON object."""
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("metadata_json must be a JSON object")
        return value


class ExternalLinkCreate(ExternalLinkFields):
    """Schema for creating a generic external link."""
    model_config = ConfigDict(extra="forbid")

    entity_type: ExternalLinkEntityType
    entity_id: int


class TaskExternalLinkCreate(ExternalLinkFields):
    """Schema for creating an external link on a task."""
    model_config = ConfigDict(extra="forbid")


class GitHubExternalLinkCreate(BaseModel):
    """Schema for manually linking a GitHub artifact to a task."""
    model_config = ConfigDict(extra="forbid")

    url: str = Field(..., min_length=1, max_length=1000)

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        normalized = _normalize_optional_url(value)
        if normalized is None:
            raise ValueError("url is required")
        return normalized


class ExternalLinkUpdate(BaseModel):
    """Schema for updating an external link."""
    model_config = ConfigDict(extra="forbid")

    provider: Optional[ExternalLinkProvider] = None
    external_key: Optional[str] = Field(default=None, max_length=255)
    url: Optional[str] = Field(default=None, max_length=1000)
    title: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, max_length=100)
    metadata_json: Optional[dict[str, Any]] = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)

    @field_validator("metadata_json", mode="before")
    @classmethod
    def validate_metadata_json(cls, value):
        """Require metadata_json updates to be JSON objects."""
        if value is None:
            raise ValueError("metadata_json must be a JSON object")
        if not isinstance(value, dict):
            raise ValueError("metadata_json must be a JSON object")
        return value


class ExternalLinkResponse(BaseModel):
    """Schema for external link responses, including synthetic legacy links."""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    entity_type: str
    entity_id: int
    provider: str
    external_key: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    is_legacy: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
