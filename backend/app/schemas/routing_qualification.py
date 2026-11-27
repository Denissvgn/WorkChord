"""Contracts for the deployment's governed qualification key registry.

A declared key extends the vocabulary that catalog entries and task routing
requirements may name. The built-in routing skill keys stay fixed in code and
are listed beside the registry, never stored in it.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.agent_routing import PositiveRevision, RoutingKey


QualificationKeyState = Literal["active", "retired"]
QualificationKeyAction = Literal["declare", "revise", "retire"]
MAX_QUALIFICATION_KEY_LABEL = 255
MAX_QUALIFICATION_KEY_DESCRIPTION = 2_000
MAX_QUALIFICATION_KEY_USAGE_ITEMS = 50


class _RegistryModel(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


def _strip_text(value: str | None, *, label: str, allow_empty: bool) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized and not allow_empty:
        raise ValueError(f"{label} must not be blank")
    if any(ord(character) < 32 and character not in "\n\t" for character in normalized):
        raise ValueError(f"{label} must not contain control characters")
    return normalized or None


class RoutingQualificationKeyDeclare(_RegistryModel):
    """Declare a new key, or bring back a retired one under the same name."""

    key: RoutingKey
    label: str = Field(..., min_length=1, max_length=MAX_QUALIFICATION_KEY_LABEL)
    description: str | None = Field(default=None, max_length=MAX_QUALIFICATION_KEY_DESCRIPTION)

    @field_validator("key", mode="before")
    @classmethod
    def normalize_key(cls, value: object) -> object:
        return value.strip().lower() if isinstance(value, str) else value

    @field_validator("label")
    @classmethod
    def strip_label(cls, value: str) -> str:
        return _strip_text(value, label="label", allow_empty=False)  # type: ignore[return-value]

    @field_validator("description")
    @classmethod
    def strip_description(cls, value: str | None) -> str | None:
        return _strip_text(value, label="description", allow_empty=True)


class RoutingQualificationKeyRevise(_RegistryModel):
    """Change an active key's label or description; the key itself never changes."""

    expected_revision: PositiveRevision
    label: str | None = Field(default=None, min_length=1, max_length=MAX_QUALIFICATION_KEY_LABEL)
    description: str | None = Field(default=None, max_length=MAX_QUALIFICATION_KEY_DESCRIPTION)

    @field_validator("label")
    @classmethod
    def strip_label(cls, value: str | None) -> str | None:
        return _strip_text(value, label="label", allow_empty=False)

    @field_validator("description")
    @classmethod
    def strip_description(cls, value: str | None) -> str | None:
        return _strip_text(value, label="description", allow_empty=True)

    @model_validator(mode="after")
    def require_change(self) -> "RoutingQualificationKeyRevise":
        if "label" in self.model_fields_set and self.label is None:
            raise ValueError("label cannot be null")
        if not self.model_fields_set.intersection({"label", "description"}):
            raise ValueError("At least one of label or description must be revised")
        return self


class RoutingQualificationKeyRetire(_RegistryModel):
    """Retire an active key that no catalog entry or current task requirement names."""

    expected_revision: PositiveRevision


class RoutingQualificationKeyResponse(_RegistryModel):
    """The current state of one declared key."""

    id: int
    key: str
    label: str
    description: str | None = None
    state: QualificationKeyState
    revision: PositiveRevision
    created_at: datetime
    updated_at: datetime
    retired_at: datetime | None = None


class RoutingQualificationKeyRevisionResponse(_RegistryModel):
    """One append-only change to a declared key, with its reason."""

    revision: PositiveRevision
    action: QualificationKeyAction
    state: QualificationKeyState
    label: str
    description: str | None = None
    reason: str
    actor_type: str
    actor_id: int | None = None
    correlation_id: str | None = None
    created_at: datetime


class QualificationKeyCatalogReference(_RegistryModel):
    """A catalog entry that holds the key."""

    id: int
    key: str
    enabled: bool


class QualificationKeyCalibrationReference(_RegistryModel):
    """A calibration contract whose current terms name the key."""

    key: str
    state: Literal["submitted", "approved"]


class RoutingQualificationKeyUsage(_RegistryModel):
    """Catalog entries, calibration contracts and tasks whose current routing assessment name the key."""

    catalog_entries: list[QualificationKeyCatalogReference] = Field(
        default_factory=list,
        max_length=MAX_QUALIFICATION_KEY_USAGE_ITEMS,
    )
    task_ids: list[int] = Field(default_factory=list, max_length=MAX_QUALIFICATION_KEY_USAGE_ITEMS)
    catalog_entries_omitted: int = Field(default=0, ge=0)
    task_ids_omitted: int = Field(default=0, ge=0)
    calibration_contracts: list[QualificationKeyCalibrationReference] = Field(
        default_factory=list,
        max_length=MAX_QUALIFICATION_KEY_USAGE_ITEMS,
    )
    calibration_contracts_omitted: int = Field(default=0, ge=0)

    @property
    def in_use(self) -> bool:
        return bool(
            self.catalog_entries
            or self.task_ids
            or self.catalog_entries_omitted
            or self.task_ids_omitted
            or self.calibration_contracts
            or self.calibration_contracts_omitted
        )


class RoutingQualificationKeyDetail(RoutingQualificationKeyResponse):
    """One key with its revision history and current usage."""

    revisions: list[RoutingQualificationKeyRevisionResponse] = Field(default_factory=list)
    usage: RoutingQualificationKeyUsage


class RoutingQualificationKeyRegistryResponse(_RegistryModel):
    """The built-in keys routing always accepts, and the deployment's declared keys."""

    builtin_keys: list[str]
    keys: list[RoutingQualificationKeyResponse]
