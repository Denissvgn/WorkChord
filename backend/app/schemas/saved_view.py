"""Saved view schemas and filter payload validation primitives."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SavedViewType(str, Enum):
    """Surface that a saved view applies to."""
    TASKS = "tasks"
    PROJECTS = "projects"
    TRIAGE = "triage"


class SavedViewScope(str, Enum):
    """Visibility scope for a saved view."""
    PERSONAL = "personal"
    SHARED = "shared"
    SYSTEM = "system"


class SavedViewCreate(BaseModel):
    """Schema for creating a saved view."""
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    view_type: SavedViewType
    scope: SavedViewScope = SavedViewScope.PERSONAL
    filters_json: dict[str, Any] = Field(default_factory=dict)
    sort_json: dict[str, Any] = Field(default_factory=dict)
    columns_json: dict[str, Any] = Field(default_factory=dict)
    created_by_session_id: Optional[int] = None
    schema_version: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def require_creator_for_personal_scope(self) -> "SavedViewCreate":
        """Personal views must be associated with a user session."""
        if self.scope == SavedViewScope.PERSONAL and self.created_by_session_id is None:
            raise ValueError("Personal saved views require created_by_session_id")
        return self


class SavedViewUpdate(BaseModel):
    """Schema for updating a saved view."""
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    view_type: Optional[SavedViewType] = None
    scope: Optional[SavedViewScope] = None
    filters_json: Optional[dict[str, Any]] = None
    sort_json: Optional[dict[str, Any]] = None
    columns_json: Optional[dict[str, Any]] = None
    created_by_session_id: Optional[int] = None
    schema_version: Optional[int] = Field(default=None, ge=1)

    @model_validator(mode="after")
    def require_creator_when_setting_personal_scope(self) -> "SavedViewUpdate":
        """Changing a view to personal scope must include a creator session."""
        if self.scope == SavedViewScope.PERSONAL and self.created_by_session_id is None:
            raise ValueError("Personal saved views require created_by_session_id")
        return self


class SavedViewCreateRequest(BaseModel):
    """Public API payload for creating a saved view."""
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    view_type: SavedViewType
    scope: SavedViewScope = SavedViewScope.PERSONAL
    filters_json: Any = Field(default_factory=dict)
    sort_json: Any = Field(default_factory=dict)
    columns_json: Any = Field(default_factory=dict)
    schema_version: int = Field(default=1, ge=1)


class SavedViewUpdateRequest(BaseModel):
    """Public API payload for updating a saved view."""
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    view_type: Optional[SavedViewType] = None
    scope: Optional[SavedViewScope] = None
    filters_json: Any = None
    sort_json: Any = None
    columns_json: Any = None
    schema_version: Optional[int] = Field(default=None, ge=1)


class SavedViewDuplicateRequest(BaseModel):
    """Public API payload for duplicating an existing saved view."""
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    scope: SavedViewScope = SavedViewScope.PERSONAL


class SavedViewResponse(BaseModel):
    """Schema for saved view responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    seed_key: Optional[str] = None
    view_type: str
    scope: str
    filters_json: dict[str, Any] = Field(default_factory=dict)
    sort_json: dict[str, Any] = Field(default_factory=dict)
    columns_json: dict[str, Any] = Field(default_factory=dict)
    created_by_session_id: Optional[int] = None
    schema_version: int
    is_valid: bool = True
    invalid_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SavedViewDashboardCardResponse(BaseModel):
    """Dashboard card summary backed by a saved view."""

    saved_view_id: int
    seed_key: str
    name: str
    description: Optional[str] = None
    view_type: str
    scope: str
    count: int
    target_path: str
    is_valid: bool = True
    invalid_reason: Optional[str] = None
