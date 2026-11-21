"""Resolve local working dates from the annual records explicitly selected by an owner."""

from datetime import date, timedelta
from functools import cached_property
import math

from app.models.calendar import Calendar


def rule_signature(calendar: Calendar) -> tuple:
    return (
        calendar.year,
        calendar.timezone,
        calendar.nominal_day_hours,
        tuple(sorted(calendar.holidays or [])),
        tuple(sorted(calendar.weekend_days or [])),
        tuple(sorted(calendar.short_days or [])),
    )


class YearRules:
    """Indexed working rules for one annual record within a single operation."""

    def __init__(self, row: Calendar):
        self.year = row.year
        self.nominal = row.nominal_day_hours
        self.holidays = frozenset(row.holidays or ())
        self.weekends = frozenset(row.weekend_days or ())
        self.shortened = frozenset(row.short_days or ())
        self.signature = rule_signature(row)

    def kind(self, day: date) -> str:
        if day.isoformat() in self.holidays:
            return "holiday"
        if day.weekday() in self.weekends:
            return "weekend"
        return "working"

    def hours(self, day: date) -> float:
        if self.kind(day) != "working":
            return 0.0
        return max(0.0, self.nominal - (day.isoformat() in self.shortened))

    @cached_property
    def cumulative(self):
        """Pay for at most 366 dated lookups once, even across many long commitments."""
        first = date(self.year, 1, 1)
        end = date(self.year, 12, 31)
        hours, days = [0.0], [0]
        for offset in range((end - first).days + 1):
            value = self.hours(first + timedelta(days=offset))
            hours.append(hours[-1] + value)
            days.append(days[-1] + int(value > 0))
        return hours, days

    def period_totals(self, start: date, end: date):
        first = date(self.year, 1, 1)
        left, right = (start - first).days, (end - first).days + 1
        hours, days = self.cumulative
        return hours[right] - hours[left], days[right] - days[left]


class AnnualCalendars:
    """A primary calendar and explicitly selected years in the owner's local time zone."""

    def __init__(self, primary: Calendar, additional=()):
        self.primary = primary
        self.by_year: dict[int, Calendar] = {primary.year: primary}
        invalid = set()
        for row in additional:
            if row.year in self.by_year or row.timezone != primary.timezone:
                invalid.add(row.year)
            else:
                self.by_year[row.year] = row
        for year in invalid:
            self.by_year.pop(year, None)
        self.by_year = {
            y: row
            for y, row in self.by_year.items()
            if row.nominal_day_hours is not None
            and math.isfinite(row.nominal_day_hours)
            and row.nominal_day_hours > 0
        }
        self.rules = {year: YearRules(row) for year, row in self.by_year.items()}

    @classmethod
    def for_iteration(cls, iteration):
        return cls(iteration.calendar, iteration.additional_calendars)

    def missing_years(self, start: date, end: date) -> list[int]:
        return [year for year in range(start.year, end.year + 1) if year not in self.by_year]

    def signature(self) -> list[dict]:
        """Stable JSON-native inputs for both planning and routing evidence hashes."""
        return [
            {
                "calendar_id": self.by_year[year].id,
                "year": year,
                "timezone": self.by_year[year].timezone,
                "nominal_day_hours": rule.nominal,
                "holidays": sorted(rule.holidays),
                "weekend_days": sorted(rule.weekends),
                "short_days": sorted(rule.shortened),
            }
            for year, rule in sorted(self.rules.items())
        ]

    def replaced_years(self, updated) -> set[int]:
        return {
            year
            for year, row in self.by_year.items()
            if year not in updated.by_year
            or row.id != updated.by_year[year].id
            or self.rules[year].signature != updated.rules[year].signature
        }

    def hours(self, day: date) -> float | None:
        rule = self.rules.get(day.year)
        return rule.hours(day) if rule is not None else None

    def dated_rules(self, start: date, end: date):
        for year, rule in sorted(self.rules.items()):
            left, right = max(start, date(year, 1, 1)), min(end, date(year, 12, 31))
            for offset in range((right - left).days + 1):
                yield left + timedelta(days=offset), rule

    def period_totals(self, start: date, end: date):
        if self.missing_years(start, end):
            return None
        hours, days = 0.0, 0
        for year in range(start.year, end.year + 1):
            left, right = max(start, date(year, 1, 1)), min(end, date(year, 12, 31))
            h, n = self.rules[year].period_totals(left, right)
            hours += h
            days += n
        return hours, days

    def working_dates(self, start: date, end: date) -> list[date]:
        return [day for day, rule in self.dated_rules(start, end) if rule.kind(day) == "working"]


def task_uses_years(task, years) -> bool:
    windows = [
        (task.start_date, task.end_date),
        (task.baseline_start_date, task.baseline_end_date),
        (task.actual_start_date, task.actual_end_date),
    ]
    complete = [(start, end) for start, end in windows if start and end and start <= end]
    if any(day and day.year in years for window in windows for day in window):
        return True
    return not complete or any(start.year <= year <= end.year for start, end in complete for year in years)


def issued_coordinates(issued):
    return ", ".join(
        f"{task_id} ({', '.join(str(row.id) for row in assignments)})"
        for task_id, assignments in sorted(issued.items())
    )


async def reserve_iteration_annuals(db, iteration_id, data, tasks):
    """A selection edits planning rules only. Refuse replacing a rule an issued task might still use."""
    from app.commands import PlanningConflict
    from app.services.iteration_service import IterationService
    from app.services.execution_planning_window import live_assignments

    fields = set(getattr(data, "model_fields_set", ())) - {"expected_revisions"}
    if not fields.intersection({"additional_calendar_ids", "calendar_id"}):
        return False
    service = IterationService(db)
    iteration = await service.get_by_id(iteration_id)
    old = AnnualCalendars.for_iteration(iteration)
    primary, selected = await service.changed_calendar_selection(iteration, data)
    new = AnnualCalendars(primary, selected)
    replaced = old.replaced_years(new)
    if replaced:
        issued = await live_assignments(
            db, [task.id for task in tasks if task_uses_years(task, replaced)], lock=True
        )
        if issued:
            raise PlanningConflict(
                "annual_calendar_change_in_use",
                "Existing annual rules are used by issued work. Finish or reconcile these task (assignment) IDs first: "
                + issued_coordinates(issued),
            )
    if fields == {"additional_calendar_ids"}:
        return True
    if old.signature() != new.signature():
        # The ordinary mixed/primary mutation reserves every nonclosed task. Do
        # not obsolete an issued fence, even when its own year's rules match.
        issued = await live_assignments(db, [task.id for task in tasks], lock=True)
        if issued:
            raise PlanningConflict(
                "annual_calendar_change_in_use",
                "This combined or primary-calendar edit would reserve issued work. "
                "Submit additional years separately from a cutoff extension, or finish the affected "
                "assignments before changing the primary calendar. Task (assignment) IDs: "
                + issued_coordinates(issued),
            )
    return False
