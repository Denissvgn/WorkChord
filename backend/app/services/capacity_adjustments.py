"""Dated availability adjustments on iteration capacity rows.

A capacity row (``TeamMember``) has one availability percentage for its whole
iteration. An adjustment replaces that percentage on a bounded date range only.
Every capacity calculation reads the effective percentage through
``DatedAvailability``, so a date without an adjustment keeps the row's own value.

Changing an adjustment is a shared planning input change: it advances the shared
planning revision and the revision of every iteration whose capacity it can
affect. It changes no task, so task versions and issued work stay current. A
reduction on dates where this row's issued work is scheduled is refused.
"""

from datetime import date, timedelta
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.authority import internal_authority
from app.commands import PlanningConflict, current_command, planning_input_reservation, preview_command, schedule_input_command
from app.models.iteration import Iteration
from app.models.team_member import TeamMember, TeamMemberCapacityAdjustment
from app.schemas.team import CapacityAdjustmentCommand, CapacityAdjustmentResponse
from app.utils.time import utc_now

ADJUSTMENT_KIND = "member_capacity_adjustment"
MAX_ACTIVE_ADJUSTMENTS = 200
MAX_PREVIEW_DAYS = 366
AUDIT_ACTION = "team_member_capacity_adjusted"


class DatedAvailability:
    """The effective availability percentage of capacity rows on each date."""

    def __init__(self, ranges=None):
        self.ranges = {key: sorted(value) for key, value in (ranges or {}).items() if value}

    def has_adjustments(self, member_id):
        return member_id in self.ranges

    def percent(self, member, day):
        for start, end, value in self.ranges.get(member.id, ()):
            if start <= day <= end:
                return value
            if start > day:
                break
        return member.availability_percent

    def adjusted_days(self, member):
        """Yield each adjusted date and its percentage."""
        for start, end, value in self.ranges.get(member.id, ()):
            day = start
            while day <= end:
                yield day, value
                day += timedelta(days=1)

    def any_positive(self, member):
        return any(value > 0 for _, _, value in self.ranges.get(member.id, ()))

    def signature(self, member_id):
        return [(start.isoformat(), end.isoformat(), value) for start, end, value in self.ranges.get(member_id, ())]


async def load_dated_availability(db, member_ids):
    """Read active adjustments of rows the caller already holds; return only dates and percentages."""
    ids = sorted({member_id for member_id in member_ids if member_id is not None})
    if not ids:
        return DatedAvailability()
    adjustment = TeamMemberCapacityAdjustment
    with internal_authority(db):
        rows = (await db.execute(
            select(adjustment.team_member_id, adjustment.start_date, adjustment.end_date, adjustment.availability_percent)
            .where(adjustment.team_member_id.in_(ids), adjustment.withdrawn_at.is_(None))
            .order_by(adjustment.team_member_id, adjustment.start_date, adjustment.id)
        )).all()
    ranges = {}
    for member_id, start, end, value in rows:
        ranges.setdefault(member_id, []).append((start, end, value))
    return DatedAvailability(ranges)


async def active_adjustment_rows(db, member_ids):
    """Return active adjustment rows by capacity row for a recovery snapshot."""
    ids = sorted({member_id for member_id in member_ids if member_id is not None})
    if not ids:
        return {}
    adjustment = TeamMemberCapacityAdjustment
    with internal_authority(db):
        rows = (await db.scalars(
            select(adjustment).where(adjustment.team_member_id.in_(ids), adjustment.withdrawn_at.is_(None))
            .order_by(adjustment.team_member_id, adjustment.start_date, adjustment.id)
        )).all()
    result = {}
    for row in rows:
        result.setdefault(row.team_member_id, []).append(row)
    return result


