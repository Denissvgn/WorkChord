"""Temporary capacity transfers between rows of one person, with a dated return.

A transfer lends part of the availability percentage of one or more source rows
(each an iteration's capacity row, usually in different projects) to a target row
of the same person for a bounded date range. It is recorded as dated adjustments,
one per row, that share one group token: each source counts its own percentage
minus the lent percentage and the target its own percentage plus the sum of the
lent percentages, on the transfer's dates only. Every other date keeps each row's
own percentage, so the prior shares apply again after the end date without any
scheduled job, and the rows' own percentages are never edited.

Recording or withdrawing a transfer is one shared planning input command over the
planning scope of every row it changes, so both sides change together or not at
all and an intervening change to any affected iteration is a revision conflict. It
changes no task, assignment or run. A source reduction on dates where that row's
issued work is scheduled is refused, as is restoring the target on such dates.
"""

from datetime import timedelta
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.authority import internal_authority
from app.commands import PlanningConflict, current_command, planning_input_reservation, preview_command, schedule_input_command
from app.models.iteration import Iteration
from app.models.team_member import TeamMember, TeamMemberCapacityAdjustment
from app.services.capacity_adjustments import MAX_ACTIVE_ADJUSTMENTS, CapacityAdjustmentService, _days, _response
from app.services.work_metrics import working_today
from app.utils.time import utc_now

TRANSFER_KIND = "capacity_transfer"
TRANSFER_AUDIT_ACTION = "team_member_capacity_transferred"
WITHDRAWAL_AUDIT_ACTION = "team_member_capacity_transfer_withdrawn"


def _unavailable(message="Capacity transfer not found or inaccessible"):
    from app.services.planning_input_context import PlanningInputUnavailable
    return PlanningInputUnavailable(message)


async def transfer_group_members(db, group_token):
    """Return the capacity rows of a recorded transfer, or None when the token names no transfer."""
    adjustment = TeamMemberCapacityAdjustment
    with internal_authority(db):
        members = (await db.scalars(select(adjustment.team_member_id).where(adjustment.group_token == group_token)
                                    .distinct().limit(MAX_ACTIVE_ADJUSTMENTS + 1))).all()
    # Adjustments recorded on one row by one command share a token too; only a token
    # spanning several rows is a transfer.
    return sorted(members) if len(members) > 1 else None


async def transfer_member_ids(db, values):
    """Resolve every row a transfer command changes, for its planning reservation."""
    token = values.get("group_token")
    if token is None:
        data = values["data"]
        return sorted({data.target_member_id, *(source.member_id for source in data.sources)})
    members = await transfer_group_members(db, token)
    if members is None:
        raise _unavailable()
    return members


async def transfer_iteration_ids(db, values):
    """The planning scope of a transfer is the union of the scopes of all of its rows."""
    from app.services.planning_input_context import affected_iteration_ids
    ids = set()
    for member_id in await transfer_member_ids(db, values):
        ids.update(await affected_iteration_ids(db, "member", {"member_id": member_id}))
    if len(ids) > 500:
        raise PlanningConflict("planning_scope_oversized", "This planning input affects more than the supported revision context limit.")
    return sorted(ids)


async def refuse_withdrawing_transfer_side(db, rows):
    """A single-row command must not withdraw one side of a transfer and leave the other in place."""
    for token in sorted({row.group_token for row in rows}):
        if await transfer_group_members(db, token) is not None:
            raise PlanningConflict(
                "capacity_transfer_side",
                f"This adjustment is one side of capacity transfer {token}. Withdraw the transfer to return every row together.",
            )


async def refuse_removing_transfer_row(db, member_id):
    """Removing a row would leave the other rows of an unfinished transfer changed alone."""
    from app.models.calendar import Calendar
    from app.models.project import Project
    adjustment = TeamMemberCapacityAdjustment
    with internal_authority(db):
        zone = (await db.execute(
            select(Project.timezone, Calendar.timezone).select_from(TeamMember)
            .join(Iteration, Iteration.id == TeamMember.iteration_id)
            .join(Calendar, Calendar.id == Iteration.calendar_id)
            .outerjoin(Project, Project.id == Iteration.project_id)
            .where(TeamMember.id == member_id)
        )).first()
        if zone is None:
            return
        today = working_today(zone[0] or zone[1])
        # A transfer whose dates have all passed has already returned; it does not hold the row.
        tokens = (await db.scalars(select(adjustment.group_token).where(
            adjustment.team_member_id == member_id, adjustment.withdrawn_at.is_(None),
            adjustment.end_date >= today).distinct())).all()
    for token in sorted(tokens):
        if await transfer_group_members(db, token) is not None:
            raise PlanningConflict(
                "capacity_transfer_active",
                f"This capacity row is part of capacity transfer {token}. Withdraw the transfer before removing the row.",
            )


