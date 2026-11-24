"""Profile-owned availability and permission-safe date capacity projections."""

from datetime import date, timedelta
from collections import defaultdict
from dataclasses import dataclass

from sqlalchemy import delete, select, update

from app.authority import AuthorityError, internal_authority
from app.commands import PlanningConflict, atomic_command, lock_iterations, lock_planning
from app.models.calendar import Calendar
from app.models.capacity import PlanningState, ProfileAbsence, ProfileAvailability
from app.models.iteration import Iteration
from app.models.team_member import TeamMember, TeamMemberProfile, Vacation
from app.services.calendar_rules import AnnualCalendars, YearRules, rule_signature as calendar_signature
from app.services.calendar_service import CalendarService


def day_hours(calendar, day):
    """Return the hours of one matching record for existing single-date callers."""
    if calendar.year != day.year:
        raise ValueError("Working date is outside the selected annual calendar")
    return YearRules(calendar).hours(day)


def agreed_calendar(coverages, year):
    """Resolve actual overlapping allocation rules, retaining ambiguity and missing coverage."""
    rows = [coverage.by_year.get(year) for coverage in coverages]
    missing = any(row is None for row in rows)
    known = [row for row in rows if row is not None]
    ambiguous = len({coverage.rules[year].signature for coverage in coverages if year in coverage.rules}) > 1
    selected = known[0] if known and not missing and not ambiguous else None
    return selected, missing, ambiguous


@dataclass
class CommitmentRate:
    per_hour: float = 0.0
    per_workday: float = 0.0
    unknown_effort: int = 0
    unknown_coverage: int = 0
    count: int = 0

    def adjust(self, rate, direction):
        self.per_hour += direction * rate.per_hour
        self.per_workday += direction * rate.per_workday
        self.unknown_effort += direction * rate.unknown_effort
        self.unknown_coverage += direction * rate.unknown_coverage
        self.count += direction


class PeriodCommitments:
    """Fold baseline rates at interval boundaries without expanding each task into daily rows."""

    def __init__(self, tasks, members, coverages, start, end):
        self.coverages = coverages
        self.events = defaultdict(list)
        self.active = {}
        self.uncovered = False
        owners = {member.id: member for member in members}
        for task in tasks:
            first, last = task.baseline_start_date, task.baseline_end_date
            if not first or not last:
                continue
            lo, hi = max(first, start), min(last, end)
            if lo > hi:
                continue
            owner = owners[task.assignee_id]
            totals = coverages[owner.id].period_totals(first, last)
            rate = CommitmentRate()
            if totals is None:
                self.uncovered = True
                rate.unknown_coverage = 1
            elif not totals[1]:
                continue
            elif task.effort_hours is None:
                rate.unknown_effort = 1
            elif owner.availability_percent > 0 and owner.operational_utilization < 100 and owner.professionalism_coefficient > 0:
                # The owner's constant productivity factor cancels from the proportional share.
                rate.per_hour = task.effort_hours / totals[0]
            else:
                rate.per_workday = task.effort_hours / totals[1]
            self.events[lo].append((owner.id, rate, 1))
            if hi < end:
                self.events[hi + timedelta(days=1)].append((owner.id, rate, -1))

    def for_day(self, day):
        for owner, rate, direction in self.events.get(day, ()):
            active = self.active.setdefault(owner, CommitmentRate())
            active.adjust(rate, direction)
            if active.count == 0:
                del self.active[owner]
        total, unknown = 0.0, False
        for owner, rate in self.active.items():
            hours = self.coverages[owner].hours(day) or 0
            if hours:
                total += rate.per_hour * hours + rate.per_workday
                unknown |= rate.unknown_effort > 0
            unknown |= rate.unknown_coverage > 0
        return total, unknown


