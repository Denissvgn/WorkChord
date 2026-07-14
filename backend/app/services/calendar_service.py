"""Calendar service with business logic."""
import csv
from collections.abc import Iterable
from datetime import date, timedelta
from io import StringIO
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.schemas.calendar import (
    CalendarCreate,
    CalendarImportError,
    CalendarImportRequest,
    CalendarImportResponse,
    CalendarUpdate,
    WorkingDaysResponse,
)


DEFAULT_CALENDAR_NAME = "Work Calendar"

PUBLIC_HOLIDAY_FIXED_DATES: dict[str, list[tuple[int, int, str]]] = {
    "US": [
        (1, 1, "New Year's Day"),
        (6, 19, "Juneteenth"),
        (7, 4, "Independence Day"),
        (11, 11, "Veterans Day"),
        (12, 25, "Christmas Day"),
    ],
    "ES": [
        (1, 1, "New Year's Day"),
        (1, 6, "Epiphany"),
        (5, 1, "Labour Day"),
        (8, 15, "Assumption of Mary"),
        (10, 12, "National Day of Spain"),
        (11, 1, "All Saints' Day"),
        (12, 6, "Constitution Day"),
        (12, 8, "Immaculate Conception"),
        (12, 25, "Christmas Day"),
    ],
    "RU": [
        (1, 1, "New Year Holiday"),
        (1, 2, "New Year Holiday"),
        (1, 3, "New Year Holiday"),
        (1, 4, "New Year Holiday"),
        (1, 5, "New Year Holiday"),
        (1, 6, "New Year Holiday"),
        (1, 7, "Orthodox Christmas"),
        (2, 23, "Defender of the Fatherland Day"),
        (3, 8, "International Women's Day"),
        (5, 1, "Spring and Labour Day"),
        (5, 9, "Victory Day"),
        (6, 12, "Russia Day"),
        (11, 4, "Unity Day"),
    ],
}


