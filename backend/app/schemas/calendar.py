"""Calendar schemas."""
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CalendarCreate(BaseModel):
    """Schema for creating a calendar."""
    name: str = Field(..., min_length=1, max_length=255)
    year: int = Field(..., ge=2000, le=2100)
    holidays: list[str] = Field(default_factory=list, description="ISO date strings")
    weekend_days: list[int] = Field(default=[5, 6], description="0=Mon, 6=Sun")
    short_days: list[str] = Field(default_factory=list, description="Pre-holiday shortened days")


class CalendarUpdate(BaseModel):
    """Schema for updating a calendar."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    year: Optional[int] = Field(default=None, ge=2000, le=2100)
    holidays: Optional[list[str]] = None
    weekend_days: Optional[list[int]] = None
    short_days: Optional[list[str]] = None


class CalendarResponse(BaseModel):
    """Schema for calendar response."""
    id: int
    name: str
    year: int
    holidays: list[str]
    weekend_days: list[int]
    short_days: list[str] = []

    class Config:
        from_attributes = True


class CalendarImportError(BaseModel):
    """One calendar import row that could not be applied."""
    row: int
    message: str


class CalendarImportRequest(BaseModel):
    """Request for importing calendar holidays from a public source or CSV text."""
    source: str = Field(..., description="'public' or 'csv'")
    country: Optional[str] = Field(default=None, description="Country code for public holidays")
    year: Optional[int] = Field(default=None, ge=2000, le=2100)
    csv_text: Optional[str] = Field(default=None, description="CSV text with a date column")


class CalendarImportResponse(BaseModel):
    """Summary of imported calendar holidays."""
    calendar: CalendarResponse
    imported_count: int
    skipped_count: int
    errors: list[CalendarImportError] = Field(default_factory=list)


class WorkingDaysRequest(BaseModel):
    """Request for calculating working days."""
    start_date: date
    end_date: date


class WorkingDaysResponse(BaseModel):
    """Response with working days calculation."""
    start_date: date
    end_date: date
    total_days: int
    working_days: int
    holidays: list[date]
    weekends: list[date]


class HolidayImportRequest(BaseModel):
    """Request for importing holidays from external source."""
    source: str = Field(..., description="'internet' or 'corporate'")
    url: Optional[str] = Field(default=None, description="URL for corporate source")
    country: Optional[str] = Field(default=None, description="Country code for internet source")
    year: Optional[int] = None
