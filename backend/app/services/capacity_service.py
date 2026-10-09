"""Profile-owned availability and permission-safe date capacity projections."""

from datetime import date, timedelta

from sqlalchemy import delete, select, update

from app.authority import AuthorityError, internal_authority
from app.commands import PlanningConflict, atomic_command, lock_iterations, lock_planning
from app.models.calendar import Calendar
from app.models.capacity import PlanningState, ProfileAbsence, ProfileAvailability
from app.models.iteration import Iteration
from app.models.team_member import TeamMember, TeamMemberProfile, Vacation


def day_hours(calendar, day):
    """Nominal local-date hours, with each holiday/weekend/short-day rule applied once."""
    if day.weekday() in calendar.weekend_days or day.isoformat() in calendar.holidays:
        return 0.0
    return max(0.0, calendar.nominal_day_hours - (day.isoformat() in calendar.short_days))


def calendar_signature(calendar):
    return (calendar.year, calendar.timezone, calendar.nominal_day_hours,
            tuple(sorted(calendar.holidays)), tuple(sorted(calendar.weekend_days)), tuple(sorted(calendar.short_days)))


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
        with internal_authority(self.db):
            setting = await self.db.get(ProfileAvailability, member.profile_id) if member.profile_id else None
            if setting and setting.calendar_id:
                return await self.db.get(Calendar, setting.calendar_id)
        return member.iteration.calendar

    async def calendar_status(self, member):
        with internal_authority(self.db):
            setting = await self.db.get(ProfileAvailability, member.profile_id) if member.profile_id else None
            if setting and setting.calendar_id:
                return "profile", False
            calendars = (await self.db.scalars(select(Calendar).join(Iteration).join(TeamMember,
                TeamMember.iteration_id == Iteration.id).where(TeamMember.profile_id == member.profile_id))).all() if member.profile_id else []
            return "legacy_allocation", not member.profile_id or len({calendar_signature(item) for item in calendars}) != 1

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

    async def invalidate_profile(self, profile_id):
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
            tasks = (await self.db.scalars(select(Task).where(Task.iteration_id.in_(ids), Task.status != "closed")
                                          .order_by(Task.id))).all()
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
                "calendar_conflicts": settings.calendar_conflicts if settings else [],
                "allocation_calendar_conflicts": conflicts,
                "calendar_selection_required": settings is None or settings.calendar_id is None,
                "absences": [{"id": item.id, "version": item.version, "start_date": item.start_date,
                              "end_date": item.end_date, "provenance": item.provenance} for item in absences]}

    @atomic_command
    async def set_calendar(self, profile_id, calendar_id, expected_version):
        self.require_owner(profile_id)
        await self.require_visible(profile_id)
        await lock_planning(self.db)
        calendar = await self.db.scalar(select(Calendar).where(Calendar.id == calendar_id))
        if calendar is None:
            raise PlanningConflict("calendar_unavailable", "Calendar not found or inaccessible.")
        with internal_authority(self.db):
            setting = await self.db.get(ProfileAvailability, profile_id, populate_existing=True)
            if expected_version != (setting.version if setting else 0):
                raise PlanningConflict("availability_version_conflict", "Availability changed. Reload before saving.")
            await self.invalidate_profile(profile_id)
            if setting is None:
                setting = ProfileAvailability(profile_id=profile_id, version=1)
                self.db.add(setting)
            else:
                setting.version += 1
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
            calendars = {calendar_signature(member.iteration.calendar) for member in members}
            uncertain = canonical is None and len(calendars) != 1
            calendar = canonical or (members[0].iteration.calendar if len(calendars) == 1 else None)
            ranges = await self.absence_ranges(members[0]) if members else list((await self.db.execute(
                select(ProfileAbsence.start_date, ProfileAbsence.end_date).where(
                    ProfileAbsence.profile_id == profile_id, ProfileAbsence.deleted.is_(False)))).all())
            included = await included_work_ids(self.db, {member.iteration_id for member in members})
            tasks = list((await self.db.execute(select(Task.id, Task.assignee_id, Task.baseline_start_date, Task.baseline_end_date, Task.effort_hours).where(Task.assignee_id.in_([m.id for m in members]),
                Task.id.in_(included), Task.status != "closed"))).all())
            commitments = {}
            for task in tasks:
                if not task.baseline_start_date or not task.baseline_end_date:
                    continue
                member = next(m for m in members if m.id == task.assignee_id)
                task_calendar = canonical or member.iteration.calendar
                days = []
                day = task.baseline_start_date
                # Legacy dates may predate calendar coverage. Flag this instead of inventing hours.
                if (task.baseline_end_date - day).days > 365 or day > task.baseline_end_date:
                    continue
                while day <= task.baseline_end_date:
                    if day_hours(task_calendar, day):
                        days.append((day, day_hours(task_calendar, day) * member.availability_percent / 100 * (1 - member.operational_utilization / 100) * member.professionalism_coefficient))
                    day += timedelta(days=1)
                total_weight = sum(weight for _, weight in days)
                for day, weight in days:
                    share = weight / total_weight if total_weight > 0 else 1 / len(days)
                    commitments.setdefault(day, []).append(None if task.effort_hours is None else task.effort_hours * share)
            result = []
            day = start
            while day <= end:
                available = day_hours(calendar, day) if calendar and not any(a <= day <= b for a, b in ranges) else 0.0
                scheduled = [m for m in members if m.iteration.start_date <= day <= m.iteration.end_date]
                absent = any(a <= day <= b for a, b in ranges)
                def hours(member):
                    return 0.0 if absent else day_hours(calendar or member.iteration.calendar, day)
                allocated = sum(hours(m) * m.availability_percent / 100 for m in scheduled)
                private_busy = sum(hours(m) * m.availability_percent / 100 for m in scheduled
                    if authority and not (authority.operator or authority.local or authority.allows(m.iteration.project_id, "read")))
                productive = sum(hours(m) * m.availability_percent / 100 *
                    (1 - m.operational_utilization / 100) * m.professionalism_coefficient for m in scheduled)
                result.append({"date": day, "available_hours": round(available, 4) if calendar else None,
                    "allocated_hours": round(allocated, 4), "private_busy_hours": round(private_busy, 4),
                    "productive_hours": round(productive if available else 0, 4) if calendar else None,
                    "committed_effort_hours": round(sum(value for value in commitments.get(day, []) if value is not None), 4),
                    "has_unknown_commitment": any(value is None for value in commitments.get(day, [])),
                    "overallocated_hours": round(max(0, allocated - available), 4) if calendar else None})
                day += timedelta(days=1)
            return {"profile_id": profile_id, "planning_revision": revision,
                "calendar_uncertain": uncertain, "timezone": calendar.timezone if calendar else None,
                "calendar_year": calendar.year if calendar else None,
                "outside_calendar_year": bool(calendar and (start.year != calendar.year or end.year != calendar.year)),
                "has_unknown_effort": any(task.effort_hours is None for task in tasks), "days": result,
                "commitment_assumption": "Known effort is distributed proportionally over calendar working hours in each saved baseline; forecasts are excluded.",
                "allocations": [{"member_id": m.id, "iteration_id": m.iteration_id,
                    "availability_percent": m.availability_percent, "operational_utilization": m.operational_utilization,
                    "professionalism_coefficient": m.professionalism_coefficient} for m in members
                    if authority is None or authority.operator or authority.local or authority.allows(m.iteration.project_id, "read")],
                "formula": "allocated = person calendar hours after absence × availability; productive = allocated × (1 − utilization) × coefficient",
                "rounding": "Round output hours to 4 decimals; calculate using unrounded values."}

    async def schedule_issues(self, iteration, members):
        """Return aggregate constraints without exposing private work or changing existing plans."""
        issues = []
        if any(member.profile_id is None for member in members):
            issues.append({"profile_id": None, "code": "capacity_profile_required",
                "message": "Link every allocation to a durable profile before committing shared capacity."})
        for profile_id in sorted({member.profile_id for member in members if member.profile_id is not None}):
            projection = await self.projection(profile_id, iteration.start_date, iteration.end_date)
            if projection["calendar_uncertain"] or projection["outside_calendar_year"]:
                issues.append({"profile_id": profile_id, "code": "calendar_reconciliation_required",
                    "message": "Select a person calendar covering this plan before committing."})
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
