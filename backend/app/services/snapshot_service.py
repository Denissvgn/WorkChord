"""Snapshot service for iteration state backups."""
import json
import re
from datetime import timedelta
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

    async def create_snapshot(self, iteration_id: int, reason: str = "auto") -> str | None:
        """Create a snapshot of the iteration's current state.

        Args:
            iteration_id: ID of the iteration to snapshot
            reason: Reason for creating snapshot (for filename)

        Returns:
            Filename of created snapshot, or None if failed
        """
        reason = self._validate_reason(reason)
        iteration_service = IterationService(self.db)
        iteration = await iteration_service.get_by_id(iteration_id)

        if not iteration:
            return None

        from app.services.task_service import TaskService
        task_service = TaskService(self.db)
        tasks = await task_service.get_by_iteration(iteration_id)

        team_service = TeamService(self.db)
        team_members = await team_service.get_by_iteration(iteration_id)

        created_at = utc_now()

        # Build export data (compatible with import format)
        export_data = {
            "iteration": {
                "name": iteration.name,
                "start_date": iteration.start_date.isoformat(),
                "end_date": iteration.end_date.isoformat(),
                "calendar_id": iteration.calendar_id,
                "project_id": iteration.project_id,
            },
            "team_members": [
                self._member_to_export(m) for m in team_members
            ],
            "tasks": [
                self._task_to_export(t) for t in tasks
            ],
            "snapshot_info": {
                "created_at": created_at.isoformat(),
                "reason": reason,
            }
        }

        # Ensure directory exists
        snapshot_dir = self._get_snapshot_dir(iteration_id)
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        # Reserve a UTC-derived filename atomically. A process creating another
        # snapshot in the same microsecond advances the filename timestamp
        # instead of overwriting the existing recovery point.
        for collision_offset in range(1_000_000):
            filename_created_at = created_at + timedelta(microseconds=collision_offset)
            timestamp = filename_created_at.strftime("%Y%m%d_%H%M%S_%f")
            filename = f"snapshot_{timestamp}_{reason}.json"
            filepath = self._snapshot_path(iteration_id, filename)
            try:
                with filepath.open("x", encoding="utf-8") as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                break
            except FileExistsError:
                continue
        else:
            raise RuntimeError("Could not reserve a unique snapshot filename.")

        # Rotate old snapshots
        await self.rotate_snapshots(iteration_id)

        return filename

    async def rotate_snapshots(self, iteration_id: int, max_count: int = 10) -> int:
        """Remove oldest snapshots if count exceeds max.

        Returns:
            Number of snapshots deleted
        """
        # Get all snapshot files sorted by modification time (oldest first)
        snapshots = sorted(
            self._snapshot_files(iteration_id),
            key=lambda p: p.stat().st_mtime
        )

        # Delete oldest if exceeding max_count
        deleted = 0
        while len(snapshots) > max_count:
            oldest = snapshots.pop(0)
            oldest.unlink()
            deleted += 1

        return deleted

    def list_snapshots(self, iteration_id: int) -> list[dict]:
        """List all snapshots for an iteration.

        Returns:
            List of snapshot info dicts with filename, created_at, reason
        """
        snapshots = []
        for filepath in sorted(self._snapshot_files(iteration_id), reverse=True):
            try:
                with filepath.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    info = data.get("snapshot_info", {})
                    snapshots.append({
                        "filename": filepath.name,
                        "created_at": info.get("created_at"),
                        "reason": info.get("reason", "unknown"),
                        "size_bytes": filepath.stat().st_size,
                    })
            except (json.JSONDecodeError, IOError):
                snapshots.append({
                    "filename": filepath.name,
                    "created_at": None,
                    "reason": "corrupt",
                    "size_bytes": filepath.stat().st_size,
                })

        return snapshots

    def get_snapshot(self, iteration_id: int, filename: str) -> dict | None:
        """Get snapshot data by filename.

        Returns:
            Snapshot data dict or None if not found
        """
        filepath = self._snapshot_path(iteration_id, filename)
        if not filepath.exists():
            return None

        try:
            with filepath.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else None
        except (json.JSONDecodeError, IOError):
            return None

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
            "effort_days": task.effort_days,
            "effort_hours": task.effort_hours,
            "status": task.status,
            "external_key": task.external_key,
            "source": task.source,
            "source_url": task.source_url,
            "project_id": task.project_id,
            "milestone_id": task.milestone_id,
            "assignee_name": task.assignee.name if task.assignee else None,
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
