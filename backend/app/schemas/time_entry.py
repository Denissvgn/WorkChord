"""Bounded minute/date contracts with explicit correction versions."""

from datetime import date, datetime
from uuid import UUID
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import re

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator


class TimeValues(BaseModel):
    model_config = ConfigDict(extra="forbid")
    work_date: date
    timezone: str = Field(min_length=1, max_length=64)
    minutes: StrictInt = Field(ge=1, le=1440)
    note: str = Field(default="", max_length=2000)

    @field_validator("work_date", mode="before")
    @classmethod
    def local_date_only(cls, value):
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("Use an explicit local work date in YYYY-MM-DD form")
        return value

    @field_validator("timezone")
    @classmethod
    def valid_timezone(cls, value):
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise ValueError("Use a valid IANA timezone, such as Europe/Madrid or UTC") from exc
        return value


class TimeEntryCreate(TimeValues):
    project_id: StrictInt = Field(ge=1)
    task_id: StrictInt | None = Field(default=None, ge=1)
    request_id: UUID


class CorrectionReason(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reason: str = Field(min_length=1, max_length=1000)

    @field_validator("reason")
    @classmethod
    def nonempty_reason(cls, value):
        if not value.strip():
            raise ValueError("Explain the correction")
        return value.strip()


class TimeEntryCorrection(TimeValues, CorrectionReason):
    expected_version: StrictInt = Field(ge=1)


class TimeEntryVoid(CorrectionReason):
    expected_version: StrictInt = Field(ge=1)


class TimeEntryResponse(TimeValues):
    id: int
    project_id: int
    task_id: int | None
    task_title: str | None
    principal_id: int
    version: int
    voided: bool
    created_at: datetime
    updated_at: datetime


class TimeEntryPage(BaseModel):
    items: list[TimeEntryResponse]
    has_more: bool
    next_after_id: int | None
    upper_id: int
    consistency: str = "live_bounded_id_order"


class TimeRevisionResponse(TimeValues):
    version: int
    principal_id: int
    reason: str
    voided: bool
    created_at: datetime


class TimeRevisionPage(BaseModel):
    items: list[TimeRevisionResponse]
    has_more: bool
    next_after_version: int | None


class TimeEntryCapabilities(BaseModel):
    schema_version: Literal[1] = 1
    enabled: bool
    human_identity_required: bool
    units: Literal["whole_minutes"] = "whole_minutes"
    privacy: Literal["private_entries_manager_totals"] = "private_entries_manager_totals"
