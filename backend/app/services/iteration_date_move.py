"""Preview a proposed iteration period against each person's shared capacity.

The preview runs the real iteration update inside a rolled-back command, so it
refuses exactly what the update would refuse and observes the same revisions.
It then compares, for every person of the iteration team and every date of the
proposed period, the hours this iteration's rows would request with the hours
the person's other rows already book, in any project. Dated capacity
adjustments apply on their dates. Nothing is saved.

Bookings in iterations the caller cannot read are reported only as a total,
the same way shared person capacity reports private busy hours.
"""

from collections import defaultdict
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.authority import internal_authority
from app.commands import PlanningConflict, current_command, lock_planning, preview_command
from app.models.iteration import Iteration
from app.models.team_member import TeamMember
from app.schemas.iteration import IterationDateMoveRequest
from app.services.calendar_rules import AnnualCalendars

MAX_PROPOSED_DAYS = 366
MAX_TEAM_ROWS = 500
MAX_SHORTFALLS = 1000
TOLERANCE = .000001


def _days(start, end):
    day = start
    while day <= end:
        yield day
        day += timedelta(days=1)


def _rounded(value):
    return round(value, 4)


class IterationDateMoveService:
    """Calculate shared capacity for a proposed iteration period, then roll everything back."""

    def __init__(self, db):
        self.db = db

    @preview_command
    async def preview(self, iteration_id: int, data: IterationDateMoveRequest):
        from app.services.iteration_service import IterationService
        from app.services.planning_input_context import PlanningInputUnavailable, affected_iteration_ids

        iterations = IterationService(self.db)
        iteration = await iterations.get_by_id(iteration_id)
        if iteration is None:
            raise PlanningInputUnavailable("Iteration not found or inaccessible")
        current = self._period(iteration)
        # The same edit authorization as the update, before any shared capacity is read.
        await affected_iteration_ids(self.db, "iteration", {"iteration_id": iteration_id})
        start = data.start_date or iteration.start_date
        end = data.end_date or iteration.end_date
        if end < start:
            raise PlanningConflict("date_move_range_invalid", "The proposed end date is before the proposed start date.")
        if (end - start).days >= MAX_PROPOSED_DAYS:
            raise PlanningConflict("date_move_range_invalid",
                f"Preview a proposed period of at most {MAX_PROPOSED_DAYS} days.")
        await lock_planning(self.db)
        with internal_authority(self.db):
            rows = list((await self.db.scalars(
                select(TeamMember).where(TeamMember.iteration_id == iteration_id)
                .order_by(TeamMember.id).limit(MAX_TEAM_ROWS + 1))).all())
        if len(rows) > MAX_TEAM_ROWS:
            raise PlanningConflict("planning_scope_oversized", "This team exceeds the supported preview limit.")
        profile_rows = defaultdict(list)
        for row in rows:
            if row.profile_id is not None:
                profile_rows[row.profile_id].append(row.id)

        from app.services.capacity_service import CapacityService
        capacity = CapacityService(self.db)
        before = {profile_id: await capacity._projection(profile_id, start, end) for profile_id in sorted(profile_rows)}

        updated = await iterations.update(iteration_id, data.as_update(), commit=False)
        if updated is None:
            raise PlanningInputUnavailable("Iteration not found or inaccessible")
        state = current_command(self.db)

        profiles, shortfalls = [], []
        for profile_id in sorted(profile_rows):
            after = await capacity._projection(profile_id, start, end)
            parts = await self._row_hours(profile_id, iteration_id, start, end)
            prior = {row["date"]: row for row in before[profile_id]["days"]}
            found = []
            for day in after["days"]:
                date_value = day["date"]
                requested, others, private, bookings = parts(date_value)
                if requested <= TOLERANCE or day["allocated_hours"] is None or day["available_hours"] is None:
                    continue
                overallocated = day["allocated_hours"] - day["available_hours"]
                if overallocated <= TOLERANCE:
                    continue
                found.append({
                    "profile_id": profile_id,
                    "member_ids": profile_rows[profile_id],
                    "date": date_value,
                    "available_hours": day["available_hours"],
                    "requested_hours": _rounded(requested),
                    "booked_elsewhere_hours": _rounded(others),
                    "private_booked_hours": _rounded(private),
                    "bookings": bookings,
                    "overallocated_hours": _rounded(overallocated),
                    "shortfall_hours": _rounded(min(requested, overallocated)),
                    "current_overallocated_hours": prior[date_value]["overallocated_hours"],
                })
            profiles.append({
                "profile_id": profile_id,
                "member_ids": profile_rows[profile_id],
                "shortfall_days": len(found),
                "shortfall_hours": _rounded(sum(row["shortfall_hours"] for row in found)),
                "first_shortfall_date": found[0]["date"] if found else None,
                "calendar_uncertain": after["calendar_uncertain"],
                "missing_calendar_years": after["missing_calendar_years"],
            })
            shortfalls.extend(found)
        shortfalls.sort(key=lambda row: (row["date"], row["profile_id"]))
        return {
            "applied": False,
            "iteration_id": iteration_id,
            "current": current,
            "proposed": self._period(updated),
            "profiles": profiles,
            "shortfalls": shortfalls[:MAX_SHORTFALLS],
            "shortfalls_truncated": len(shortfalls) > MAX_SHORTFALLS,
            "max_shortfalls": MAX_SHORTFALLS,
            "unlinked_member_ids": [row.id for row in rows if row.profile_id is None],
            "expected_revisions": dict(sorted(state.iterations.items())),
            "planning_revision": state.planning_revision,
        }

    def _period(self, iteration):
        from app.services.calendar_service import CalendarService
        coverage = AnnualCalendars.for_iteration(iteration)
        working = CalendarService(self.db).calculate_working_days(coverage, iteration.start_date, iteration.end_date)
        return {
            "start_date": iteration.start_date,
            "end_date": iteration.end_date,
            "calendar_id": iteration.calendar_id,
            "additional_calendar_ids": sorted(row.id for row in iteration.additional_calendars),
            "working_days": working.working_days,
            "missing_calendar_years": working.missing_calendar_years,
        }

    async def _row_hours(self, profile_id, iteration_id, start, end):
        """Return a function giving this iteration's and the other rows' hours of one person on a date.

        Uses the same inputs as the shared person capacity: the person's calendar,
        or each row's iteration calendar, minus absences, times the row's
        percentage on that date.
        """
        from app.services.capacity_adjustments import load_dated_availability
        from app.services.capacity_service import CapacityService

        capacity = CapacityService(self.db)
        authority = self.db.info.get("authority")
        with internal_authority(self.db):
            members = list((await self.db.scalars(
                select(TeamMember).join(Iteration, TeamMember.iteration_id == Iteration.id)
                .where(TeamMember.profile_id == profile_id, Iteration.start_date <= end, Iteration.end_date >= start)
                .options(selectinload(TeamMember.iteration).selectinload(Iteration.calendar))
                .order_by(TeamMember.id))).all())
            coverages = {member.id: await capacity.coverage_for(member) for member in members}
            absences = await capacity.absence_ranges(members[0]) if members else []
        dated = await load_dated_availability(self.db, [member.id for member in members])

        def readable(member):
            return (authority is None or authority.operator or authority.local
                    or authority.allows(member.iteration.project_id, "read"))

        visible = {member.id: readable(member) for member in members}

        def parts(day):
            requested = others = private = 0.0
            bookings = defaultdict(float)
            if any(first <= day <= last for first, last in absences):
                return requested, others, private, []
            for member in members:
                if not member.iteration.start_date <= day <= member.iteration.end_date:
                    continue
                hours = (coverages[member.id].hours(day) or 0.0) * dated.percent(member, day) / 100
                if member.iteration_id == iteration_id:
                    requested += hours
                    continue
                others += hours
                if not visible[member.id]:
                    private += hours
                elif hours > TOLERANCE:
                    bookings[(member.iteration_id, member.iteration.project_id)] += hours
            return requested, others, private, [
                {"iteration_id": key[0], "project_id": key[1], "hours": _rounded(value)}
                for key, value in sorted(bookings.items())]

        return parts