async def restore_adjustments(db, member, saved, snapshot_name):
    """Make a restored row's active adjustments match its snapshot, keeping every prior record."""
    if not isinstance(saved, list) or len(saved) > MAX_ACTIVE_ADJUSTMENTS:
        raise ValueError("Snapshot capacity adjustments are invalid")
    wanted = {}
    for item in saved:
        try:
            start, end = date.fromisoformat(item["start_date"]), date.fromisoformat(item["end_date"])
            percent = float(item["availability_percent"])
            identifier, reason = item.get("id"), str(item.get("reason") or "Restored from a recovery snapshot")
        except (KeyError, TypeError, ValueError, AttributeError):
            raise ValueError("Snapshot capacity adjustments are invalid") from None
        if end < start or not 0 <= percent <= 100:
            raise ValueError("Snapshot capacity adjustments are invalid")
        wanted[(identifier, start, end, percent)] = reason
    adjustment = TeamMemberCapacityAdjustment
    current = list((await db.scalars(select(adjustment).where(
        adjustment.team_member_id == member.id, adjustment.withdrawn_at.is_(None)).with_for_update())).all())
    keep = {(row.id, row.start_date, row.end_date, row.availability_percent) for row in current} & set(wanted)
    authority = db.info.get("authority")
    principal_id = getattr(authority, "principal_id", None)
    token, now = str(uuid4()), utc_now()
    for row in current:
        if (row.id, row.start_date, row.end_date, row.availability_percent) not in keep:
            row.withdrawn_at, row.withdrawn_by_principal_id = now, principal_id
            row.withdrawal_reason, row.withdrawn_group_token = f"Restored recovery snapshot {snapshot_name}", token
    spans = sorted((start, end) for (_, start, end, _) in wanted)
    if any(second <= first_end for (_, first_end), (second, _) in zip(spans, spans[1:])):
        raise ValueError("Snapshot capacity adjustments overlap")
    db.add_all([adjustment(team_member_id=member.id, start_date=start, end_date=end, availability_percent=percent,
                           base_availability_percent=member.availability_percent, reason=reason, group_token=token,
                           created_by_principal_id=principal_id, created_at=now)
                for key, reason in wanted.items() if key not in keep for (_, start, end, percent) in [key]])
    await db.flush()


def _response(row, *, persisted=True):
    data = CapacityAdjustmentResponse.model_validate(row)
    data.active = row.withdrawn_at is None
    if not persisted:
        data.id = None
        data.created_at = None
        data.group_token = None
    return data


def _days(start, end):
    day = start
    while day <= end:
        yield day
        day += timedelta(days=1)


