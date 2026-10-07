"""Scoped recorded coverage, distinct from current effort estimates."""

from datetime import date
from typing import Literal
from pydantic import BaseModel


class TimeReportItem(BaseModel):
    task_id: int
    task_title: str | None
    recorded_minutes: int | None
    entry_count: int
    estimate_hours: float | None
    estimate_state: Literal["known", "unknown", "unavailable"]


class TimeReportTotals(BaseModel):
    task_count: int
    tasks_with_records: int
    recorded_minutes: int | None
    project_work_minutes: int | None
    known_estimate_hours: float | None
    tasks_with_estimates: int


class TimeReportPage(BaseModel):
    project_id: int
    scope: Literal["mine", "project"]
    start: date
    end: date
    items: list[TimeReportItem]
    totals: TimeReportTotals
    has_more: bool
    next_after_id: int | None
    upper_id: int
    can_view_project_totals: bool
    consistency: str = "live_scope_totals_bounded_id_pages"
