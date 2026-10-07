"""Authorized scalar totals and exports without exposing other authors' records."""

import csv
from io import StringIO

from sqlalchemy import and_, case, func, select, union
from sqlalchemy.orm import aliased

from app.authority import AuthorityError, internal_authority
from app.models.task import Task
from app.models.time_entry import TimeEntry
from app.query_limits import CollectionLimitExceededError
from app.services.time_entry_service import TimeEntryService


class TimeReportService:
    def __init__(self, db):
        self.db = db
        self.ledger = TimeEntryService(db)

    async def statement(self, project_id, start, end, scope):
        author = self.ledger.principal_id()
        await self.ledger.project(project_id)
        self.ledger.check_window(start, end)
        if scope not in {"mine", "project"}:
            raise ValueError("Use personal or authorized project totals")
        can_manage = self.db.info["authority"].allows(project_id, "manage")
        if scope == "project" and not can_manage:
            raise AuthorityError("project_time_totals_required", "Project manager permission is required for team totals.")
        conditions = [TimeEntry.project_id == project_id, TimeEntry.voided.is_(False),
            TimeEntry.work_date >= start, TimeEntry.work_date <= end]
        if scope == "mine":
            conditions.append(TimeEntry.principal_id == author)
        # Select scalar aggregates only. Never hydrate notes, revisions or author identities for team totals.
        grouped = select(TimeEntry.task_id.label("task_id"), func.sum(TimeEntry.minutes).label("minutes"),
            func.count(TimeEntry.id).label("entry_count"), func.min(TimeEntry.task_title).label("recorded_title"))
        grouped = grouped.where(*conditions, TimeEntry.task_id.is_not(None)).group_by(TimeEntry.task_id).subquery()
        child = aliased(Task)
        leaf = and_(Task.is_summary.is_(False), ~select(child.id).where(child.parent_id == Task.id).exists())
        cohort = union(select(Task.id.label("task_id")).where(Task.project_id == project_id, leaf),
            select(grouped.c.task_id)).subquery()
        current_leaf = and_(Task.id.is_not(None), leaf)
        rows = select(cohort.c.task_id, func.coalesce(Task.title, grouped.c.recorded_title).label("task_title"),
            grouped.c.minutes.label("recorded_minutes"), func.coalesce(grouped.c.entry_count, 0).label("entry_count"),
            case((current_leaf, Task.effort_hours), else_=None).label("estimate_hours"),
            current_leaf.label("current_leaf"))
        rows = rows.select_from(cohort.outerjoin(grouped, grouped.c.task_id == cohort.c.task_id)
            .outerjoin(Task, and_(Task.id == cohort.c.task_id, Task.project_id == project_id)))
        with internal_authority(self.db):
            project_work = await self.db.scalar(select(func.sum(TimeEntry.minutes)).where(*conditions, TimeEntry.task_id.is_(None)))
        return rows, can_manage, project_work

    @staticmethod
    def item(row):
        return {"task_id": row.task_id, "task_title": row.task_title,
            "recorded_minutes": row.recorded_minutes, "entry_count": row.entry_count,
            "estimate_hours": row.estimate_hours,
            "estimate_state": "unavailable" if not row.current_leaf else "unknown" if row.estimate_hours is None else "known"}

    async def page(self, project_id, start, end, *, scope="mine", after_id=0, upper_id=None, limit=50):
        if after_id < 0 or upper_id is not None and upper_id < 0 or not 1 <= limit <= 100:
            raise ValueError("Use bounded report page parameters")
        query, can_manage, project_work = await self.statement(project_id, start, end, scope)
        all_rows = query.subquery()
        with internal_authority(self.db):
            totals = (await self.db.execute(select(func.count(),
                func.sum(case((all_rows.c.entry_count > 0, 1), else_=0)),
                func.sum(all_rows.c.recorded_minutes), func.sum(all_rows.c.estimate_hours),
                func.count(all_rows.c.estimate_hours)).select_from(all_rows))).one()
            if upper_id is None:
                upper_id = await self.db.scalar(select(func.max(all_rows.c.task_id))) or 0
            rows = (await self.db.execute(select(all_rows).where(all_rows.c.task_id > after_id,
                all_rows.c.task_id <= upper_id).order_by(all_rows.c.task_id).limit(limit + 1))).all()
        recorded = None if totals[2] is None and project_work is None else (totals[2] or 0) + (project_work or 0)
        return {"project_id": project_id, "scope": scope, "start": start, "end": end,
            "items": [self.item(row) for row in rows[:limit]], "has_more": len(rows) > limit,
            "next_after_id": rows[limit - 1].task_id if len(rows) > limit else None, "upper_id": upper_id,
            "can_view_project_totals": can_manage,
            "totals": {"task_count": totals[0], "tasks_with_records": totals[1] or 0,
                "recorded_minutes": recorded, "project_work_minutes": project_work,
                "known_estimate_hours": totals[3], "tasks_with_estimates": totals[4]}}

    @staticmethod
    def csv(rows):
        def cell(value):
            if value is None:
                return ""
            text = str(value)
            if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n")):
                return "'" + text
            return text
        output = StringIO(newline="")
        writer = csv.writer(output)
        writer.writerows([cell(value) for value in row] for row in rows)
        return "\ufeff" + output.getvalue()

    async def export(self, project_id, start, end, *, scope="mine", kind="totals"):
        if kind not in {"totals", "entries"}:
            raise ValueError("Choose totals or your personal entries")
        query, _, project_work = await self.statement(project_id, start, end, scope)
        if kind == "totals":
            with internal_authority(self.db):
                rows = (await self.db.execute(query.order_by("task_id").limit(5001))).all()
            if len(rows) > 5000:
                raise CollectionLimitExceededError("Time report export", 5000)
            values = [["task_id", "task_title", "recorded_minutes", "current_estimate_hours", "estimate_state"]]
            for row in rows:
                item = self.item(row)
                values.append([item["task_id"], item["task_title"], item["recorded_minutes"], item["estimate_hours"], item["estimate_state"]])
            values.append([None, "Project work without a task", project_work, None, "unavailable"])
        else:
            if scope != "mine":
                raise AuthorityError("private_time_entries", "Only authors may export individual time records.")
            author = self.ledger.principal_id()
            rows = (await self.db.scalars(select(TimeEntry).where(TimeEntry.project_id == project_id,
                TimeEntry.principal_id == author, TimeEntry.work_date >= start, TimeEntry.work_date <= end)
                .order_by(TimeEntry.id).limit(5001))).all()
            if len(rows) > 5000:
                raise CollectionLimitExceededError("Personal time-entry export", 5000)
            values = [["id", "task_id", "task_title", "work_date", "timezone", "minutes", "note", "version", "voided"]]
            values.extend([[row.id, row.task_id, row.task_title, row.work_date, row.timezone,
                row.minutes, row.note, row.version, row.voided] for row in rows])
        return self.csv(values)