class CapacityAdjustmentService:
    """Record, withdraw, preview and list dated capacity adjustments."""

    def __init__(self, db):
        self.db = db

    async def _member(self, member_id):
        member = (await self.db.execute(
            select(TeamMember).options(selectinload(TeamMember.iteration).selectinload(Iteration.calendar))
            .where(TeamMember.id == member_id)
        )).scalar_one_or_none()
        if member is None:
            from app.services.planning_input_context import PlanningInputUnavailable
            raise PlanningInputUnavailable("Capacity row not found or inaccessible")
        return member

    async def list_adjustments(self, member_id, *, include_withdrawn=False):
        await self._member(member_id)
        adjustment = TeamMemberCapacityAdjustment
        query = select(adjustment).where(adjustment.team_member_id == member_id)
        if not include_withdrawn:
            query = query.where(adjustment.withdrawn_at.is_(None))
        from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
        rows = (await self.db.scalars(query.order_by(adjustment.start_date, adjustment.id).limit(MAX_BOUNDED_LIST_ITEMS + 1))).all()
        if len(rows) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError("capacity_adjustments", MAX_BOUNDED_LIST_ITEMS)
        return [_response(row) for row in rows]

    @preview_command
    async def preview(self, member_id, data: CapacityAdjustmentCommand):
        """Calculate effective capacity with the change, then roll everything back."""
        async with planning_input_reservation(self.db, ADJUSTMENT_KIND, {"member_id": member_id, "data": data}):
            return await self._change(member_id, data)

    @schedule_input_command(ADJUSTMENT_KIND)
    async def apply(self, member_id, data: CapacityAdjustmentCommand, *, commit: bool = True):
        """Record the change under the observed planning revisions."""
        return await self._change(member_id, data)

    async def _change(self, member_id, data):
        state = current_command(self.db)
        applying = state.mode == "apply"
        member = await self._member(member_id)
        if member.iteration_id is None or member.iteration is None:
            raise PlanningConflict("capacity_adjustment_unscheduled", "Add this capacity row to an iteration before adjusting dates.")
        await self.db.execute(select(TeamMember.id).where(TeamMember.id == member_id).with_for_update())
        iteration = member.iteration
        adjustment = TeamMemberCapacityAdjustment
        active = list((await self.db.scalars(
            select(adjustment).where(adjustment.team_member_id == member_id, adjustment.withdrawn_at.is_(None))
            .order_by(adjustment.start_date, adjustment.id).with_for_update()
        )).all())
        by_id = {row.id: row for row in active}
        missing = [value for value in data.withdraw_adjustment_ids if value not in by_id]
        if missing:
            raise PlanningConflict("capacity_adjustment_unavailable",
                "These adjustments are not active on this capacity row: " + ", ".join(map(str, missing)) + ". Reload its adjustments.")
        withdrawn = [by_id[value] for value in data.withdraw_adjustment_ids]
        remaining = [row for row in active if row.id not in set(data.withdraw_adjustment_ids)]
        items = sorted(data.adjustments, key=lambda item: (item.start_date, item.end_date))
        for item in items:
            if item.start_date < iteration.start_date or item.end_date > iteration.end_date:
                raise PlanningConflict("capacity_adjustment_outside_iteration",
                    f"Adjust dates from {iteration.start_date} through {iteration.end_date}, the dates of this capacity row's iteration.")
        spans = [(item.start_date, item.end_date) for item in items]
        for (_, first_end), (second_start, _) in zip(spans, spans[1:]):
            if second_start <= first_end:
                raise PlanningConflict("capacity_adjustment_overlap", "Adjustments in one command must not overlap.")
        for item in items:
            for row in remaining:
                if row.start_date <= item.end_date and item.start_date <= row.end_date:
                    raise PlanningConflict("capacity_adjustment_overlap",
                        f"Adjustment {row.id} already covers some of these dates. Withdraw it in the same command to replace it.")
        if len(remaining) + len(items) > MAX_ACTIVE_ADJUSTMENTS:
            raise PlanningConflict("capacity_adjustment_limit", f"A capacity row holds at most {MAX_ACTIVE_ADJUSTMENTS} active adjustments.")
        changed = spans + [(row.start_date, row.end_date) for row in withdrawn]
        first, last = min(start for start, _ in changed), max(end for _, end in changed)
        if (last - first).days >= MAX_PREVIEW_DAYS:
            raise PlanningConflict("capacity_adjustment_range_invalid",
                f"Change dates within {MAX_PREVIEW_DAYS} consecutive days in one command.")

        before = DatedAvailability({member.id: [(row.start_date, row.end_date, row.availability_percent) for row in active]})
        after = DatedAvailability({member.id: [(row.start_date, row.end_date, row.availability_percent) for row in remaining]
                                   + [(item.start_date, item.end_date, item.availability_percent) for item in items]})
        reduced = [day for day in _days(first, last) if after.percent(member, day) < before.percent(member, day)]
        await self._refuse_reducing_issued_work(member, reduced)

        from app.services.capacity_service import CapacityService
        capacity = CapacityService(self.db)
        coverage = await capacity.coverage_for(member)
        absences = await capacity.absence_ranges(member)
        projection_before = await self._projection(member, first, last)

        authority = self.db.info.get("authority")
        principal_id = getattr(authority, "principal_id", None)
        token = str(uuid4())
        now = utc_now()
        for row in withdrawn:
            row.withdrawn_at = now
            row.withdrawn_by_principal_id = principal_id
            row.withdrawal_reason = data.reason
            row.withdrawn_group_token = token
        created = [adjustment(team_member_id=member.id, start_date=item.start_date, end_date=item.end_date,
                              availability_percent=item.availability_percent,
                              base_availability_percent=member.availability_percent,
                              reason=item.reason or data.reason, group_token=token,
                              created_by_principal_id=principal_id, created_at=now)
                   for item in items]
        self.db.add_all(created)
        await self.db.flush()
        projection_after = await self._projection(member, first, last)

        def own_hours(day):
            if any(start <= day <= end for start, end in absences):
                return 0.0
            return coverage.hours(day)

        def rounded(value):
            return None if value is None else round(value, 4)

        days = []
        for index, day in enumerate(_days(first, last)):
            hours = own_hours(day)
            own_before = None if hours is None else hours * before.percent(member, day) / 100
            own_after = None if hours is None else hours * after.percent(member, day) / 100
            row = {
                "date": day,
                "availability_percent_before": before.percent(member, day),
                "availability_percent_after": after.percent(member, day),
                "row_hours_before": rounded(own_before),
                "row_hours_after": rounded(own_after),
                "available_hours": rounded(hours),
                "allocated_hours_before": rounded(own_before),
                "allocated_hours_after": rounded(own_after),
                "overallocated_hours_before": None if hours is None else rounded(max(0.0, own_before - hours)),
                "overallocated_hours_after": None if hours is None else rounded(max(0.0, own_after - hours)),
            }
            if projection_before is not None:
                # The person's totals include every row of the same profile, in any project.
                prior, later = projection_before[index], projection_after[index]
                row.update(available_hours=prior["available_hours"],
                           allocated_hours_before=prior["allocated_hours"], allocated_hours_after=later["allocated_hours"],
                           overallocated_hours_before=prior["overallocated_hours"],
                           overallocated_hours_after=later["overallocated_hours"])
            days.append(row)

        active_after = sorted(remaining + created, key=lambda row: (row.start_date, row.id or 0))
        result = {
            "applied": applying,
            "member_id": member.id,
            "iteration_id": member.iteration_id,
            "profile_id": member.profile_id,
            "group_token": token if applying else None,
            "created": [_response(row, persisted=applying) for row in created],
            "withdrawn": [_response(row, persisted=True) for row in withdrawn],
            "active_adjustments": [_response(row, persisted=applying or row not in created) for row in active_after],
            "reduced_dates": reduced,
            "effective_capacity": days,
            "observed_revisions": dict(sorted(state.iterations.items())),
            "resulting_revisions": {key: value + 1 for key, value in sorted(state.iterations.items())} if applying else {},
            "planning_revision": state.planning_revision,
        }
        if applying:
            from app.models.identity import CommandAudit
            self.db.add(CommandAudit(
                principal_id=principal_id,
                project_id=iteration.project_id,
                action=AUDIT_ACTION,
                source=getattr(authority, "source", None) or "local",
                correlation_id=getattr(authority, "correlation_id", None) or token,
                reason=data.reason,
                details={
                    "member_id": member.id,
                    "iteration_id": member.iteration_id,
                    "profile_id": member.profile_id,
                    "group_token": token,
                    "base_availability_percent": member.availability_percent,
                    "created": [{"id": row.id, "start_date": row.start_date.isoformat(), "end_date": row.end_date.isoformat(),
                                 "availability_percent": row.availability_percent} for row in created],
                    "withdrawn": [{"id": row.id, "start_date": row.start_date.isoformat(), "end_date": row.end_date.isoformat(),
                                   "availability_percent": row.availability_percent} for row in withdrawn],
                    "observed_revisions": {str(key): value for key, value in sorted(state.iterations.items())},
                    "planning_revision": state.planning_revision,
                },
            ))
            await self.db.flush()
        return result

    async def _refuse_reducing_issued_work(self, member, reduced):
        """A reduction must not change the capacity that this row's issued work was planned with."""
        if not reduced:
            return
        from app.models.task import Task
        from app.services.calendar_rules import issued_coordinates
        from app.services.execution_planning_window import live_assignments
        first, last = min(reduced), max(reduced)
        dates = set(reduced)
        with internal_authority(self.db):
            tasks = (await self.db.execute(
                select(Task.id, Task.start_date, Task.end_date)
                .where(Task.assignee_id == member.id, Task.status != "closed",
                       Task.start_date.is_not(None), Task.end_date.is_not(None),
                       Task.start_date <= last, Task.end_date >= first)
                .order_by(Task.id)
            )).all()
            affected = [task.id for task in tasks if any(day in dates for day in _days(max(task.start_date, first), min(task.end_date, last)))]
            issued = await live_assignments(self.db, affected, lock=True)
        if issued:
            raise PlanningConflict(
                "capacity_adjustment_in_use",
                "Issued work on this capacity row is scheduled on the reduced dates. Finish or reconcile these "
                "task (assignment) IDs first, or reduce other dates: " + issued_coordinates(issued),
            )

    async def _projection(self, member, start, end):
        """Return the person's daily totals across all of their rows, or None for a row without a person."""
        if member.profile_id is None:
            return None
        from app.services.capacity_service import CapacityService
        projection = await CapacityService(self.db)._projection(member.profile_id, start, end)
        return projection["days"]
