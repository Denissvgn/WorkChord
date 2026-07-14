"""Release schemas."""
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReleaseStatus(str, Enum):
    """Release lifecycle independent of task status."""

    PLANNED = "planned"
    BUILDING = "building"
    SHIPPED = "shipped"
    CANCELED = "canceled"


class ReleaseTaskSummary(BaseModel):
    """Compact task identity embedded in release responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: str
    project_id: Optional[int] = None


class ReleaseCreate(BaseModel):
    """Schema for creating a release."""

    model_config = ConfigDict(extra="forbid")

    project_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ReleaseStatus = ReleaseStatus.PLANNED
    target_date: Optional[date] = None
    shipped_at: Optional[datetime] = None
    version: Optional[str] = Field(default=None, max_length=100)
    environment: Optional[str] = Field(default=None, max_length=100)
    task_ids: list[int] = Field(default_factory=list)


class ReleaseCreateRequest(BaseModel):
    """API request for creating a project-scoped release."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ReleaseStatus = ReleaseStatus.PLANNED
    target_date: Optional[date] = None
    shipped_at: Optional[datetime] = None
    version: Optional[str] = Field(default=None, max_length=100)
    environment: Optional[str] = Field(default=None, max_length=100)
    task_ids: list[int] = Field(default_factory=list)


class ReleaseUpdate(BaseModel):
    """Schema for updating a release."""

    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ReleaseStatus] = None
    target_date: Optional[date] = None
    shipped_at: Optional[datetime] = None
    version: Optional[str] = Field(default=None, max_length=100)
    environment: Optional[str] = Field(default=None, max_length=100)
    task_ids: Optional[list[int]] = None


class ReleaseUpdateRequest(ReleaseUpdate):
    """API request for partially updating a release."""


class ReleaseResponse(BaseModel):
    """Schema for release responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    description: Optional[str] = None
    status: str
    target_date: Optional[date] = None
    shipped_at: Optional[datetime] = None
    version: Optional[str] = None
    environment: Optional[str] = None
    task_ids: list[int] = Field(default_factory=list)
    tasks: list[ReleaseTaskSummary] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
