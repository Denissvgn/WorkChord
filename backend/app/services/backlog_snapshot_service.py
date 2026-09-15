"""Project backlog recovery using the shared transactional snapshot store."""

import hashlib
import json
from datetime import date, datetime

from sqlalchemy import delete, func, or_, select

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import atomic_command, current_command, lock_backlog_project
from app.config import get_settings
from app.models.recovery import ApplicationSnapshot
from app.models.task import Task, TaskDependency
from app.models.task_brief import TaskBriefRevision, TaskProgressRecord, TaskReviewRecord
from app.services.snapshot_service import SnapshotService
from app.services.task_service import TaskService
from app.utils.time import utc_now


class BacklogSnapshotService:
    def __init__(self, db):
        self.db = db

    @atomic_command
    async def capture(self, project_id, reason="manual"):
        require_project(self.db, project_id, "read")
        state = current_command(self.db)
        key = ("project", project_id)
        if state.mode == "preview" or key in state.snapshots:
            return None
        await lock_backlog_project(self.db, project_id)
        roots, _ = await TaskService(self.db)._load_iteration_tree(None, project_id=project_id)
        serializer = SnapshotService(self.db)
        reason = serializer._validate_reason(reason)
        now = utc_now()
        payload = {"schema_version": 1, "scope": "project_backlog", "project_id": project_id,
                   "tasks": [serializer._task_to_export(task) for task in roots]}
        encoded = serializer._encode(payload)
        snapshot = ApplicationSnapshot(project_id=project_id, iteration_id=None, schema_version=3, input_revision=0,
            filename=f"snapshot_{now.strftime('%Y%m%d_%H%M%S_%f')}_{reason}.json", payload=payload,
            checksum=hashlib.sha256(encoded).hexdigest(), created_at=now,
            created_by_principal_id=getattr(self.db.info.get("authority"), "principal_id", None))
        self.db.add(snapshot)
        await self.db.flush()
        state.snapshots.add(key)
        old = list((await self.db.scalars(select(ApplicationSnapshot.id).where(ApplicationSnapshot.project_id == project_id)
            .order_by(ApplicationSnapshot.id.desc()).offset(get_settings().snapshot_retention_count))).all())
        if old:
            await self.db.execute(delete(ApplicationSnapshot).where(ApplicationSnapshot.id.in_(old)))
        return snapshot.id

    async def list(self, project_id):
        require_project(self.db, project_id)
        rows = (await self.db.scalars(select(ApplicationSnapshot).where(ApplicationSnapshot.project_id == project_id).order_by(ApplicationSnapshot.id.desc()).limit(get_settings().snapshot_retention_count))).all()
        return [{"id": row.id, "filename": row.filename, "created_at": row.created_at, "checksum": row.checksum} for row in rows]

    @atomic_command
    async def restore(self, project_id, snapshot_id, expected_versions, *, reason):
        require_project(self.db, project_id, "manage")
        if not reason.strip():
            raise ValueError("Restore requires a reason")
        await lock_backlog_project(self.db, project_id)
        snapshot = await self.db.scalar(select(ApplicationSnapshot).where(ApplicationSnapshot.id == snapshot_id, ApplicationSnapshot.project_id == project_id))
        if snapshot is None or hashlib.sha256(SnapshotService._encode(snapshot.payload)).hexdigest() != snapshot.checksum:
            raise ValueError("Snapshot unavailable or checksum mismatch")
        payload = snapshot.payload
        if payload.get("scope") != "project_backlog" or payload.get("project_id") != project_id:
            raise ValueError("Snapshot scope does not match the project")
        service = TaskService(self.db)
        _, current = await service._load_iteration_tree(None, project_id=project_id)
        if {task.id: task.version for task in current.values()} != expected_versions:
            raise AuthorityError("backlog_version_conflict", "The backlog changed. Reload all current task versions before restoring.", 409)
        await service._require_unclaimed_structure(current)
        await self.capture(project_id, "before_restore")
        rows, pending = [], [(row, None) for row in payload["tasks"]]
        while pending:
            row, parent_id = pending.pop()
            rows.append((row, parent_id))
            pending.extend((child, row["id"]) for child in row.get("children", []))
        ids = {row["id"] for row, _ in rows}
        if len(ids) != len(rows):
            raise ValueError("Snapshot contains duplicate task IDs")
        # Existence checks avoid revealing a colliding task's inaccessible details.
        with internal_authority(self.db):
            collision = await self.db.scalar(select(Task.id).where(Task.id.in_(ids), or_(Task.project_id != project_id, Task.project_id.is_(None), Task.iteration_id.is_not(None))).limit(1))
        if collision is not None:
            raise ValueError("A snapshot task ID is already in another scope")
        removed = set(current) - ids
        outside = await self.db.scalar(select(TaskDependency.id).where(TaskDependency.depends_on_id.in_(removed), TaskDependency.task_id.notin_(removed)).limit(1))
        if outside is not None:
            raise ValueError("Restore would remove a referenced task")
        await self.db.execute(delete(TaskDependency).where(TaskDependency.task_id.in_(set(current) | ids)))
        for task in current.values():
            task.parent_id = None
        await self.db.flush()
        for task in current.values():
            if task.id in removed:
                await self.db.delete(task)
        await self.db.flush()
        for row, _ in rows:
            task = await self.db.get(Task, row["id"])
            if task is None:
                versions = [row.get("version", 1)]
                for model in (TaskBriefRevision, TaskProgressRecord, TaskReviewRecord):
                    versions.append(await self.db.scalar(select(func.max(model.task_version)).where(model.original_task_id == row["id"])) or 0)
                task = Task(id=row["id"], project_id=project_id, version=max(versions) + 1)
                self.db.add(task)
            else:
                await service.reserve_task_version(task, task.version)
            for name in ("title", "description", "priority", "effort_hours", "nominal_day_hours", "estimate_provenance", "owner_profile_id", "ownership_provenance",
                         "status", "is_summary", "is_optional", "is_deferred", "sort_order", "external_key", "source", "source_url", "milestone_id", "blocked_reason", "canceled_reason", "execution_mode"):
                if name in row:
                    setattr(task, name, row[name])
            task.tags = json.dumps(row.get("tags", []))
            task.iteration_id = task.assignee_id = task.start_date = task.end_date = None
            task.parent_id = None
            for name in ("actual_start_date", "actual_end_date", "min_start_date", "max_end_date"):
                setattr(task, name, date.fromisoformat(row[name]) if row.get(name) else None)
            for name in ("started_at", "resolved_at", "canceled_at"):
                setattr(task, name, datetime.fromisoformat(row[name]) if row.get(name) else None)
            task.executed_by_principal_id = row.get("executed_by_principal_id")
            task.progress = task.accepted_at = task.accepted_by_principal_id = task.accepted_version = None
            from app.services.task_domain_service import require_owner
            await require_owner(self.db, task.owner_profile_id, project_id)
            await self.db.flush()
            from app.services.task_brief_service import TaskBriefService
            await TaskBriefService(self.db).restore_brief(task, row)
            await service.record_task_event(task.id, "backlog_snapshot_restored", {"snapshot_id": snapshot_id, "reason": reason, "version": task.version})
        await self.db.flush()
        for row, parent_id in rows:
            task = await self.db.get(Task, row["id"])
            task.parent_id = parent_id
            for target in row.get("dependencies", []):
                if target not in ids:
                    raise ValueError("Snapshot dependency is outside its complete backlog graph")
                self.db.add(TaskDependency(task_id=task.id, depends_on_id=target))
        await self.db.flush()
        roots, _ = await service._load_iteration_tree(None, project_id=project_id)
        return [service.task_to_response(task) for task in roots]
