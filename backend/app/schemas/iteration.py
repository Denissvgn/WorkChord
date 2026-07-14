"""Iteration schemas."""
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class IterationCreate(BaseModel):
    """Schema for creating an iteration."""
    name: str = Field(..., min_length=1, max_length=255)
    calendar_id: Optional[int] = None
    project_id: Optional[int] = None
    start_date: date
    end_date: date
    manager_email: Optional[str] = Field(default=None, max_length=255)


class IterationUpdate(BaseModel):
    """Schema for updating an iteration."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    calendar_id: Optional[int] = None
    project_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    manager_email: Optional[str] = Field(default=None, max_length=255)


class IterationSeriesStop(BaseModel):
    """Stop rule for generating a back-to-back iteration series."""
    mode: Literal["count", "until_date"]
    count: Optional[int] = Field(default=None, ge=1, le=100)
    until_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_stop_rule(self) -> "IterationSeriesStop":
        """Ensure the stop rule carries the field required by its mode."""
        if self.mode == "count" and self.count is None:
            raise ValueError("count is required when mode is 'count'")
        if self.mode == "until_date" and self.until_date is None:
            raise ValueError("until_date is required when mode is 'until_date'")
        return self


class IterationSeriesCreate(BaseModel):
    """Schema for creating multiple back-to-back iterations."""
    base_name: str = Field(..., min_length=1, max_length=255)
    calendar_id: Optional[int] = None
    project_id: Optional[int] = None
    start_date: date
    duration_days: int = Field(default=14, ge=1, le=366)
    stop: IterationSeriesStop
    manager_email: Optional[str] = Field(default=None, max_length=255)


class IterationProjectSummary(BaseModel):
    """Compact project identity embedded in iteration responses."""
    id: int
    name: str
    status: str
    health: str

    class Config:
        from_attributes = True


class IterationResponse(BaseModel):
    """Schema for iteration response."""
    id: int
    name: str
    calendar_id: int
    project_id: Optional[int] = None
    project: Optional[IterationProjectSummary] = None
    start_date: date
    end_date: date
    manager_email: Optional[str] = None
    working_days: int = 0  # Computed field

    class Config:
        from_attributes = True


class IterationSeriesResponse(BaseModel):
    """Response returned after creating an iteration series."""
    iterations: list[IterationResponse]


class IterationSummary(BaseModel):
    """Summary statistics for an iteration."""
    id: int
    name: str
    project_id: Optional[int] = None
    project: Optional[IterationProjectSummary] = None
    start_date: date
    end_date: date
    working_days: int
    total_tasks: int
    completed_tasks: int
    total_effort_days: float
    team_capacity_days: float
    overdue_tasks_count: int
