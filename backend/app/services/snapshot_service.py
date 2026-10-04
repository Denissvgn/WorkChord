"""Snapshot service for iteration state backups."""
from app.commands import atomic_command, current_command, lock_iterations
from app.config import get_settings
from app.models.recovery import ApplicationSnapshot, LegacySnapshotImport
from sqlalchemy import select, delete
import hashlib
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.iteration_service import IterationService
from app.services.team_service import TeamService
from app.utils.time import utc_now


# Base directory for snapshots
SNAPSHOTS_DIR = Path("data/snapshots")
SNAPSHOT_REASON_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$")
SNAPSHOT_FILENAME_PATTERN = re.compile(
    r"^snapshot_\d{8}_\d{6}(?:_\d{6})?_[A-Za-z0-9][A-Za-z0-9._-]{0,119}\.json$"
)


class SnapshotPathError(ValueError):
    """Raised when a snapshot name cannot be safely resolved inside its iteration directory."""


class SnapshotService:
    """Service for creating and managing iteration snapshots."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _get_snapshot_dir(self, iteration_id: int) -> Path:
        """Get the snapshot directory for an iteration."""
        return SNAPSHOTS_DIR / str(iteration_id)

    def _validate_reason(self, reason: str) -> str:
        """Return a filename-safe snapshot reason or reject the caller value."""
        normalized = str(reason).strip()
        if not SNAPSHOT_REASON_PATTERN.fullmatch(normalized):
            raise SnapshotPathError(
                "Snapshot reason must contain only letters, numbers, dots, underscores, and hyphens."
            )
        return normalized

    def _snapshot_path(
        self,
        iteration_id: int,
        filename: str,
        *,
        reject_symlink: bool = True,
    ) -> Path:
        """Resolve a generated basename beneath the iteration snapshot directory."""
        if not isinstance(filename, str) or not SNAPSHOT_FILENAME_PATTERN.fullmatch(filename):
            raise SnapshotPathError("Invalid snapshot filename.")
        if Path(filename).name != filename or Path(filename).is_absolute():
            raise SnapshotPathError("Invalid snapshot filename.")

        snapshot_dir = self._get_snapshot_dir(iteration_id).resolve(strict=False)
        candidate = snapshot_dir / filename
        if reject_symlink and candidate.is_symlink():
            raise SnapshotPathError("Snapshot symlinks are not allowed.")
        resolved_candidate = candidate.resolve(strict=False)
        try:
            resolved_candidate.relative_to(snapshot_dir)
        except ValueError as exc:
            raise SnapshotPathError("Snapshot path escapes its iteration directory.") from exc
        return resolved_candidate

    def _snapshot_files(self, iteration_id: int) -> list[Path]:
        """Return validated generated snapshot files without following unsafe links."""
        snapshot_dir = self._get_snapshot_dir(iteration_id)
        if not snapshot_dir.exists():
            return []

        validated: list[Path] = []
        for candidate in snapshot_dir.glob("snapshot_*.json"):
            resolved = self._snapshot_path(iteration_id, candidate.name)
            if resolved.is_file():
                validated.append(resolved)
        return validated

    async def build_snapshot_data(
        self,
        iteration_id: int,
        reason: str = "auto",
    ) -> dict | None:
        """Build one JSON-native immutable representation of an iteration."""
        reason = self._validate_reason(reason)
        iteration_service = IterationService(self.db)
        iteration = await iteration_service.get_by_id(iteration_id)
        if not iteration:
            return None

        from app.services.task_service import TaskService

        tasks = await TaskService(self.db).get_by_iteration(iteration_id)
        team_members = await TeamService(self.db).get_by_iteration(iteration_id)
        created_at = utc_now()

        return {
            "iteration": {
                "id": iteration.id,
                "name": iteration.name,
                "start_date": iteration.start_date.isoformat(),
                "end_date": iteration.end_date.isoformat(),
                "calendar_id": iteration.calendar_id,
                "project_id": iteration.project_id,
                "manager_email": iteration.manager_email,
            },
            "team_members": [
                self._member_to_export(member)
                for member in team_members
            ],
            "tasks": [
                self._task_to_export(task)
                for task in tasks
            ],
            "snapshot_info": {
                "schema_version": 2,
                "created_at": created_at.isoformat(),
                "reason": reason,
            },
        }

    @atomic_command
    async def create_snapshot(self, iteration_id: int, reason: str = "auto") -> str | None:
        """Persist one pre-command recovery point and retention in the owner's transaction."""
        state = current_command(self.db)
        if iteration_id is None or state.mode == "preview" or iteration_id in state.snapshots:
            return None
        revisions = await lock_iterations(self.db, [iteration_id])
        payload = await self.build_snapshot_data(iteration_id, reason)
        if payload is None:
            return None
        encoded = self._encode(payload)
        created = utc_now()
        for offset in range(1024):
            name = f"snapshot_{(created + timedelta(microseconds=offset)).strftime('%Y%m%d_%H%M%S_%f')}_{self._validate_reason(reason)}.json"
            if await self.db.scalar(select(ApplicationSnapshot.id).where(ApplicationSnapshot.iteration_id == iteration_id, ApplicationSnapshot.filename == name)) is None:
                break
        else:
            raise ValueError("Snapshot filename reservation exhausted")
        authority = self.db.info.get("authority")
        self.db.add(ApplicationSnapshot(iteration_id=iteration_id, filename=name, schema_version=2,
            input_revision=revisions[iteration_id], payload=payload, checksum=hashlib.sha256(encoded).hexdigest(),
            created_by_principal_id=getattr(authority, "principal_id", None), created_at=created))
        await self.db.flush()
        state.snapshots.add(iteration_id)
        await self.rotate_snapshots(iteration_id)
        return name

    @staticmethod
    def _encode(payload: dict) -> bytes:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        if len(encoded) > get_settings().snapshot_max_bytes:
            raise ValueError("Application snapshot exceeds the configured payload limit")
        return encoded

    @atomic_command
    async def rotate_snapshots(self, iteration_id: int, max_count: int | None = None) -> int:
        if current_command(self.db).mode == "preview":
            return 0
        await lock_iterations(self.db, [iteration_id])
        count = max_count if max_count is not None else get_settings().snapshot_retention_count
        if not 1 <= count <= 100:
            raise ValueError("Snapshot retention must be between 1 and 100")
        ids = list((await self.db.scalars(select(ApplicationSnapshot.id).where(ApplicationSnapshot.iteration_id == iteration_id)
                                        .order_by(ApplicationSnapshot.created_at.desc(), ApplicationSnapshot.id.desc()).offset(count))).all())
        if ids:
            await self.db.execute(delete(ApplicationSnapshot).where(ApplicationSnapshot.id.in_(ids)))
        return len(ids)

    async def list_snapshots(self, iteration_id: int) -> list[dict]:
        rows = (await self.db.scalars(select(ApplicationSnapshot).where(ApplicationSnapshot.iteration_id == iteration_id)
                                     .order_by(ApplicationSnapshot.created_at.desc(), ApplicationSnapshot.id.desc()).limit(100))).all()
        rows = [row for row in rows if self._payload_visible(row.payload)]
        return [{"filename": row.filename, "created_at": row.created_at.isoformat(),
                 "reason": row.payload.get("snapshot_info", {}).get("reason", "unknown"),
                 "size_bytes": len(self._encode(row.payload)), "schema_version": row.schema_version,
                 "checksum": row.checksum, "provenance": row.provenance, "input_revision": row.input_revision} for row in rows]

    async def get_snapshot(self, iteration_id: int, filename: str) -> dict | None:
        if not SNAPSHOT_FILENAME_PATTERN.fullmatch(filename):
            raise SnapshotPathError("Invalid snapshot filename")
        row = await self.db.scalar(select(ApplicationSnapshot).where(ApplicationSnapshot.iteration_id == iteration_id, ApplicationSnapshot.filename == filename))
        if row is None or not self._payload_visible(row.payload):
            return None
        if hashlib.sha256(self._encode(row.payload)).hexdigest() != row.checksum:
            raise SnapshotPathError("Snapshot checksum does not match stored content")
        return row.payload

    def _payload_visible(self, payload):
        """Historical JSON must not bypass current project visibility through an unscoped iteration."""
        authority = self.db.info.get("authority")
        if authority is None or authority.operator or authority.local:
            return True
        tasks = list(payload.get("tasks", []))
        while tasks:
            task = tasks.pop()
            if not authority.allows(task.get("project_id"), "read"):
                return False
            tasks.extend(task.get("children", []))
        return True

    @atomic_command
    async def import_legacy(self, iteration_id: int, *, dry_run=True, limit=25) -> list[dict]:
        """Inventory legacy files without inventing trust for ambiguous preview-era content."""
        if not 1 <= limit <= 100:
            raise ValueError("Legacy import limit must be between 1 and 100")
        results = []
        for path in sorted(self._snapshot_files(iteration_id))[:limit]:
            if path.stat().st_size > get_settings().snapshot_max_bytes:
                results.append({"filename": path.name, "disposition": "rejected", "reason": "payload limit"})
                continue
            raw = path.read_bytes()
            checksum = hashlib.sha256(raw).hexdigest()
            reason = "Legacy files may originate from rolled-back previews; independent provenance is unavailable"
            disposition = "quarantined"
            try:
                value = json.loads(raw)
                if not isinstance(value, dict) or value.get("iteration", {}).get("id") != iteration_id or not isinstance(value.get("tasks"), list):
                    raise ValueError("Snapshot scope or shape is invalid")
            except (ValueError, TypeError) as exc:
                reason, disposition = str(exc), "rejected"
            existing = await self.db.get(LegacySnapshotImport, checksum)
            if not dry_run and existing is None:
                self.db.add(LegacySnapshotImport(checksum=checksum, iteration_id=iteration_id,
                    source_name=path.name, disposition=disposition, reason=reason))
            results.append({"filename": path.name, "checksum": checksum,
                "disposition": disposition, "reason": reason, "already_recorded": existing is not None})
        return results

    @atomic_command
    async def restore(self, iteration_id: int, filename: str, *, expected_revision=None) -> dict:
        """Restore supported IDs in place, retain history and invalidate current execution acceptance."""
        from app.models.task import Task, TaskDependency
        from app.models.team_member import TeamMember, Vacation
        from app.models.iteration import Iteration
        from app.models.recovery import TaskScheduleBaseline
        from app.authority import require_operator
        if self.db.info.get("authority") is not None or get_settings().workchord_auth_mode == "managed":
            require_operator(self.db)
        from app.services.task_service import TaskService
        from app.routers.snapshots import _validate_snapshot_task_payloads
        from datetime import date

        await lock_iterations(self.db, [iteration_id], expected={iteration_id: expected_revision} if expected_revision is not None else None, require_expected=True, revision_field="expected_revision")
        payload = await self.get_snapshot(iteration_id, filename)
        if payload is None:
            raise LookupError("Snapshot not found or inaccessible")
        if payload.get("snapshot_info", {}).get("schema_version") != 2:
            raise ValueError("Legacy snapshot identity/provenance needs explicit operator reconciliation")
        service = TaskService(self.db)
        await _validate_snapshot_task_payloads(iteration_id, payload, service)
        current = await service.get_all_tasks(iteration_id)
        await service._require_unclaimed_structure([task.id for task in current])
        recovery = await self.create_snapshot(iteration_id, "before_restore")
        iteration = await self.db.get(Iteration, iteration_id)
        saved_iteration = payload["iteration"]
        if saved_iteration.get("project_id") != iteration.project_id:
            raise ValueError("Restore cannot change project authority; reconcile the iteration scope first")
        for key in ["name", "calendar_id", "manager_email"]:
            if key in saved_iteration:
                setattr(iteration, key, saved_iteration[key])
        for key in ["start_date", "end_date"]:
            setattr(iteration, key, date.fromisoformat(saved_iteration[key]))
        members = {}
        for data in payload["team_members"]:
            if not isinstance(data.get("id"), int):
                raise ValueError("Snapshot capacity identity is unknown")
            member = await self.db.get(TeamMember, data["id"])
            if member is not None and member.iteration_id not in (None, iteration_id):
                raise ValueError("Snapshot capacity ID belongs to another iteration")
            if member is None:
                member = TeamMember(id=data["id"], iteration_id=iteration_id)
                self.db.add(member)
            elif "profile_id" in data and member.profile_id != data["profile_id"]:
                from app.services.team_service import TeamService
                await TeamService(self.db).detach_absence_adapters(member, data["profile_id"])
            for key in ["name", "position", "profile_id", "availability_percent", "professionalism_coefficient", "operational_utilization"]:
                if key in data:
                    setattr(member, key, data[key])
            member.iteration_id = iteration_id
            members[member.id] = member
            # Person availability is shared across iterations and is never restored from one plan.
            if member.profile_id is not None:
                continue
            await self.db.execute(delete(Vacation).where(Vacation.team_member_id == member.id, Vacation.profile_absence_id.is_(None)))
            for vacation in data.get("vacations", []):
                start, end = date.fromisoformat(vacation["start_date"]), date.fromisoformat(vacation["end_date"])
                if end < start:
                    raise ValueError("Snapshot absence dates are invalid")
                self.db.add(Vacation(team_member_id=member.id, start_date=start, end_date=end))
        await self.db.flush()
        flat = []
        pending = [(row, None) for row in payload["tasks"]]
        while pending:
            row, parent_id = pending.pop()
            if not isinstance(row.get("id"), int):
                raise ValueError("Snapshot task identity is unknown")
            flat.append((row, parent_id))
            pending.extend((child, row["id"]) for child in row.get("children", []))
        ids = {row["id"] for row, _ in flat}
        from app.services.delivery_dependency_service import DeliveryDependencyService
        from app.models.delivery_dependency import DeliveryDependency
        removed_ids = {task.id for task in current} - ids
        self.db.info.setdefault("delivery_changed_nodes", set()).update(("task", task_id) for task_id in ids)
        await DeliveryDependencyService(self.db).require_unreferenced(removed_ids)
        await self.db.execute(delete(DeliveryDependency).where(DeliveryDependency.task_id.in_(removed_ids)))
        outside = await self.db.scalar(select(TaskDependency.task_id).where(TaskDependency.depends_on_id.in_({t.id for t in current} - ids), TaskDependency.task_id.notin_(ids)).limit(1))
        if outside is not None:
            raise ValueError("Restoring would remove a referenced task")
        await self.db.execute(delete(TaskDependency).where(TaskDependency.task_id.in_([t.id for t in current])))
        for task in current:
            if task.id not in ids:
                await self.db.delete(task)
        await self.db.flush()
        for row, parent_id in flat:
            task = await self.db.get(Task, row["id"])
            if task is not None and task.iteration_id != iteration_id:
                raise ValueError("Snapshot task ID belongs to another iteration")
            from app.services.task_recovery_service import reserve_restored_task_version
            version = await reserve_restored_task_version(self.db, row["id"], task, row.get("version", 1))
            if task is None:
                task = Task(id=row["id"], iteration_id=iteration_id, version=version)
                self.db.add(task)
            for key in ["title", "description", "priority", "effort_days", "effort_hours", "status", "project_id", "milestone_id", "is_optional", "is_deferred", "sort_order", "external_key", "source", "source_url"]:
                if key in row:
                    setattr(task, key, row[key])
            for key in ["nominal_day_hours", "estimate_provenance", "owner_profile_id", "ownership_provenance", "blocked_reason", "canceled_reason", "execution_mode"]:
                if key in row:
                    setattr(task, key, row[key])
            from app.services.task_domain_service import require_owner
            await require_owner(self.db, task.owner_profile_id, task.project_id)
            from app.services.task_brief_service import TaskBriefService
            await self.db.flush()
            await TaskBriefService(self.db).restore_brief(task, row)
            task.progress = None
            task.canceled_at = datetime.fromisoformat(row["canceled_at"]) if row.get("canceled_at") else None
            task.is_summary = bool(row.get("is_summary", row.get("children")))
            task.tags = json.dumps(row.get("tags", []))
            task.parent_id = None
            task.assignee_id = row.get("assignee_id")
            if task.assignee_id is not None and task.assignee_id not in members:
                raise ValueError("Snapshot task refers to unknown capacity")
            for key in ["start_date", "end_date", "actual_start_date", "actual_end_date", "min_start_date", "max_end_date", "baseline_start_date", "baseline_end_date"]:
                setattr(task, key, date.fromisoformat(row[key]) if row.get(key) else None)
            for key in ["started_at", "resolved_at"]:
                setattr(task, key, datetime.fromisoformat(row[key]) if row.get(key) else None)
            task.executed_by_principal_id = row.get("executed_by_principal_id")
            task.accepted_at = task.accepted_by_principal_id = task.accepted_version = None
            task.baseline_provenance = "restored"
            from sqlalchemy import func
            latest = await self.db.scalar(select(func.max(TaskScheduleBaseline.revision)).where(TaskScheduleBaseline.task_id == task.id))
            task.baseline_revision = max(latest or 0, task.baseline_revision or 0) + 1
            self.db.add(TaskScheduleBaseline(task_id=task.id, revision=task.baseline_revision,
                start_date=task.baseline_start_date, end_date=task.baseline_end_date,
                timezone=iteration.calendar.timezone if iteration.__dict__.get("calendar") else "UTC",
                reason=f"Explicit snapshot restore from {filename}",
                principal_id=getattr(self.db.info.get("authority"), "principal_id", None)))
        await self.db.flush()
        for row, parent_id in flat:
            task = await self.db.get(Task, row["id"])
            task.parent_id = parent_id
            for dependency in row.get("dependencies", []):
                self.db.add(TaskDependency(task_id=task.id, depends_on_id=dependency))
        await self.db.flush()
        event = await service.record_task_event(None, "snapshot_restored", {"iteration_id": iteration_id,
            "source_snapshot": filename, "pre_restore_snapshot": recovery, "restored_count": len(flat) + len(members)}, actor_type="admin")
        await self.db.flush()
        return {"message": "Application snapshot restored", "success": True, "source_snapshot": filename,
                "pre_restore_snapshot": recovery, "restored_count": len(flat) + len(members), "audit_event_id": event.id}

    def _task_to_export(self, task) -> dict:
        """Convert task to export format recursively."""
        tags = []
        if task.tags:
            try:
                tags = json.loads(task.tags) if isinstance(task.tags, str) else task.tags
            except (json.JSONDecodeError, TypeError):
                tags = []

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "is_summary": task.is_summary,
            "effort_days": task.effort_days,
            "effort_hours": task.effort_hours,
            "nominal_day_hours": task.nominal_day_hours,
            "estimate_provenance": task.estimate_provenance,
            "owner_profile_id": task.owner_profile_id,
            "ownership_provenance": task.ownership_provenance,
            "brief": task.brief,
            "brief_provenance": task.brief_provenance,
            "legacy_description": task.legacy_description,
            "brief_migration_notes": task.brief_migration_notes,
            "blocked_reason": task.blocked_reason,
            "canceled_reason": task.canceled_reason,
            "canceled_at": task.canceled_at.isoformat() if task.canceled_at else None,
            "execution_mode": task.execution_mode,
            "status": task.status,
            "external_key": task.external_key,
            "source": task.source,
            "source_url": task.source_url,
            "project_id": task.project_id,
            "milestone_id": task.milestone_id,
            "assignee_name": task.assignee.name if task.assignee else None,
            "assignee_id": task.assignee_id,
            "version": task.version,
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "resolved_at": task.resolved_at.isoformat() if task.resolved_at else None,
            "accepted_at": task.accepted_at.isoformat() if task.accepted_at else None,
            "accepted_version": task.accepted_version,
            "accepted_by_principal_id": task.accepted_by_principal_id,
            "executed_by_principal_id": task.executed_by_principal_id,
            "baseline_start_date": task.baseline_start_date.isoformat() if task.baseline_start_date else None,
            "baseline_end_date": task.baseline_end_date.isoformat() if task.baseline_end_date else None,
            "start_date": task.start_date.isoformat() if task.start_date else None,
            "end_date": task.end_date.isoformat() if task.end_date else None,
            "actual_start_date": task.actual_start_date.isoformat() if task.actual_start_date else None,
            "actual_end_date": task.actual_end_date.isoformat() if task.actual_end_date else None,
            "min_start_date": task.min_start_date.isoformat() if task.min_start_date else None,
            "max_end_date": task.max_end_date.isoformat() if task.max_end_date else None,
            "is_optional": task.is_optional,
            "is_deferred": task.is_deferred,
            "tags": tags,
            "sort_order": task.sort_order,
            "dependencies": [dep.depends_on_id for dep in task.dependencies],
            "dependency_external_keys": [
                dep.depends_on.external_key
                for dep in task.dependencies
                if getattr(dep, "depends_on", None) and dep.depends_on.external_key
            ],
            "children": [self._task_to_export(c) for c in task.children],
        }

    def _member_to_export(self, member) -> dict:
        """Convert team member to export format."""
        return {
            "id": member.id,
            "profile_id": member.profile_id,
            "name": member.name,
            "position": member.position,
            "availability_percent": member.availability_percent,
            "professionalism_coefficient": member.professionalism_coefficient,
            "operational_utilization": member.operational_utilization,
            "vacations": [
                {
                    "start_date": v.start_date.isoformat(),
                    "end_date": v.end_date.isoformat(),
                }
                for v in member.vacations
            ]
        }
