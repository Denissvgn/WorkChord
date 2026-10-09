"""Operator-scoped, bounded hierarchy diagnosis and version-checked deterministic repair."""

from sqlalchemy import select

from app.authority import require_operator
from app.commands import atomic_command, lock_iterations
from app.models.task import Task
from app.services.task_service import TaskService
from app.services.task_status_service import TaskStatusService
from app.services.snapshot_service import SnapshotService
from app.services.work_metrics import effective_work_flags, scoped_metric_tasks, task_signals


class HierarchyRepairService:
    def __init__(self, db):
        self.db = db

    async def audit(self, iteration_id, *, after_id=0, limit=100):
        require_operator(self.db)
        if not 1 <= limit <= 500:
            raise ValueError("Repair limit must be between 1 and 500")
        tasks = await scoped_metric_tasks(self.db, iteration_id=iteration_id)
        by_id = {task.id: task for task in tasks}
        children = {}
        for task in tasks:
            children.setdefault(task.parent_id, []).append(task)
        rows = []
        for task in sorted(tasks, key=lambda task: task.id):
            if task.id <= after_id:
                continue
            issues, proposed = [], {}
            parent = by_id.get(task.parent_id)
            if task.parent_id is not None and (parent is None or parent.project_id != task.project_id):
                issues.append("Parent scope is missing or inconsistent; operator reconciliation required")
            seen, ancestor = {task.id}, task.parent_id
            while ancestor in by_id:
                if ancestor in seen:
                    issues.append("Hierarchy cycle requires explicit reconciliation")
                    break
                seen.add(ancestor)
                ancestor = by_id[ancestor].parent_id
            descendants = children.get(task.id, [])
            if descendants or task.is_summary:
                target = TaskStatusService.derive_parent_status([child.status for child in descendants]) if descendants else "planned"
                priority = min(child.priority for child in descendants) if descendants else task.priority
                if task.status != target:
                    if target == "closed" and any(not task_signals(child, effective_flags=effective_work_flags(child, by_id=by_id))["is_accepted"] for child in descendants):
                        issues.append("Closed roll-up has unknown acceptance provenance; do not promote automatically")
                    else:
                        proposed["status"] = target
                for field, value in {"priority": priority, "is_summary": True, "effort_days": 0.0, "effort_hours": 0.0, "assignee_id": None}.items():
                    if getattr(task, field) != value:
                        proposed[field] = value
            if issues and any("scope" in issue or "cycle" in issue for issue in issues):
                proposed = {}
            if proposed or issues:
                rows.append({"task_id": task.id, "version": task.version, "current": {key: getattr(task, key) for key in proposed},
                             "proposed": proposed, "unresolved": issues})
                if len(rows) == limit:
                    break
        return {"iteration_id": iteration_id, "rows": rows, "next_after_id": rows[-1]["task_id"] if len(rows) == limit else None,
                "read_only": True}

    @atomic_command
    async def repair(self, iteration_id, *, expected_versions, reason, after_id=0, limit=100, expected_revision=None):
        require_operator(self.db)
        if len(reason.strip()) < 8:
            raise ValueError("A clear operator repair reason is required")
        initial = await self.audit(iteration_id, after_id=after_id, limit=limit)
        if not any(row["proposed"] for row in initial["rows"]):
            if expected_revision is not None:
                from app.models.iteration import Iteration
                from app.commands import AggregateVersionConflict
                current = await self.db.scalar(select(Iteration.revision).where(Iteration.id == iteration_id))
                if current != expected_revision:
                    raise AggregateVersionConflict(iteration_id, expected_revision, current or 0)
            return {**initial, "read_only": False, "repaired_ids": []}
        await lock_iterations(self.db, [iteration_id], expected={iteration_id: expected_revision} if expected_revision is not None else None)
        report = await self.audit(iteration_id, after_id=after_id, limit=limit)
        candidates = [row for row in report["rows"] if row["proposed"]]
        service = TaskService(self.db)
        if candidates:
            await service._require_unclaimed_structure([row["task_id"] for row in candidates])
            for row in candidates:
                if expected_versions.get(row["task_id"]) != row["version"]:
                    from app.services.task_service import TaskVersionConflictError
                    raise TaskVersionConflictError(expected_versions.get(row["task_id"], 0), {"id": row["task_id"], "version": row["version"]})
            await SnapshotService(self.db).create_snapshot(iteration_id, "before_hierarchy_repair")
        for row in candidates:
            task = await self.db.get(Task, row["task_id"])
            await service.reserve_task_version(task, row["version"])
            self.db.info.setdefault("derived_rollups", set()).add(task.id)
            for key, value in row["proposed"].items():
                setattr(task, key, value)
            task.accepted_at = task.accepted_by_principal_id = task.accepted_version = None
            await service.record_task_event(task.id, "hierarchy_repaired", {"before": row["current"], "after": row["proposed"], "reason": reason}, actor_type="admin")
        await self.db.flush()
        return {**report, "read_only": False, "repaired_ids": [row["task_id"] for row in candidates]}