def _round(value):
    return None if value is None else round(value, 4)


class _RowHours:
    """Calendar hours of one row on each date, after the person's absences."""

    def __init__(self, coverage, absences):
        self.coverage, self.absences = coverage, absences

    def __call__(self, day):
        if any(start <= day <= end for start, end in self.absences):
            return 0.0
        return self.coverage.hours(day)


class CapacityTransferService:
    """Preview, record, withdraw and read temporary capacity transfers."""

    def __init__(self, db):
        self.db = db
        self.adjustments = CapacityAdjustmentService(db)

    async def _members(self, member_ids):
        rows = (await self.db.execute(
            select(TeamMember).options(selectinload(TeamMember.iteration).selectinload(Iteration.calendar),
                                       selectinload(TeamMember.iteration).selectinload(Iteration.project))
            .where(TeamMember.id.in_(member_ids))
        )).scalars().all()
        found = {row.id: row for row in rows}
        if set(found) != set(member_ids):
            raise _unavailable("Capacity row not found or inaccessible")
        return found

    @staticmethod
    def _today(members):
        """The latest current date among the rows' zones, so no row's past is changed."""
        zones = {member.iteration.project.timezone if member.iteration.project else member.iteration.calendar.timezone
                 for member in members}
        return max(working_today(zone) for zone in zones)

    async def _row_hours(self, member):
        from app.services.capacity_service import CapacityService
        capacity = CapacityService(self.db)
        return _RowHours(await capacity.coverage_for(member), await capacity.absence_ranges(member))

    async def _side(self, role, member, adjustment, hours, days, before, after, *, persisted=True, retained=None,
                    retained_persisted=True):
        effective = []
        for day in days:
            available = hours(day)
            prior, later = before(day), after(day)
            effective.append({
                "date": day,
                "availability_percent_before": prior,
                "availability_percent_after": later,
                "row_hours_before": None if available is None else _round(available * prior / 100),
                "row_hours_after": None if available is None else _round(available * later / 100),
            })
        return {
            "role": role,
            "member_id": member.id,
            "iteration_id": member.iteration_id,
            "project_id": member.iteration.project_id if member.iteration else None,
            "base_availability_percent": adjustment.base_availability_percent,
            "transferred_percent": _round(abs(adjustment.availability_percent - adjustment.base_availability_percent)),
            "availability_percent": adjustment.availability_percent,
            "adjustment": _response(adjustment, persisted=persisted),
            "retained": None if retained is None else _response(retained, persisted=retained_persisted),
            "effective_capacity": effective,
        }

    async def _person(self, member, start, end):
        projection = await self.adjustments._projection(member, start, end)
        return projection or []

    @staticmethod
    def _person_days(before, after):
        return [{
            "date": prior["date"],
            "available_hours": prior["available_hours"],
            "allocated_hours_before": prior["allocated_hours"],
            "allocated_hours_after": later["allocated_hours"],
            "overallocated_hours_before": prior["overallocated_hours"],
            "overallocated_hours_after": later["overallocated_hours"],
        } for prior, later in zip(before, after)]

    def _audit(self, action, member, adjustment, role, token, reason, details):
        from app.models.identity import CommandAudit
        authority = self.db.info.get("authority")
        self.db.add(CommandAudit(
            principal_id=getattr(authority, "principal_id", None),
            project_id=member.iteration.project_id if member.iteration else None,
            action=action,
            source=getattr(authority, "source", None) or "local",
            correlation_id=getattr(authority, "correlation_id", None) or token,
            reason=reason,
            # Each side's entry names only its own row; the shared group token links the sides.
            details={"group_token": token, "role": role, "member_id": member.id, "iteration_id": member.iteration_id,
                     "profile_id": member.profile_id, "adjustment_id": adjustment.id,
                     "start_date": adjustment.start_date.isoformat(), "end_date": adjustment.end_date.isoformat(),
                     "base_availability_percent": adjustment.base_availability_percent,
                     "availability_percent": adjustment.availability_percent, **details},
        ))

    # Recording a transfer -------------------------------------------------------------

    @preview_command
    async def preview(self, data):
        """Calculate both rows' effective capacity with the transfer, then roll everything back."""
        async with planning_input_reservation(self.db, TRANSFER_KIND, {"data": data}):
            return await self._transfer(data)

    @schedule_input_command(TRANSFER_KIND)
    async def apply(self, data, *, commit: bool = True):
        """Record every side of the transfer under the observed planning revisions."""
        return await self._transfer(data)

    async def _transfer(self, data):
        state = current_command(self.db)
        applying = state.mode == "apply"
        lent = {source.member_id: source.transferred_percent for source in data.sources}
        ids = sorted([data.target_member_id, *lent])
        members = await self._members(ids)
        target = members[data.target_member_id]
        sources = [members[member_id] for member_id in sorted(lent)]
        for member in members.values():
            if member.iteration_id is None or member.iteration is None:
                raise PlanningConflict("capacity_adjustment_unscheduled",
                    f"Add capacity row {member.id} to an iteration before transferring capacity.")
        profiles = {member.profile_id for member in members.values()}
        if None in profiles or len(profiles) != 1:
            raise PlanningConflict("capacity_transfer_profile_mismatch",
                "Transfer capacity only between rows of the same person or agent profile.")
        await self.db.execute(select(TeamMember.id).where(TeamMember.id.in_(ids)).order_by(TeamMember.id).with_for_update())
        start, end = data.start_date, data.end_date
        for member in members.values():
            iteration = member.iteration
            if start < iteration.start_date or end > iteration.end_date:
                raise PlanningConflict("capacity_adjustment_outside_iteration",
                    f"Transfer dates must lie within the iteration of capacity row {member.id}, "
                    f"{iteration.start_date} through {iteration.end_date}.")
        today = self._today(members.values())
        if start < today:
            raise PlanningConflict("capacity_transfer_in_past",
                f"A transfer takes effect from today, {today}, or later; earlier capacity is history.")

        adjustment = TeamMemberCapacityAdjustment
        active = list((await self.db.scalars(
            select(adjustment).where(adjustment.team_member_id.in_(ids), adjustment.withdrawn_at.is_(None))
            .order_by(adjustment.team_member_id, adjustment.start_date, adjustment.id).with_for_update()
        )).all())
        for row in active:
            if row.start_date <= end and start <= row.end_date:
                raise PlanningConflict("capacity_adjustment_overlap",
                    f"Adjustment {row.id} on capacity row {row.team_member_id} already covers some of these dates. "
                    "Withdraw it, or the transfer it belongs to, first.")
        for member_id in ids:
            if sum(1 for row in active if row.team_member_id == member_id) + 1 > MAX_ACTIVE_ADJUSTMENTS:
                raise PlanningConflict("capacity_adjustment_limit",
                    f"A capacity row holds at most {MAX_ACTIVE_ADJUSTMENTS} active adjustments.")

        percent = {}
        for source in sources:
            value = round(source.availability_percent - lent[source.id], 4)
            if value < 0:
                raise PlanningConflict("capacity_transfer_out_of_range",
                    f"Capacity row {source.id} can lend at most its own {source.availability_percent} percent.")
            percent[source.id] = value
        received = round(sum(lent.values()), 4)
        percent[target.id] = round(target.availability_percent + received, 4)
        if percent[target.id] > 100:
            raise PlanningConflict("capacity_transfer_out_of_range",
                f"Capacity row {target.id} can receive at most {round(100 - target.availability_percent, 4)} percent.")

        days = list(_days(start, end))
        for source in sources:
            await self.adjustments._refuse_reducing_issued_work(source, days)

        hours = {member.id: await self._row_hours(member) for member in members.values()}
        person_before = await self._person(target, start, end)
        authority = self.db.info.get("authority")
        principal_id = getattr(authority, "principal_id", None)
        token, now = str(uuid4()), utc_now()
        created = {member.id: adjustment(
            team_member_id=member.id, start_date=start, end_date=end, availability_percent=percent[member.id],
            base_availability_percent=member.availability_percent, reason=data.reason, group_token=token,
            created_by_principal_id=principal_id, created_at=now) for member in members.values()}
        self.db.add_all([created[member_id] for member_id in ids])
        await self.db.flush()
        person_after = await self._person(target, start, end)

        async def side(role, member):
            row = created[member.id]
            return await self._side(role, member, row, hours[member.id], days,
                                    lambda day: member.availability_percent, lambda day: row.availability_percent,
                                    persisted=applying)

        result = {
            "applied": applying,
            "action": "transfer",
            "group_token": token if applying else None,
            "withdrawal_group_token": None,
            "profile_id": target.profile_id,
            "start_date": start,
            "end_date": end,
            "returns_on": end + timedelta(days=1),
            "restored_from": None,
            "reason": data.reason,
            "target": await side("target", target),
            "sources": [await side("source", source) for source in sources],
            "person_capacity": self._person_days(person_before, person_after),
            "observed_revisions": dict(sorted(state.iterations.items())),
            "resulting_revisions": {key: value + 1 for key, value in sorted(state.iterations.items())} if applying else {},
            "planning_revision": state.planning_revision,
        }
        if applying:
            self._audit(TRANSFER_AUDIT_ACTION, target, created[target.id], "target", token, data.reason,
                        {"transferred_percent": received})
            for source in sources:
                self._audit(TRANSFER_AUDIT_ACTION, source, created[source.id], "source", token, data.reason,
                            {"transferred_percent": lent[source.id]})
            await self.db.flush()
        return result

    # Withdrawing a transfer -----------------------------------------------------------

    @preview_command
    async def preview_withdrawal(self, group_token, data):
        """Calculate the capacity every row gets back, then roll everything back."""
        async with planning_input_reservation(self.db, TRANSFER_KIND, {"group_token": group_token, "data": data}):
            return await self._withdraw(group_token, data)

    @schedule_input_command(TRANSFER_KIND)
    async def withdraw(self, group_token, data, *, commit: bool = True):
        """Return the lent capacity of every row of the transfer together."""
        return await self._withdraw(group_token, data)

    async def _group(self, group_token, *, lock=False):
        adjustment = TeamMemberCapacityAdjustment
        query = select(adjustment).where(adjustment.group_token == group_token).order_by(adjustment.team_member_id, adjustment.id)
        rows = list((await self.db.scalars(query.with_for_update() if lock else query)).all())
        with internal_authority(self.db):
            total = await self.db.scalar(select(func.count()).select_from(adjustment).where(adjustment.group_token == group_token))
        # Every row must be readable; a partly hidden transfer is reported as absent.
        if len({row.team_member_id for row in rows}) < 2 or len(rows) != total:
            raise _unavailable()
        return rows

    @staticmethod
    def _role(row):
        return "source" if row.availability_percent < row.base_availability_percent else "target"

    async def _withdraw(self, group_token, data):
        state = current_command(self.db)
        applying = state.mode == "apply"
        members = await self._members(await transfer_group_members(self.db, group_token) or [])
        ids = sorted(members)
        await self.db.execute(select(TeamMember.id).where(TeamMember.id.in_(ids)).order_by(TeamMember.id).with_for_update())
        rows = await self._group(group_token, lock=True)
        active = [row for row in rows if row.withdrawn_at is None]
        if not active:
            raise PlanningConflict("capacity_transfer_unavailable", "This transfer has already been withdrawn.")
        start, end = min(row.start_date for row in rows), max(row.end_date for row in rows)
        today = self._today(members.values())
        if end < today:
            raise PlanningConflict("capacity_transfer_ended",
                f"This transfer ended on {end}; its capacity has already returned and its dates are history.")
        restored_from = max(start, today)
        restored = list(_days(restored_from, end))
        for row in active:
            member = members[row.team_member_id]
            if member.availability_percent < row.availability_percent:
                await self.adjustments._refuse_reducing_issued_work(member, restored)

        hours = {member.id: await self._row_hours(member) for member in members.values()}
        profiled = next((member for member in members.values() if member.profile_id is not None), None)
        person_before = await self._person(profiled, start, end) if profiled else []
        authority = self.db.info.get("authority")
        principal_id = getattr(authority, "principal_id", None)
        token, now = str(uuid4()), utc_now()
        retained = {}
        for row in active:
            row.withdrawn_at, row.withdrawn_by_principal_id = now, principal_id
            row.withdrawal_reason, row.withdrawn_group_token = data.reason, token
            if row.start_date < restored_from:
                # Dates already elapsed keep the capacity they were lent; only the rest returns.
                retained[row.id] = TeamMemberCapacityAdjustment(
                    team_member_id=row.team_member_id, start_date=row.start_date, end_date=restored_from - timedelta(days=1),
                    availability_percent=row.availability_percent, base_availability_percent=row.base_availability_percent,
                    reason=row.reason, group_token=token, created_by_principal_id=principal_id, created_at=now)
        self.db.add_all(list(retained.values()))
        await self.db.flush()
        person_after = await self._person(profiled, start, end) if profiled else []

        days = list(_days(start, end))

        async def side(row):
            member = members[row.team_member_id]
            was_active = row in active

            def before(day):
                return row.availability_percent if was_active and row.start_date <= day <= row.end_date else member.availability_percent

            def after(day):
                kept = was_active and row.start_date <= day < restored_from
                return row.availability_percent if kept else (before(day) if not was_active else member.availability_percent)

            return await self._side(self._role(row), member, row, hours[member.id], days, before, after,
                                    retained=retained.get(row.id), retained_persisted=applying)

        target_row = next((row for row in rows if self._role(row) == "target"), rows[0])
        result = {
            "applied": applying,
            "action": "withdrawal",
            "group_token": group_token,
            "withdrawal_group_token": token if applying else None,
            "profile_id": profiled.profile_id if profiled else None,
            "start_date": start,
            "end_date": end,
            "returns_on": end + timedelta(days=1),
            "restored_from": restored_from,
            "reason": data.reason,
            "target": await side(target_row),
            "sources": [await side(row) for row in rows if row is not target_row],
            "person_capacity": self._person_days(person_before, person_after),
            "observed_revisions": dict(sorted(state.iterations.items())),
            "resulting_revisions": {key: value + 1 for key, value in sorted(state.iterations.items())} if applying else {},
            "planning_revision": state.planning_revision,
        }
        if not applying:
            for item in [result["target"], *result["sources"]]:
                item["adjustment"].withdrawn_group_token = None
        else:
            for row in active:
                kept = retained.get(row.id)
                self._audit(WITHDRAWAL_AUDIT_ACTION, members[row.team_member_id], row, self._role(row), group_token, data.reason,
                            {"withdrawal_group_token": token, "restored_from": restored_from.isoformat(),
                             "retained_adjustment_id": kept.id if kept else None})
            await self.db.flush()
        return result

    # Reading a transfer ---------------------------------------------------------------

    async def get(self, group_token):
        """Read every row of one transfer; the caller must be able to read all of them."""
        rows = await self._group(group_token)
        members = await self._members(sorted({row.team_member_id for row in rows}))
        days = []
        sides = []
        for row in rows:
            member = members[row.team_member_id]
            side = await self._side(self._role(row), member, row, None, days, None, None)
            sides.append(side)
        targets = [side for side in sides if side["role"] == "target"]
        target = targets[0] if targets else sides[0]
        withdrawn = [row for row in rows if row.withdrawn_at is not None]
        active = len(withdrawn) < len(rows)
        latest = max(withdrawn, key=lambda row: row.withdrawn_at) if withdrawn and not active else None
        first = rows[0]
        return {
            "group_token": group_token,
            "active": active,
            "profile_id": members[first.team_member_id].profile_id,
            "start_date": min(row.start_date for row in rows),
            "end_date": max(row.end_date for row in rows),
            "returns_on": max(row.end_date for row in rows) + timedelta(days=1),
            "reason": first.reason,
            "created_by_principal_id": first.created_by_principal_id,
            "created_at": first.created_at,
            "withdrawn_at": latest.withdrawn_at if latest else None,
            "withdrawal_reason": latest.withdrawal_reason if latest else None,
            "withdrawn_group_token": latest.withdrawn_group_token if latest else None,
            "target": target,
            "sources": [side for side in sides if side is not target],
        }
