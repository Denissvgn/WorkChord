"""Governed label taxonomy schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


HEX_COLOR_PATTERN = r"^#[0-9A-Fa-f]{6}$"
GROUP_KEY_PATTERN = r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
LABEL_SLUG_PATTERN = r"^[a-z0-9](?:[a-z0-9:-]*[a-z0-9])?$"


class LabelGroupCreate(BaseModel):
    """Schema for creating a governed label group."""
    model_config = ConfigDict(extra="forbid")

    key: str = Field(..., min_length=1, max_length=100, pattern=GROUP_KEY_PATTERN)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    color: str = Field(default="#64748b", pattern=HEX_COLOR_PATTERN)
    is_active: bool = True
    sort_order: int = 0


class LabelGroupUpdate(BaseModel):
    """Schema for updating a governed label group."""
    model_config = ConfigDict(extra="forbid")

    key: Optional[str] = Field(default=None, min_length=1, max_length=100, pattern=GROUP_KEY_PATTERN)
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    color: Optional[str] = Field(default=None, pattern=HEX_COLOR_PATTERN)
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class LabelGroupBrief(BaseModel):
    """Brief label group shape embedded in label responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str
    name: str
    color: str
    is_active: bool


class LabelCreate(BaseModel):
    """Schema for creating a governed label."""
    model_config = ConfigDict(extra="forbid")

    slug: str = Field(..., min_length=1, max_length=100, pattern=LABEL_SLUG_PATTERN)
    name: str = Field(..., min_length=1, max_length=255)
    group_id: int
    description: Optional[str] = None
    color: str = Field(default="#64748b", pattern=HEX_COLOR_PATTERN)
    is_active: bool = True
    sort_order: int = 0


class LabelUpdate(BaseModel):
    """Schema for updating a governed label."""
    model_config = ConfigDict(extra="forbid")

    slug: Optional[str] = Field(default=None, min_length=1, max_length=100, pattern=LABEL_SLUG_PATTERN)
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    group_id: Optional[int] = None
    description: Optional[str] = None
    color: Optional[str] = Field(default=None, pattern=HEX_COLOR_PATTERN)
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class LabelResponse(BaseModel):
    """Schema for governed label responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    group_id: int
    group: Optional[LabelGroupBrief] = None
    description: Optional[str] = None
    color: str
    is_active: bool
    sort_order: int
    seed_key: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class LabelGroupResponse(BaseModel):
    """Schema for governed label group responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str
    name: str
    description: Optional[str] = None
    color: str
    is_active: bool
    sort_order: int
    seed_key: Optional[str] = None
    labels: list[LabelResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