class CalendarService:
    """Service for calendar operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Calendar]:
        """Get all calendars."""
        await self.get_or_create_default()
        result = await self.db.execute(select(Calendar).order_by(Calendar.year.desc()))
        return result.scalars().all()

    async def get_or_create_default(self, *, commit: bool = True) -> Calendar:
        """Return the default calendar, optionally deferring creation commit."""
        result = await self.db.execute(select(Calendar).order_by(Calendar.id).limit(1))
        calendar = result.scalar_one_or_none()
        if calendar:
            return calendar

        current_year = date.today().year
        calendar = Calendar(
            name=f"{DEFAULT_CALENDAR_NAME} {current_year}",
            year=current_year,
            holidays=[],
            weekend_days=[5, 6],
            short_days=[],
        )
        self.db.add(calendar)
        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(calendar)
        return calendar

    async def get_by_id(self, calendar_id: int) -> Calendar | None:
        """Get calendar by ID."""
        result = await self.db.execute(
            select(Calendar).where(Calendar.id == calendar_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: CalendarCreate) -> Calendar:
        """Create a new calendar."""
        calendar = Calendar(
            name=data.name,
            year=data.year,
            holidays=data.holidays,
            weekend_days=data.weekend_days,
        )
        self.db.add(calendar)
        await self.db.commit()
        await self.db.refresh(calendar)
        return calendar

    async def update(self, calendar_id: int, data: CalendarUpdate) -> Calendar | None:
        """Update an existing calendar."""
        calendar = await self.get_by_id(calendar_id)
        if not calendar:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(calendar, field, value)

        await self.db.commit()
        await self.db.refresh(calendar)
        return calendar

    async def delete(self, calendar_id: int) -> bool:
        """Delete a calendar."""
        calendar = await self.get_by_id(calendar_id)
        if not calendar:
            return False

        total_result = await self.db.execute(select(func.count(Calendar.id)))
        if (total_result.scalar_one() or 0) <= 1:
            raise ValueError("The persistent work calendar cannot be deleted")

        usage_result = await self.db.execute(
            select(func.count(Iteration.id)).where(Iteration.calendar_id == calendar_id)
        )
        if (usage_result.scalar_one() or 0) > 0:
            raise ValueError("Calendar is used by iterations and cannot be deleted")

        await self.db.delete(calendar)
        await self.db.commit()
        return True

    def _public_holidays(self, country: str, year: int) -> list[str]:
        """Return deterministic built-in public holiday dates for a country/year."""
        country_key = country.strip().upper()
        definitions = PUBLIC_HOLIDAY_FIXED_DATES.get(country_key)
        if not definitions:
            supported = ", ".join(sorted(PUBLIC_HOLIDAY_FIXED_DATES))
            raise ValueError(f"Unsupported public holiday country '{country}'. Supported: {supported}")
        return [date(year, month, day).isoformat() for month, day, _name in definitions]

    def _parse_holiday_csv(self, csv_text: str | None) -> tuple[list[str], list[CalendarImportError]]:
        """Parse holiday CSV rows with a required date column."""
        if not csv_text or not csv_text.strip():
            raise ValueError("csv_text is required for CSV imports")

        reader = csv.DictReader(StringIO(csv_text))
        if not reader.fieldnames or "date" not in {name.strip() for name in reader.fieldnames}:
            raise ValueError("CSV must include a date column")

        dates: list[str] = []
        errors: list[CalendarImportError] = []
        for row_number, row in enumerate(reader, start=2):
            raw_date = (row.get("date") or "").strip()
            if not raw_date:
                errors.append(CalendarImportError(row=row_number, message="Missing date"))
                continue
            try:
                dates.append(date.fromisoformat(raw_date).isoformat())
            except ValueError:
                errors.append(CalendarImportError(row=row_number, message=f"Invalid date '{raw_date}'"))
        return dates, errors

    def _merge_holidays(
        self,
        existing_holidays: Iterable[str],
        imported_holidays: Iterable[str],
    ) -> tuple[list[str], int, int]:
        """Merge imported holiday dates into existing holiday strings."""
        existing = {date.fromisoformat(day).isoformat() for day in existing_holidays}
        imported_count = 0
        skipped_count = 0

        for holiday in imported_holidays:
            normalized = date.fromisoformat(holiday).isoformat()
            if normalized in existing:
                skipped_count += 1
            else:
                existing.add(normalized)
                imported_count += 1

        return sorted(existing), imported_count, skipped_count

    async def import_holidays(
        self,
        calendar_id: int,
        data: CalendarImportRequest,
    ) -> CalendarImportResponse | None:
        """Import public or CSV holiday dates into a calendar."""
        calendar = await self.get_by_id(calendar_id)
        if not calendar:
            return None

        source = data.source.strip().lower()
        errors: list[CalendarImportError] = []
        if source == "public":
            if not data.country:
                raise ValueError("country is required for public holiday imports")
            year = data.year or calendar.year
            imported_dates = self._public_holidays(data.country, year)
        elif source == "csv":
            imported_dates, errors = self._parse_holiday_csv(data.csv_text)
        else:
            raise ValueError("source must be 'public' or 'csv'")

        merged, imported_count, duplicate_count = self._merge_holidays(
            calendar.holidays or [],
            imported_dates,
        )
        calendar.holidays = merged
        await self.db.commit()
        await self.db.refresh(calendar)

        return CalendarImportResponse(
            calendar=calendar,
            imported_count=imported_count,
            skipped_count=duplicate_count + len(errors),
            errors=errors,
        )

    def calculate_working_days(
        self,
        calendar: Calendar,
        start_date: date,
        end_date: date
    ) -> WorkingDaysResponse:
        """Calculate working days for a period."""
        holidays_set = set(date.fromisoformat(d) for d in calendar.holidays)
        weekend_days_set = set(calendar.weekend_days)

        current = start_date
        total_days = 0
        working_days = 0
        holidays_in_period: list[date] = []
        weekends_in_period: list[date] = []

        while current <= end_date:
            total_days += 1
            weekday = current.weekday()

            if current in holidays_set:
                holidays_in_period.append(current)
            elif weekday in weekend_days_set:
                weekends_in_period.append(current)
            else:
                working_days += 1

            current += timedelta(days=1)

        return WorkingDaysResponse(
            start_date=start_date,
            end_date=end_date,
            total_days=total_days,
            working_days=working_days,
            holidays=holidays_in_period,
            weekends=weekends_in_period,
        )

    def get_working_dates(
        self,
        calendar: Calendar,
        start_date: date,
        end_date: date
    ) -> list[date]:
        """Get list of working dates in a period."""
        holidays_set = set(date.fromisoformat(d) for d in calendar.holidays)
        weekend_days_set = set(calendar.weekend_days)

        working_dates = []
        current = start_date

        while current <= end_date:
            weekday = current.weekday()
            if current not in holidays_set and weekday not in weekend_days_set:
                working_dates.append(current)
            current += timedelta(days=1)

        return working_dates