class CapacityService:
    def __init__(self, db):
        self.db = db

    def require_owner(self, profile_id):
        authority = self.db.info.get("authority")
        from app.config import get_settings
        if authority is None and get_settings().workchord_auth_mode != "trusted_local":
            raise AuthorityError("authentication_required", "Sign in to continue.", 401)
        if authority is not None and not (authority.operator or authority.local or
                authority.kind == "human" and authority.profile_id == profile_id):
            raise AuthorityError("profile_owner_required", "Only this person or an operator can manage their availability.")

    async def require_visible(self, profile_id):
        authority = self.db.info.get("authority")
        if authority is not None and not (authority.operator or authority.local or authority.profile_id == profile_id):
            visible = await self.db.scalar(select(TeamMember.id).where(TeamMember.profile_id == profile_id).limit(1))
            if visible is None:
                from app.models.task import Task
                visible = await self.db.scalar(select(Task.id).where(Task.owner_profile_id == profile_id).limit(1))
            if visible is None:
                raise AuthorityError("profile_unavailable", "Profile not found or inaccessible.", status=404)
        with internal_authority(self.db):
            if await self.db.get(TeamMemberProfile, profile_id) is None:
                raise PlanningConflict("profile_unavailable", "Profile not found or inaccessible.")

    async def calendar_for(self, member):
        """Use durable rules; retain a flagged local fallback until conflicts are reconciled."""
        return (await self.coverage_for(member)).primary

    async def coverage_for(self, member):
        """A profile owner's selection is authoritative; otherwise use this iteration's rules."""
        with internal_authority(self.db):
            setting = await self.db.get(ProfileAvailability, member.profile_id) if member.profile_id else None
            if setting and setting.calendar_id:
                return AnnualCalendars(await self.db.get(Calendar, setting.calendar_id), setting.additional_calendars)
        return AnnualCalendars.for_iteration(member.iteration)

    async def calendar_status(self, member):
        with internal_authority(self.db):
            setting = await self.db.get(ProfileAvailability, member.profile_id) if member.profile_id else None
            if setting and setting.calendar_id:
                return "profile", False
            if not member.profile_id:
                return "legacy_allocation", True
            from sqlalchemy.orm import selectinload
            period = member.iteration
            others = (await self.db.scalars(select(Iteration).join(TeamMember, TeamMember.iteration_id == Iteration.id)
                .options(selectinload(Iteration.calendar)).where(TeamMember.profile_id == member.profile_id,
                    Iteration.start_date <= period.end_date, Iteration.end_date >= period.start_date))).unique().all()
            own = AnnualCalendars.for_iteration(period)
            for other in others:
                coverage = AnnualCalendars.for_iteration(other)
                first = max(other.start_date, period.start_date).year
                last = min(other.end_date, period.end_date).year
                if any(agreed_calendar((own, coverage), year)[2] for year in range(first, last + 1)):
                    return "legacy_allocation", True
            return "legacy_allocation", False

    async def absence_ranges(self, member):
        """Never return these private ranges to a transport; expose only capacity totals."""
        with internal_authority(self.db):
            ranges = []
            if member.profile_id:
                ranges = list((await self.db.execute(select(ProfileAbsence.start_date, ProfileAbsence.end_date)
                    .where(ProfileAbsence.profile_id == member.profile_id, ProfileAbsence.deleted.is_(False)))).all())
                legacy = select(Vacation.start_date, Vacation.end_date).join(TeamMember, TeamMember.id == Vacation.team_member_id)
                legacy = legacy.where(TeamMember.profile_id == member.profile_id)
            else:
                legacy = select(Vacation.start_date, Vacation.end_date).where(Vacation.team_member_id == member.id)
            ranges.extend((await self.db.execute(legacy.where(Vacation.profile_absence_id.is_(None)))).all())
            return ranges

    async def invalidate_profile(self, profile_id, *, annual_selection=None, annual_only=False):
        """Update private derived revisions without exposing or rewriting their planning content."""
        from app.models.task import Task
        from app.services.snapshot_service import SnapshotService
        from app.services.task_service import TaskService
        with internal_authority(self.db):
            ids = list((await self.db.scalars(select(TeamMember.iteration_id).where(
                TeamMember.profile_id == profile_id, TeamMember.iteration_id.is_not(None)).distinct())).all())
            await lock_iterations(self.db, ids)
            for iteration_id in sorted(ids):
                await SnapshotService(self.db).create_snapshot(iteration_id, "before_availability_change")
            if annual_selection is not None:
                # A first explicit choice can replace different inherited rules in
                # different allocations. Check the actual prior rules of each row.
                from sqlalchemy.orm import selectinload
                from app.services.calendar_rules import task_uses_years
                from app.services.execution_planning_window import live_assignments

                members = (await self.db.scalars(select(TeamMember).where(
                    TeamMember.profile_id == profile_id, TeamMember.iteration_id.in_(ids)).options(
                    selectinload(TeamMember.iteration).selectinload(Iteration.calendar)))).all()
                replaced = {}
                for member in members:
                    years = (await self.coverage_for(member)).replaced_years(annual_selection)
                    if years:
                        replaced[member.id] = years
                if replaced:
                    tasks = (await self.db.scalars(select(Task).where(Task.assignee_id.in_(replaced),
                        Task.status != "closed").order_by(Task.id))).all()
                    affected = [task.id for task in tasks if task_uses_years(task, replaced[task.assignee_id])]
                    if await live_assignments(self.db, affected, lock=True):
                        raise PlanningConflict("annual_calendar_change_in_use",
                            "Issued work uses these existing annual rules. Coordinate with the responsible project manager.")
                if annual_only:
                    return
            tasks = (await self.db.scalars(select(Task).where(Task.iteration_id.in_(ids), Task.status != "closed")
                                          .order_by(Task.id))).all()
            if annual_selection is not None and await live_assignments(self.db, [task.id for task in tasks], lock=True):
                raise PlanningConflict("annual_calendar_change_in_use",
                    "This primary calendar change would reserve issued work. Coordinate with the responsible project manager.")
            for task in tasks:
                await TaskService(self.db).reserve_task_version(task, task.version)

    async def detail(self, profile_id):
        self.require_owner(profile_id)
        await self.require_visible(profile_id)
        with internal_authority(self.db):
            settings = await self.db.get(ProfileAvailability, profile_id)
            candidate_calendars = list((await self.db.scalars(select(Calendar).join(Iteration)
                .join(TeamMember, TeamMember.iteration_id == Iteration.id)
                .where(TeamMember.profile_id == profile_id))).unique().all())
            conflicts = sorted(calendar.id for calendar in candidate_calendars) if len({calendar_signature(c) for c in candidate_calendars}) > 1 else []
            absences = (await self.db.scalars(select(ProfileAbsence).where(ProfileAbsence.profile_id == profile_id,
                ProfileAbsence.deleted.is_(False)).order_by(ProfileAbsence.start_date, ProfileAbsence.id))).all()
            return {"profile_id": profile_id, "version": settings.version if settings else 0,
                "calendar_id": settings.calendar_id if settings else None,
                "additional_calendar_ids": [c.id for c in settings.additional_calendars] if settings else [],
                "calendar_conflicts": settings.calendar_conflicts if settings else [],
                "allocation_calendar_conflicts": conflicts,
                "calendar_selection_required": settings is None or settings.calendar_id is None,
                "absences": [{"id": item.id, "version": item.version, "start_date": item.start_date,
                              "end_date": item.end_date, "provenance": item.provenance} for item in absences]}

    @atomic_command
    async def set_calendar(self, profile_id, calendar_id, expected_version, additional_calendar_ids=None):
        self.require_owner(profile_id)
        await self.require_visible(profile_id)
        await lock_planning(self.db)
        calendar = await self.db.scalar(select(Calendar).where(Calendar.id == calendar_id))
        if calendar is None:
            raise PlanningConflict("calendar_unavailable", "Calendar not found or inaccessible.")
        explicit = None
        if additional_calendar_ids is not None:
            try:
                explicit = await CalendarService(self.db).selected_years(calendar, additional_calendar_ids)
            except ValueError as exc:
                raise PlanningConflict("calendar_selection_invalid", str(exc)) from exc
        with internal_authority(self.db):
            setting = await self.db.get(ProfileAvailability, profile_id, populate_existing=True)
            if expected_version != (setting.version if setting else 0):
                raise PlanningConflict("availability_version_conflict", "Availability changed. Reload before saving.")
            additional = explicit if explicit is not None else (list(setting.additional_calendars) if setting else [])
            if len(AnnualCalendars(calendar, additional).by_year) != 1 + len(additional):
                raise PlanningConflict("calendar_selection_invalid", "Choose one calendar per year in the same local time zone.")
            same_primary = setting is not None and setting.calendar_id == calendar.id
            selected = AnnualCalendars(calendar, additional) if explicit is not None or not same_primary else None
            await self.invalidate_profile(profile_id, annual_selection=selected,
                                          annual_only=explicit is not None and same_primary)
            if setting is None:
                setting = ProfileAvailability(profile_id=profile_id, version=1, additional_calendars=additional)
                self.db.add(setting)
            else:
                setting.version += 1
                setting.additional_calendars = additional
            setting.calendar_id, setting.provenance, setting.calendar_conflicts = calendar_id, "explicit", []
            await self.db.flush()
        return await self.detail(profile_id)

    @atomic_command
    async def save_absence(self, profile_id, start, end, *, absence_id=None, expected_version=None, deleted=False):
        self.require_owner(profile_id)
        await self.require_visible(profile_id)
        if end < start:
            raise PlanningConflict("invalid_absence_dates", "The end date must be on or after the start date.")
        await lock_planning(self.db)
        with internal_authority(self.db):
            absence = await self.db.get(ProfileAbsence, absence_id, populate_existing=True) if absence_id else None
            if absence_id and (absence is None or absence.profile_id != profile_id):
                raise PlanningConflict("absence_unavailable", "Absence not found or inaccessible.")
            if absence and expected_version != absence.version:
                raise PlanningConflict("absence_version_conflict", "Absence changed. Reload before saving.")
            await self.invalidate_profile(profile_id)
            if absence is None:
                absence = ProfileAbsence(profile_id=profile_id, version=1, provenance=[])
                self.db.add(absence)
            else:
                absence.version += 1
            authority = self.db.info.get("authority")
            absence.provenance = [*absence.provenance, {"version": absence.version,
                "start_date": start.isoformat(), "end_date": end.isoformat(), "deleted": deleted,
                "principal_id": authority.principal_id if authority else None}]
            absence.start_date, absence.end_date, absence.deleted = start, end, deleted
            await self.db.flush()
            if deleted:
                await self.db.execute(delete(Vacation).where(Vacation.profile_absence_id == absence.id))
            else:
                await self.db.execute(update(Vacation).where(Vacation.profile_absence_id == absence.id)
                                      .values(start_date=start, end_date=end))
        return absence

    async def projection(self, profile_id, start, end):
        if end < start or (end - start).days > 365:
            raise PlanningConflict("capacity_range_invalid", "Choose an inclusive date range of at most 366 days.")
        return await self._projection(profile_id, start, end)

    async def _projection(self, profile_id, start, end):
        await self.require_visible(profile_id)
        from sqlalchemy.orm import selectinload
        from app.models.task import Task
        from app.services.work_metrics import included_work_ids
        authority = self.db.info.get("authority")
        with internal_authority(self.db):
            revision = await self.db.scalar(select(PlanningState.revision).where(PlanningState.id == 1)) or 0
            setting = await self.db.get(ProfileAvailability, profile_id)
            members = list((await self.db.scalars(select(TeamMember).join(Iteration).where(
                TeamMember.profile_id == profile_id, Iteration.start_date <= end, Iteration.end_date >= start)
                .options(selectinload(TeamMember.iteration).selectinload(Iteration.calendar)))).all())
            canonical = await self.db.get(Calendar, setting.calendar_id) if setting and setting.calendar_id else None
            profile_coverage = AnnualCalendars(canonical, setting.additional_calendars) if canonical else None
            member_coverages = {m.id: profile_coverage or AnnualCalendars.for_iteration(m.iteration) for m in members}
            uncertain = not members and profile_coverage is None
            missing_years = set()
            observed_zones = set()
            observed_years = set()
            ranges = await self.absence_ranges(members[0]) if members else list((await self.db.execute(
                select(ProfileAbsence.start_date, ProfileAbsence.end_date).where(
                    ProfileAbsence.profile_id == profile_id, ProfileAbsence.deleted.is_(False)))).all())
            included = await included_work_ids(self.db, {member.iteration_id for member in members})
            tasks = list((await self.db.execute(select(Task.id, Task.assignee_id, Task.baseline_start_date, Task.baseline_end_date, Task.effort_hours).where(Task.assignee_id.in_([m.id for m in members]),
                Task.id.in_(included), Task.status != "closed"))).all())
            commitments = PeriodCommitments(tasks, members, member_coverages, start, end)
            from app.services.capacity_adjustments import load_dated_availability
            dated = await load_dated_availability(self.db, [m.id for m in members])
            resolved_calendars = {}
            result = []
            day = start
            while day <= end:
                scheduled = [m for m in members if m.iteration.start_date <= day <= m.iteration.end_date]
                absent = any(a <= day <= b for a, b in ranges)
                dated_coverage = profile_coverage
                if profile_coverage is not None:
                    calendar = profile_coverage.by_year.get(day.year)
                    missing, ambiguous = calendar is None, False
                else:
                    candidates = scheduled or [m for m in members if m.iteration.start_date.year <= day.year <= m.iteration.end_date.year]
                    cache_key = (day.year, tuple(m.id for m in candidates))
                    if cache_key not in resolved_calendars:
                        resolved_calendars[cache_key] = agreed_calendar([member_coverages[m.id] for m in candidates], day.year)
                    calendar, missing, ambiguous = resolved_calendars[cache_key]
                    dated_coverage = member_coverages[candidates[0].id] if candidates else None
                    if not candidates:
                        missing = bool(members)
                if missing:
                    missing_years.add(day.year)
                uncertain |= ambiguous
                if calendar:
                    observed_zones.add(calendar.timezone)
                    observed_years.add(calendar.year)
                available = dated_coverage.hours(day) if calendar and not absent else 0.0
                def hours(member):
                    return 0.0 if absent else member_coverages[member.id].hours(day) or 0.0
                incomplete = any(member_coverages[m.id].by_year.get(day.year) is None for m in scheduled)
                allocated = sum(hours(m) * dated.percent(m, day) / 100 for m in scheduled)
                private_busy = sum(hours(m) * dated.percent(m, day) / 100 for m in scheduled
                    if authority and not (authority.operator or authority.local or authority.allows(m.iteration.project_id, "read")))
                productive = sum(hours(m) * dated.percent(m, day) / 100 *
                    (1 - m.operational_utilization / 100) * m.professionalism_coefficient for m in scheduled)
                committed, unknown_commitment = commitments.for_day(day)
                result.append({"date": day, "available_hours": round(available, 4) if calendar else None,
                    "allocated_hours": None if incomplete else round(allocated, 4), "private_busy_hours": None if incomplete else round(private_busy, 4),
                    "productive_hours": round(productive if available else 0, 4) if calendar else None,
                    "committed_effort_hours": round(committed, 4),
                    "has_unknown_commitment": unknown_commitment,
                    "overallocated_hours": round(max(0, allocated - available), 4) if calendar else None})
                day += timedelta(days=1)
            return {"profile_id": profile_id, "planning_revision": revision,
                "calendar_uncertain": uncertain, "timezone": canonical.timezone if canonical else (next(iter(observed_zones)) if len(observed_zones)==1 else None),
                "calendar_year": canonical.year if canonical else (next(iter(observed_years)) if len(observed_years)==1 else None),
                "missing_calendar_years": sorted(missing_years), "outside_calendar_year": bool(missing_years),
                "has_uncovered_commitments": commitments.uncovered,
                "has_unknown_effort": any(task.effort_hours is None for task in tasks), "days": result,
                "commitment_assumption": "Known effort is distributed proportionally over calendar working hours in each saved baseline; forecasts are excluded.",
                "allocations": [{"member_id": m.id, "iteration_id": m.iteration_id,
                    "availability_percent": m.availability_percent, "operational_utilization": m.operational_utilization,
                    "professionalism_coefficient": m.professionalism_coefficient} for m in members
                    if authority is None or authority.operator or authority.local or authority.allows(m.iteration.project_id, "read")],
                "formula": "allocated = person calendar hours after absence × availability on that date; productive = allocated × (1 − utilization) × coefficient",
                "rounding": "Round output hours to 4 decimals; calculate using unrounded values."}

    async def schedule_issues(self, iteration, members):
        """Return aggregate constraints without exposing private work or changing existing plans."""
        issues = []
        missing = AnnualCalendars.for_iteration(iteration).missing_years(iteration.start_date, iteration.end_date)
        if missing:
            issues.append({"profile_id": None, "code": "calendar_outside_year", "missing_calendar_years": missing,
                           "message": "Select an annual calendar for every year of this iteration."})
        if any(member.profile_id is None for member in members):
            issues.append({"profile_id": None, "code": "capacity_profile_required",
                "message": "Link every allocation to a durable profile before committing shared capacity."})
        for profile_id in sorted({member.profile_id for member in members if member.profile_id is not None}):
            if missing and (iteration.end_date - iteration.start_date).days > 365:
                # The forecast is already held. Avoid expanding an arbitrarily long
                # uncovered interval; still identify the affected owner and years.
                owner = next(row for row in members if row.profile_id == profile_id)
                coverage = await self.coverage_for(owner)
                missing_years = coverage.missing_years(iteration.start_date, iteration.end_date)
                if missing_years:
                    issues.append({"profile_id":profile_id,"code":"calendar_reconciliation_required",
                        "missing_calendar_years":missing_years,"message":"Select a person calendar covering this plan before committing."})
                continue
            projection = await self._projection(profile_id, iteration.start_date, iteration.end_date)
            if projection["calendar_uncertain"] or projection["outside_calendar_year"]:
                issues.append({"profile_id": profile_id, "code": "calendar_reconciliation_required",
                    "missing_calendar_years": projection["missing_calendar_years"],
                    "message": "Select a person calendar covering this plan before committing."})
            if projection["has_uncovered_commitments"]:
                issues.append({"profile_id": profile_id, "code": "commitment_calendar_coverage_missing",
                    "message": "This person's saved commitment has an unknown distribution. Ask the capacity owner "
                               "to reconcile its annual rules before publishing a baseline. The draft forecast remains available."})
            committed_overflow = [str(row["date"]) for row in projection["days"]
                if row["productive_hours"] is not None and row["committed_effort_hours"] > row["productive_hours"] + .000001]
            if committed_overflow:
                issues.append({"profile_id": profile_id, "code": "committed_capacity_exceeded", "dates": committed_overflow,
                    "message": "Saved commitments exceed productive capacity. Reconcile them before publishing another schedule."})
            dates = [str(row["date"]) for row in projection["days"] if row["overallocated_hours"] and row["overallocated_hours"] > .000001]
            if dates:
                issues.append({"profile_id": profile_id, "code": "shared_capacity_overallocated", "dates": dates,
                    "message": "Reduce overlapping allocations or change the plan dates before committing."})
        return issues
