"""Attributable minute commands with private reads and independent version history."""

import hashlib
import json

from sqlalchemy import func, select, update
from sqlalchemy.orm import raiseload

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import PlanningConflict, atomic_command
from app.config import get_settings
from app.models.identity import Principal
from app.models.project import Project
from app.models.task import Task
from app.models.time_entry import TimeEntry, TimeEntryRevision
from app.schemas.time_entry import TimeEntryResponse, TimeRevisionResponse
from app.utils.time import utc_now


class TimeEntryVersionConflict(PlanningConflict):
    def __init__(self, expected, entry):
        super().__init__("time_entry_version_conflict", "This entry changed. Reload it before applying your correction.")
        self.expected, self.entry = expected, entry

    def detail(self):
        return {**super().detail(), "expected_version": self.expected, "current_entry": self.entry}


class TimeEntryService:
    def __init__(self, db):
        self.db = db

    def principal_id(self):
        if not get_settings().time_entries_enabled:
            raise AuthorityError("time_entries_disabled", "Time entry is disabled for this workspace.", 404)
        authority = self.db.info.get("authority")
        if authority is None or authority.kind != "human" or authority.principal_id is None:
            raise AuthorityError("human_identity_required", "Sign in with a human account to record time.")
        return authority.principal_id

    async def project(self, project_id, *, writing=False):
        require_project(self.db, project_id)
        project = await self.db.scalar(select(Project.id).where(Project.id == project_id))
        if project is None:
            raise LookupError("Project not found or inaccessible")
        authority = self.db.info["authority"]
        if writing and not any(authority.allows(project_id, action) for action in ("edit", "execute", "review")):
            raise AuthorityError()
        return project

    async def lock_author(self):
        principal_id = self.principal_id()
        # Serialize retries, corrections and daily totals without reserving task/planning revisions.
        with internal_authority(self.db):
            await self.db.execute(update(Principal).where(Principal.id == principal_id)
                .values(enabled=Principal.enabled).execution_options(synchronize_session=False))
            principal = await self.db.get(Principal, principal_id, populate_existing=True)
        if principal is None or principal.kind != "human" or not principal.enabled:
            raise AuthorityError("account_disabled", "This account is unavailable.", 401)
        return principal_id

    def authorize_object(self, obj):
        self.db.info.setdefault("time_entry_commands", set()).add(id(obj))

    @staticmethod
    def serialize(entry):
        return TimeEntryResponse(**{name: getattr(entry, name) for name in TimeEntryResponse.model_fields}).model_dump(mode="json")

    async def get(self, entry_id):
        principal_id = self.principal_id()
        entry = await self.db.scalar(select(TimeEntry).where(TimeEntry.id == entry_id,
            TimeEntry.principal_id == principal_id).execution_options(populate_existing=True))
        if entry is None:
            raise LookupError("Time entry not found or inaccessible")
        await self.project(entry.project_id)
        return entry

    @staticmethod
    def check_window(start, end):
        if start is not None and end is not None and (end < start or (end - start).days > 366):
            raise ValueError("Use an ordered date range of at most 366 days")

    async def list(self, *, project_id=None, task_id=None, start=None, end=None, after_id=0,
                   upper_id=None, limit=50, include_voided=False):
        principal_id = self.principal_id()
        self.check_window(start, end)
        if not 1 <= limit <= 100 or after_id < 0 or upper_id is not None and upper_id < 0:
            raise ValueError("Use bounded time-entry page parameters")
        if project_id is not None:
            await self.project(project_id)
        conditions = [TimeEntry.principal_id == principal_id,
            TimeEntry.project_id.in_(select(Project.id))]
        if project_id is not None:
            conditions.append(TimeEntry.project_id == project_id)
        if task_id is not None:
            conditions.append(TimeEntry.task_id == task_id)
        if start is not None:
            conditions.append(TimeEntry.work_date >= start)
        if end is not None:
            conditions.append(TimeEntry.work_date <= end)
        if not include_voided:
            conditions.append(TimeEntry.voided.is_(False))
        if upper_id is None:
            upper_id = await self.db.scalar(select(func.max(TimeEntry.id)).where(*conditions)) or 0
        rows = (await self.db.scalars(select(TimeEntry).where(*conditions, TimeEntry.id > after_id,
            TimeEntry.id <= upper_id).order_by(TimeEntry.id).limit(limit + 1))).all()
        return {"items": [self.serialize(row) for row in rows[:limit]], "has_more": len(rows) > limit,
            "next_after_id": rows[limit - 1].id if len(rows) > limit else None, "upper_id": upper_id}

    async def check_day_total(self, principal_id, work_date, minutes, *, exclude_id=None):
        # Count the author's other scopes internally; expose neither their identities nor notes.
        with internal_authority(self.db):
            query = select(func.sum(TimeEntry.minutes)).where(TimeEntry.principal_id == principal_id,
                TimeEntry.work_date == work_date, TimeEntry.voided.is_(False))
            if exclude_id is not None:
                query = query.where(TimeEntry.id != exclude_id)
            total = await self.db.scalar(query) or 0
        if total + minutes > 1440:
            raise ValueError("A person's recorded time for one work date cannot exceed 1440 minutes")

    async def append_revision(self, entry, reason):
        revision = TimeEntryRevision(entry_id=entry.id, project_id=entry.project_id,
            principal_id=entry.principal_id, version=entry.version, work_date=entry.work_date,
            timezone=entry.timezone, minutes=entry.minutes, note=entry.note, voided=entry.voided,
            reason=reason, created_at=entry.updated_at)
        self.authorize_object(revision)
        self.db.add(revision)
        await self.db.flush()

    @atomic_command
    async def create(self, data):
        principal_id = await self.lock_author()
        payload = data.model_dump(mode="json")
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        with internal_authority(self.db):
            existing = await self.db.scalar(select(TimeEntry).where(TimeEntry.principal_id == principal_id,
                TimeEntry.request_id == str(data.request_id)).execution_options(populate_existing=True))
        if existing is not None:
            await self.project(existing.project_id)
            if existing.creation_digest != digest:
                raise PlanningConflict("time_entry_request_conflict", "This request ID was already used for different recorded time.")
            return self.serialize(existing)
        await self.project(data.project_id, writing=True)
        title = None
        if data.task_id is not None:
            task = await self.db.scalar(select(Task).options(raiseload("*")).where(Task.id == data.task_id, Task.project_id == data.project_id))
            if task is None:
                raise LookupError("Task not found or inaccessible in this project")
            with internal_authority(self.db):
                await self.db.execute(update(Task).where(Task.id == task.id).values(id=Task.id, updated_at=Task.updated_at)
                    .execution_options(synchronize_session=False))
            task = await self.db.scalar(select(Task).options(raiseload("*")).where(Task.id == data.task_id, Task.project_id == data.project_id)
                .execution_options(populate_existing=True))
            if task is None:
                raise LookupError("Task changed project or became unavailable")
            with internal_authority(self.db):
                child = await self.db.scalar(select(Task.id).where(Task.parent_id == task.id).limit(1))
            if task.is_summary or child is not None:
                raise ValueError("Record task time against leaf work, or record project work without a task")
            title = task.title
        await self.check_day_total(principal_id, data.work_date, data.minutes)
        now = utc_now()
        entry = TimeEntry(project_id=data.project_id, task_id=data.task_id, task_title=title,
            principal_id=principal_id, request_id=str(data.request_id), creation_digest=digest,
            work_date=data.work_date, timezone=data.timezone, minutes=data.minutes, note=data.note,
            version=1, voided=False, created_at=now, updated_at=now)
        self.authorize_object(entry)
        self.db.add(entry)
        await self.db.flush()
        await self.append_revision(entry, "Time recorded")
        return self.serialize(entry)

    @atomic_command
    async def correct(self, entry_id, data, *, void=False):
        await self.lock_author()
        entry = await self.get(entry_id)
        if data.expected_version != entry.version:
            raise TimeEntryVersionConflict(data.expected_version, self.serialize(entry))
        if entry.voided:
            raise PlanningConflict("time_entry_voided", "This entry is voided. Record a new entry instead.")
        if not void:
            await self.check_day_total(entry.principal_id, data.work_date, data.minutes, exclude_id=entry.id)
            entry.work_date, entry.timezone, entry.minutes, entry.note = data.work_date, data.timezone, data.minutes, data.note
        entry.version += 1
        entry.voided = void
        entry.updated_at = utc_now()
        self.authorize_object(entry)
        await self.db.flush()
        await self.append_revision(entry, data.reason)
        return self.serialize(entry)

    async def history(self, entry_id, *, after_version=0, limit=50):
        entry = await self.get(entry_id)
        if after_version < 0 or not 1 <= limit <= 100:
            raise ValueError("Use bounded correction history parameters")
        rows = (await self.db.scalars(select(TimeEntryRevision).where(TimeEntryRevision.entry_id == entry.id,
            TimeEntryRevision.principal_id == entry.principal_id, TimeEntryRevision.version > after_version)
            .order_by(TimeEntryRevision.version).limit(limit + 1))).all()
        return {"items": [TimeRevisionResponse(**{name: getattr(row, name) for name in TimeRevisionResponse.model_fields})
            .model_dump(mode="json") for row in rows[:limit]], "has_more": len(rows) > limit,
            "next_after_version": rows[limit - 1].version if len(rows) > limit else None}
