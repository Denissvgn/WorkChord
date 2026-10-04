"""Task service with business logic."""

from app.commands import atomic_command, command_transaction, commit_or_flush, lock_iterations, current_command, lock_planning
from app.authority import require_project, internal_authority
import json
from datetime import date
from typing import Any, Optional, Sequence

from sqlalchemy import and_, or_, select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import attributes, selectinload

from app.models.agent import TaskEvent
from app.models.iteration import Iteration
from app.models.project import Project, ProjectMilestone
from app.models.request_source import RequestSourceLink
from app.models.task import Task, TaskDependency, TaskStatus
from app.models.team_member import TeamMember
from app.models.triage import TriageItem
from app.query_limits import (
    CollectionLimitExceededError,
    MAX_ITERATION_TREE_TASKS,
)
from app.schemas.task import (
    TaskAssignee,
    TaskClaimedBy,
    TaskCreate,
    TaskImportDestination,
    TaskMilestone,
    TaskProject,
    TaskResponse,
    TaskUpdate,
)
from app.services.agent_readiness import evaluate_agent_readiness
from app.services.external_link_service import ExternalLinkService
from app.services.language_service import (
    automatic_child_status_reason,
    incomplete_dependency_message,
    resolve_runtime_ui_language,
    task_requires_schedule_message,
)
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.snapshot_service import SnapshotService


class TaskTreeIntegrityError(ValueError):
    """Raised when persisted task parent links cannot form a valid iteration tree."""


class TaskVersionConflictError(RuntimeError):
    """Raised when an optimistic task write no longer matches the stored version."""

    def __init__(self, expected_version: int, current_task: dict[str, Any]):
        self.expected_version = expected_version
        self.current_task = current_task
        super().__init__(
            f"Task version conflict: expected {expected_version}, "
            f"current {current_task['version']}."
        )

    def detail(self) -> dict[str, Any]:
        """Return the stable API conflict envelope."""
        return {
            "code": "task_version_conflict",
            "message": str(self),
            "expected_version": self.expected_version,
            "current_task": self.current_task,
        }


class TaskService:
    """Service for task operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent_capability_slugs: Optional[set[str]] = None
        self._status_service = None
        self._import_service = None

    def _json_dumps(self, data: Any) -> str:
        """Serialize event payloads consistently."""
        return json.dumps(data, ensure_ascii=False, default=str)

    async def _project_exists(self, project_id: int) -> bool:
        """Return whether a project exists."""
        result = await self.db.execute(
            select(Project.id).where(Project.id == project_id)
        )
        return result.scalar_one_or_none() is not None

    async def _require_project_exists(self, project_id: Optional[int]) -> None:
        """Validate optional project reference."""
        if project_id is not None and not await self._project_exists(project_id):
            raise ValueError(f"Project with id {project_id} not found")

    async def require_iteration_exists(self, iteration_id: int) -> None:
        """Validate that a task write target is a real iteration."""
        if iteration_id is not None:
            await self._iteration_project_id(iteration_id)

    async def _iteration_project_id(self, iteration_id: int) -> Optional[int]:
        """Return an iteration's project scope, raising when the iteration is missing."""
        result = await self.db.execute(
            select(Iteration.project_id).where(Iteration.id == iteration_id)
        )
        row = result.first()
        if row is None:
            raise ValueError(f"Iteration with id {iteration_id} not found")
        return row[0]

    async def _resolve_project_for_iteration_create(
        self,
        iteration_id: int,
        requested_project_id: Optional[int],
    ) -> Optional[int]:
        """Apply iteration project scope to a new executable task."""
        if iteration_id is None:
            if requested_project_id is None:
                raise ValueError("Project backlog tasks require project_id")
            await self._require_project_exists(requested_project_id)
            return requested_project_id
        scoped_project_id = await self._iteration_project_id(iteration_id)
        if scoped_project_id is not None:
            if requested_project_id is not None and requested_project_id != scoped_project_id:
                raise ValueError("Task project must match the scoped iteration project.")
            return scoped_project_id

        await self._require_project_exists(requested_project_id)
        return requested_project_id

    async def require_task_project_scope_for_update(
        self,
        task: Task,
        requested_project_id: Optional[int],
        project_id_was_set: bool,
    ) -> Optional[int]:
        """Validate and return the effective project for a task update."""
        if task.iteration_id is None:
            effective = requested_project_id if project_id_was_set else task.project_id
            if effective is None:
                raise ValueError("Project backlog tasks require project_id")
            await self._require_project_exists(effective)
            return effective
        scoped_project_id = await self._iteration_project_id(task.iteration_id)
        if scoped_project_id is not None:
            if project_id_was_set:
                if requested_project_id != scoped_project_id:
                    raise ValueError("Task project must match the scoped iteration project.")
                return scoped_project_id
            if task.project_id != scoped_project_id:
                raise ValueError("Existing task project must match the scoped iteration project.")
            return task.project_id

        if project_id_was_set:
            await self._require_project_exists(requested_project_id)
            return requested_project_id
        return task.project_id

    async def _require_same_iteration_dependencies(
        self,
        iteration_id: int,
        dependency_ids: Sequence[int],
        project_id: int | None = None,
    ) -> None:
        """Validate that task dependencies stay inside one iteration schedule graph."""
        dependency_id_set = set(dependency_ids)
        if not dependency_id_set:
            return

        result = await self.db.execute(
            select(Task.id, Task.iteration_id, Task.project_id).where(Task.id.in_(dependency_id_set))
        )
        dependency_iterations = {
            task_id: (dependency_iteration_id, dependency_project_id)
            for task_id, dependency_iteration_id, dependency_project_id in result.all()
        }

        for dependency_id in dependency_id_set:
            dependency_scope = dependency_iterations.get(dependency_id)
            if dependency_scope is None:
                raise ValueError(f"Dependency task with id {dependency_id} not found")
            if dependency_scope[0] != iteration_id or iteration_id is None and dependency_scope[1] != project_id:
                raise ValueError("Task dependencies must belong to the same iteration.")

    async def _require_acyclic_dependencies(
        self,
        task_id: int,
        iteration_id: int,
        dependency_ids: Sequence[int],
    ) -> None:
        """Serialize one iteration graph and reject dependency cycles."""
        await self.db.execute(
            select(Iteration.id)
            .where(Iteration.id == iteration_id)
            .with_for_update()
        )
        dependency_id_set = set(dependency_ids)
        if task_id in dependency_id_set:
            raise ValueError("Task cannot depend on itself.")
        result = await self.db.execute(
            select(TaskDependency.task_id, TaskDependency.depends_on_id)
            .join(Task, Task.id == TaskDependency.task_id)
            .where(Task.iteration_id == iteration_id)
        )
        adjacency: dict[int, set[int]] = {}
        for source_id, target_id in result.all():
            adjacency.setdefault(source_id, set()).add(target_id)
        adjacency[task_id] = dependency_id_set

        visiting: set[int] = set()
        visited: set[int] = set()

        def visit(node_id: int) -> None:
            if node_id in visiting:
                raise ValueError("Task dependency graph cannot contain a cycle.")
            if node_id in visited:
                return
            visiting.add(node_id)
            for dependency_id in adjacency.get(node_id, set()):
                visit(dependency_id)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in set(adjacency).union(dependency_id_set):
            visit(node_id)

    async def _lock_dependency_task(self, task_id: int) -> Optional[Task]:
        """Lock one dependency graph in Iteration -> Task order."""
        await self._lock_task_scope(task_id)

        hint_result = await self.db.execute(
            select(Task.iteration_id).where(Task.id == task_id)
        )
        hint = hint_result.first()
        if hint is None:
            return None
        iteration_id = hint[0]
        await self.db.execute(
            select(Iteration.id)
            .where(Iteration.id == iteration_id)
            .with_for_update()
        )
        task_result = await self.db.execute(
            select(Task)
            .where(Task.id == task_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        task = task_result.scalar_one_or_none()
        if task is None:
            return None
        if task.iteration_id != iteration_id:
            raise ValueError("Task iteration changed while acquiring dependency lock")
        # Reuse the complete tree loader only after the aggregate and row locks
        # are held, so relationship reads cannot race another graph mutation.
        return await self.get_by_id(task_id)

    async def _milestone_project_id(self, milestone_id: int) -> Optional[int]:
        """Return the project owning a milestone, or None when missing."""
        result = await self.db.execute(
            select(ProjectMilestone.project_id).where(ProjectMilestone.id == milestone_id)
        )
        return result.scalar_one_or_none()

    async def _require_milestone_compatible(
        self,
        milestone_id: Optional[int],
        project_id: Optional[int],
    ) -> None:
        """Validate that a milestone belongs to the task's effective project."""
        if milestone_id is None:
            return
        if project_id is None:
            raise ValueError("Task milestone requires a project.")

        milestone_project_id = await self._milestone_project_id(milestone_id)
        if milestone_project_id is None:
            raise ValueError(f"Milestone with id {milestone_id} not found")
        if milestone_project_id != project_id:
            raise ValueError("Task milestone must belong to the task project.")

    async def require_iteration_assignee(
        self,
        assignee_id: Optional[int],
        iteration_id: int,
    ) -> None:
        """Validate that an executable task assignee belongs to the task iteration."""
        if assignee_id is None:
            return
        if iteration_id is None:
            raise ValueError("Backlog ownership uses owner_profile_id; capacity assignment requires an iteration")

        result = await self.db.execute(
            select(TeamMember).where(TeamMember.id == assignee_id)
        )
        member = result.scalar_one_or_none()
        if member is None:
            raise ValueError(f"Team member with id {assignee_id} not found")
        if member.iteration_id != iteration_id:
            raise ValueError(
                f"Team member with id {assignee_id} is not assigned to iteration {iteration_id}"
            )

    async def _milestone_matches_project(
        self,
        milestone_id: Optional[int],
        project_id: Optional[int],
    ) -> bool:
        """Return whether an existing milestone assignment remains compatible."""
        if milestone_id is None:
            return True
        if project_id is None:
            return False
        return await self._milestone_project_id(milestone_id) == project_id

    async def _cascade_project_to_children(
        self,
        parent_id: int,
        project_id: Optional[int],
        actor_type: str = "user",
        actor_id: Optional[int] = None,
    ) -> list[int]:
        """Cascade a project assignment to all descendants."""
        result = await self.db.execute(
            select(Task).where(Task.parent_id == parent_id)
        )
        children = result.scalars().all()
        changed_ids: list[int] = []

        for child in children:
            child_changes: dict[str, dict[str, Any]] = {}
            if child.project_id != project_id:
                from app.services.task_domain_service import require_owner
                await require_owner(self.db, child.owner_profile_id, project_id)
                old_project_id = child.project_id
                child.project_id = project_id
                child_changes["project_id"] = {
                    "old": old_project_id,
                    "new": project_id,
                }

            if child.milestone_id is not None and not await self._milestone_matches_project(
                child.milestone_id,
                project_id,
            ):
                old_milestone_id = child.milestone_id
                child.milestone_id = None
                child_changes["milestone_id"] = {
                    "old": old_milestone_id,
                    "new": None,
                }

            if child_changes:
                from app.services.task_brief_service import clear_execution_evidence
                clear_execution_evidence(child)
                await self.reserve_task_version(child, child.version)
                changed_ids.append(child.id)
                await self.record_task_event(
                    child.id,
                    "task_updated",
                    {
                        "changes": child_changes,
                        "version": child.version,
                        "cascaded_from_parent_id": parent_id,
                    },
                    actor_type=actor_type,
                    actor_id=actor_id,
                )

            changed_ids.extend(
                await self._cascade_project_to_children(
                    child.id,
                    project_id,
                    actor_type=actor_type,
                    actor_id=actor_id,
                )
            )

        return changed_ids

    async def record_task_event(
        self,
        task_id: Optional[int],
        event_type: str,
        payload: Optional[dict] = None,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> TaskEvent:
        """Append an audit event for a task mutation or checkpoint."""
        authority = self.db.info.get("authority")
        if authority is not None:
            payload = {**(payload or {}), "principal_id": authority.principal_id, "source": authority.source}
            correlation_id = authority.correlation_id
            actor_id = authority.actor_id
            if actor_type != "auto":
                actor_type = "agent" if authority.kind == "agent" else "admin" if authority.kind == "system" else "user"
        event = TaskEvent(
            task_id=task_id,
            actor_type=actor_type,
            actor_id=actor_id,
            event_type=event_type,
            payload=self._json_dumps(payload or {}),
            trace_id=trace_id,
            span_id=span_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )
        self.db.add(event)
        return event

    def _metadata_from_task(self, task: Task) -> dict[str, Any]:
        """Return the client-safe current-task fields used by conflict responses."""
        return {
            "id": task.id,
            "version": task.version,
            "title": task.title,
            "status": task.status,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        }

    async def _current_task_metadata(self, task_id: int) -> dict[str, Any] | None:
        """Load conflict metadata without loading the complete task tree."""
        result = await self.db.execute(
            select(Task.id, Task.version, Task.title, Task.status, Task.updated_at).where(
                Task.id == task_id
            )
        )
        row = result.one_or_none()
        if row is None:
            return None
        return {
            "id": row.id,
            "version": row.version,
            "title": row.title,
            "status": row.status,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }

    def ensure_expected_version(self, task: Task, expected_version: int | None) -> None:
        """Fail early for an already-stale caller before filesystem side effects."""
        from app.mutation_versions import require_mutation_revision
        require_mutation_revision(self.db, expected_version, field="expected_version", resource="task", resource_id=task.id)
        command = current_command(self.db)
        version = command.tasks.get(task.id, task.version) if command is not None else task.version
        if expected_version is not None and version != expected_version:
            raise TaskVersionConflictError(expected_version, self._metadata_from_task(task))

    async def reserve_task_version(
        self,
        task: Task,
        expected_version: int | None,
    ) -> int:
        """Atomically reserve the next task version at the database write boundary."""
        # Rollback expires ORM state even with expire_on_commit=False. Capture
        # conflict identifiers before the write so a losing async transaction
        # never triggers an implicit synchronous refresh (MissingGreenlet).
        task_id = task.id
        loaded_version = task.version
        command = current_command(self.db)
        if command is not None:
            await lock_iterations(self.db, [task.iteration_id] if task.iteration_id is not None else [])
            if task_id in command.tasks:
                if expected_version is not None and expected_version not in {command.tasks[task_id], task.version}:
                    raise TaskVersionConflictError(expected_version, self._metadata_from_task(task))
                return task.version
        if expected_version is None:
            from app.runtime_telemetry import metrics
            metrics.increment("workchord_legacy_task_commands_total")
        statement = sql_update(Task).where(Task.id == task_id)
        if expected_version is not None:
            statement = statement.where(Task.version == expected_version)
        statement = (
            statement.values(version=Task.version + 1)
            .returning(Task.version, Task.updated_at)
            .execution_options(synchronize_session=False)
        )
        with self.db.no_autoflush:
            result = await self.db.execute(statement)
        row = result.one_or_none()
        if row is None:
            await self.db.rollback()
            current = await self._current_task_metadata(task_id)
            if current is None:
                raise ValueError(f"Task with id {task_id} not found")
            if expected_version is None:
                expected_version = loaded_version
            raise TaskVersionConflictError(expected_version, current)

        if command is not None:
            command.tasks[task_id] = row.version - 1
        attributes.set_committed_value(task, "version", row.version)
        if row.updated_at is not None:
            attributes.set_committed_value(task, "updated_at", row.updated_at)
        return row.version

    async def get_by_iteration(
        self,
        iteration_id: int,
        include_children: bool = True,
        *,
        max_tasks: int = MAX_ITERATION_TREE_TASKS,
    ) -> Sequence[Task]:
        """Get one explicitly bounded iteration tree from a flat task query."""
        if not include_children:
            result = await self.db.execute(
                self._task_graph_query(iteration_id)
                .where(Task.parent_id.is_(None))
                .limit(max_tasks + 1)
            )
            roots = list(result.scalars().all())
            if len(roots) > max_tasks:
                raise CollectionLimitExceededError(
                    "iteration task roots",
                    max_tasks,
                )
            return roots
        roots, _ = await self._load_iteration_tree(
            iteration_id,
            max_tasks=max_tasks,
        )
        return roots

    async def load_owner_names(self, tasks):
        """Expose only the public owner name through already authorized task scope."""
        from app.authority import internal_authority
        from app.models.team_member import TeamMemberProfile
        for task in tasks:
            task.__dict__["_owner_name"] = None
        ids = {task.owner_profile_id for task in tasks if task.owner_profile_id is not None}
        if not ids:
            return
        for task in tasks:
            require_project(self.db, task.project_id, "read")
        with internal_authority(self.db):
            names = dict((await self.db.execute(select(TeamMemberProfile.id, TeamMemberProfile.display_name).where(TeamMemberProfile.id.in_(ids)))).all())
        for task in tasks:
            task.__dict__["_owner_name"] = names.get(task.owner_profile_id)

    def _task_graph_query(self, iteration_id: int | None, project_id: int | None = None):
        """Build the bounded relationship query used before in-memory tree assembly."""
        return (
            select(Task)
            .where(Task.iteration_id == iteration_id, *([Task.project_id == project_id] if iteration_id is None else []))
            .execution_options(populate_existing=True)
            .options(
                selectinload(Task.owner_profile),
                selectinload(Task.project),
                selectinload(Task.milestone),
                selectinload(Task.assignee).selectinload(TeamMember.vacations),
                selectinload(Task.claimed_agent),
                selectinload(Task.external_links),
                selectinload(Task.request_source_links).selectinload(
                    RequestSourceLink.request_source
                ),
            )
            .order_by(Task.sort_order, Task.id)
        )

    async def _load_iteration_tree(
        self,
        iteration_id: int,
        *,
        max_tasks: int = MAX_ITERATION_TREE_TASKS,
        project_id: int | None = None,
    ) -> tuple[list[Task], dict[int, Task]]:
        """Load and defensively assemble a contract-bounded iteration."""
        result = await self.db.execute(
            self._task_graph_query(iteration_id, project_id).limit(max_tasks + 1)
        )
        tasks = list(result.scalars().all())
        if len(tasks) > max_tasks:
            raise CollectionLimitExceededError("iteration task tree", max_tasks)
        await self.load_owner_names(tasks)
        tasks_by_id = {task.id: task for task in tasks}

        # Relationship access from synchronous scheduling/snapshot serializers
        # must never initiate async I/O.  Rebuild this collection explicitly
        # from one bounded query so concurrent flushes cannot leave a task with
        # an expired or partially populated dependency relationship.
        dependencies_by_task: dict[int, list[TaskDependency]] = {
            task.id: [] for task in tasks
        }
        if tasks_by_id:
            dependency_result = await self.db.execute(
                select(TaskDependency)
                .where(TaskDependency.task_id.in_(tasks_by_id))
                .options(selectinload(TaskDependency.depends_on))
                .order_by(TaskDependency.task_id, TaskDependency.id)
            )
            for dependency in dependency_result.scalars():
                dependencies_by_task[dependency.task_id].append(dependency)
        for task in tasks:
            attributes.set_committed_value(
                task,
                "dependencies",
                dependencies_by_task[task.id],
            )

        visit_state: dict[int, int] = {}

        def visit(task: Task) -> None:
            state = visit_state.get(task.id, 0)
            if state == 1:
                raise TaskTreeIntegrityError(
                    f"Task tree cycle detected in iteration {iteration_id} at task {task.id}."
                )
            if state == 2:
                return
            visit_state[task.id] = 1
            if task.parent_id is not None:
                parent = tasks_by_id.get(task.parent_id)
                if parent is None:
                    raise TaskTreeIntegrityError(
                        f"Task {task.id} references missing or cross-iteration parent {task.parent_id}."
                    )
                visit(parent)
            visit_state[task.id] = 2

        for task in tasks:
            visit(task)

        roots: list[Task] = []
        children_by_parent: dict[int, list[Task]] = {task.id: [] for task in tasks}
        for task in tasks:
            if task.parent_id is None:
                roots.append(task)
                attributes.set_committed_value(task, "parent", None)
                continue
            parent = tasks_by_id[task.parent_id]
            children_by_parent[parent.id].append(task)
            attributes.set_committed_value(task, "parent", parent)

        for task in tasks:
            children = sorted(
                children_by_parent[task.id],
                key=lambda child: (child.sort_order, child.id),
            )
            attributes.set_committed_value(task, "children", children)
        roots.sort(key=lambda root: (root.sort_order, root.id))
        return roots, tasks_by_id

    async def get_all_tasks(self, iteration_id: int) -> Sequence[Task]:
        """Get all tasks (flat list) for an iteration."""
        _, tasks_by_id = await self._load_iteration_tree(iteration_id)
        return sorted(tasks_by_id.values(), key=lambda task: (task.priority, task.id))

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get one task with its complete iteration tree relationships assembled."""
        row = (await self.db.execute(select(Task.iteration_id, Task.project_id).where(Task.id == task_id))).first()
        if row is None:
            return None
        _, tasks_by_id = await self._load_iteration_tree(row.iteration_id, project_id=row.project_id)
        return tasks_by_id.get(task_id)

    @atomic_command
    async def create(
        self,
        iteration_id: int,
        data: TaskCreate,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        create_snapshot: bool = True,
        commit: bool = True,
    ) -> Task:
        """Create a new task."""
        if iteration_id is not None:
            await lock_iterations(self.db, [iteration_id], expected={iteration_id: data.expected_revision} if data.expected_revision is not None else None, require_expected=True, revision_field="expected_revision")
        await self.require_iteration_exists(iteration_id)
        if iteration_id is None and data.project_id is not None:
            from app.commands import lock_backlog_project
            await lock_backlog_project(self.db, data.project_id)
            if create_snapshot:
                from app.services.backlog_snapshot_service import BacklogSnapshotService
                await BacklogSnapshotService(self.db).capture(data.project_id, "before_create")
        await self._require_same_iteration_dependencies(iteration_id, data.depends_on, data.project_id)

        project_id = data.project_id
        milestone_id = data.milestone_id

        if data.parent_id is not None:
            parent = await self.get_by_id(data.parent_id)
            if not parent:
                raise ValueError(f"Parent task with id {data.parent_id} not found")
            if parent.iteration_id != iteration_id:
                raise ValueError("Parent task must belong to the same iteration.")
            await self._require_unclaimed_structure([parent.id])
            if not parent.children and not parent.is_summary:
                if parent.status != "planned":
                    raise ValueError("Executed leaf work cannot be silently converted into a summary")
                inherited = {key: getattr(parent, key) for key in ["priority", "assignee_id", "owner_profile_id", "effort_days", "effort_hours"] if key not in data.model_fields_set}
                data = data.model_copy(update=inherited)

            if project_id is None:
                project_id = parent.project_id
            elif project_id != parent.project_id:
                raise ValueError("Subtask project must match parent task project.")
            if "milestone_id" not in data.model_fields_set:
                milestone_id = parent.milestone_id

        project_id = await self._resolve_project_for_iteration_create(
            iteration_id,
            project_id,
        )
        require_project(self.db, project_id, "create")
        await self._require_milestone_compatible(milestone_id, project_id)
        await self.require_iteration_assignee(data.assignee_id, iteration_id)

        from app.services.task_domain_service import normalize_effort, require_owner, nominal_day_hours
        day_hours = await nominal_day_hours(self.db, iteration_id)
        estimate = normalize_effort(data.model_dump(exclude_unset=True), day_hours)
        await require_owner(self.db, data.owner_profile_id, project_id)
        if create_snapshot:
            # Create snapshot after validation so rejected writes do not leave snapshots.
            snapshot_service = SnapshotService(self.db)
            await snapshot_service.create_snapshot(iteration_id, "before_create")

        task = Task(
            iteration_id=iteration_id,
            project_id=project_id,
            milestone_id=milestone_id,
            parent_id=data.parent_id,
            title=data.title,
            description=data.description,
            priority=data.priority,
            effort_hours=estimate["effort_hours"],
            _legacy_effort_days=estimate["effort_days"],
            nominal_day_hours=day_hours,
            estimate_provenance=estimate["estimate_provenance"],
            owner_profile_id=data.owner_profile_id,
            ownership_provenance="explicit" if data.owner_profile_id else "unassigned",
            assignee_id=data.assignee_id,
            status=TaskStatus.PLANNED.value,
            is_optional=data.is_optional,
            is_deferred=data.is_deferred,
            min_start_date=data.min_start_date,
            max_end_date=data.max_end_date,
            external_key=data.external_key,
            source=data.source,
            source_url=data.source_url,
            tags=json.dumps(data.tags) if data.tags else "[]",
            sort_order=data.sort_order,
        )
        self.db.add(task)
        await self.db.flush()
        if data.brief is not None:
            from app.services.task_brief_service import TaskBriefService
            await TaskBriefService(self.db).apply_brief(task, data.brief)
        if task.parent_id is not None:
            await self.status_service.reconcile_parent_chain(task.parent_id, commit=False)

        # Add dependencies
        for dep_id in data.depends_on:
            dependency = TaskDependency(task_id=task.id, depends_on_id=dep_id)
            self.db.add(dependency)

        await self.record_task_event(
            task.id,
            "task_created",
            {
                "title": task.title,
                "iteration_id": iteration_id,
                "project_id": task.project_id,
                "milestone_id": task.milestone_id,
                "parent_id": task.parent_id,
                "depends_on": data.depends_on,
                "external_key": task.external_key,
                "source": task.source,
            },
            actor_type=actor_type,
            actor_id=actor_id,
            trace_id=trace_id,
            span_id=span_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="task.created",
                entity_type="task",
                entity_id=task.id,
                data={
                    "task_id": task.id,
                    "title": task.title,
                    "iteration_id": task.iteration_id,
                    "project_id": task.project_id,
                    "milestone_id": task.milestone_id,
                    "parent_id": task.parent_id,
                    "status": task.status,
                },
            )
            if commit:
                await commit_or_flush(self.db)
            else:
                await self.db.flush()
        except Exception:
            if commit:
                await self.db.rollback()
            raise

        if not commit:
            return task
        created = await self.get_by_id(task.id)
        if created is None:
            raise RuntimeError("Created task could not be reloaded")
        return created

    async def create_subtask(self, parent_id: int, data: TaskCreate) -> Optional[Task]:
        """Create a subtask under a parent task."""
        parent = await self.get_by_id(parent_id)
        if not parent:
            return None
        if data.project_id is not None and data.project_id != parent.project_id:
            raise ValueError("Subtask project must match parent task project.")

        data.parent_id = parent_id
        if data.project_id is None:
            data.project_id = parent.project_id
        return await self.create(parent.iteration_id, data)

    @atomic_command
    async def update(
        self,
        task_id: int,
        data: TaskUpdate,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[Task]:
        """Update an existing task."""
        await self._lock_task_scope(task_id, target_project_id=data.project_id)
        task = await self.get_by_id(task_id)
        if not task:
            return None

        previous_project_id = task.project_id
        fields = set(data.model_dump(exclude_unset=True)) - {"expected_version"}
        new_state = getattr(data.status, "value", data.status)
        action = ("review" if new_state == "closed" else "execute") if fields == {"status"} else "edit"
        require_project(self.db, task.project_id, action)
        if task.is_summary and fields.intersection({"priority", "effort_days", "effort_hours", "assignee_id", "status"}):
            raise ValueError("Summary work fields are derived from leaves; edit the relevant leaf tasks")

        self.ensure_expected_version(task, data.expected_version)

        update_data = data.model_dump(exclude_unset=True)
        expected_version = update_data.pop("expected_version", None)

        # Dependency writes participate in the same scheduling aggregate as
        # serialized preview/apply. Acquire the aggregate root before any
        # snapshot write, ORM mutation, or autoflush can lock a task row; the
        # shared global order is Iteration -> Task/dependency rows.
        depends_on_ids = update_data.pop("depends_on", None)
        if depends_on_ids is not None:
            await self.db.execute(
                select(Iteration.id)
                .where(Iteration.id == task.iteration_id)
                .with_for_update()
            )
            locked_result = await self.db.execute(
                select(Task)
                .where(Task.id == task_id)
                .with_for_update()
                .execution_options(populate_existing=True)
            )
            task = locked_result.scalar_one_or_none()
            if task is None:
                return None
            self.ensure_expected_version(task, expected_version)
            task = await self.get_by_id(task_id)

        # Create snapshot before modification
        snapshot_service = SnapshotService(self.db)
        await snapshot_service.create_snapshot(task.iteration_id, f"before_update_task_{task_id}")

        requested_status = update_data.pop("status", None)
        if requested_status is not None:
            requested_status_value = requested_status.value if hasattr(requested_status, "value") else requested_status
            if requested_status_value != task.status:
                raise ValueError("Use the task status transition endpoint to change status.")

        # Handle depends_on separately - it is a relationship, not a field.
        project_id_requested = update_data.pop("project_id", None) if "project_id" in update_data else None
        project_id_was_set = "project_id" in data.model_fields_set
        milestone_id_requested = (
            update_data.pop("milestone_id", None) if "milestone_id" in update_data else None
        )
        milestone_id_was_set = "milestone_id" in data.model_fields_set
        assignee_id_was_set = "assignee_id" in data.model_fields_set
        changed_fields: dict[str, dict[str, Any]] = {}

        effective_project_id = await self.require_task_project_scope_for_update(
            task,
            project_id_requested,
            project_id_was_set,
        )
        if project_id_was_set and task.parent_id is not None:
            parent = await self.get_by_id(task.parent_id)
            if parent and project_id_requested != parent.project_id:
                raise ValueError("Subtask project must match parent task project.")

        if milestone_id_was_set:
            await self._require_milestone_compatible(
                milestone_id_requested,
                effective_project_id,
            )

        if assignee_id_was_set:
            await self.require_iteration_assignee(
                update_data.get("assignee_id"),
                task.iteration_id,
            )

        if project_id_was_set:
            if task.project_id != project_id_requested:
                if task.iteration_id is None:
                    subtree_ids = await self._task_subtree_ids(task.id)
                    await self._require_unclaimed_structure(subtree_ids)
                    await self._require_no_cross_subtree_dependencies(subtree_ids)
                old_project_id = task.project_id
                task.project_id = project_id_requested
                changed_fields["project_id"] = {
                    "old": old_project_id,
                    "new": project_id_requested,
                }
                if task.parent_id is None:
                    cascaded_ids = await self._cascade_project_to_children(
                        task_id,
                        project_id_requested,
                        actor_type=actor_type,
                        actor_id=actor_id,
                    )
                    if cascaded_ids:
                        changed_fields["cascaded_project_task_ids"] = {
                            "old": [],
                            "new": cascaded_ids,
                        }

        if milestone_id_was_set:
            if task.milestone_id != milestone_id_requested:
                old_milestone_id = task.milestone_id
                task.milestone_id = milestone_id_requested
                changed_fields["milestone_id"] = {
                    "old": old_milestone_id,
                    "new": milestone_id_requested,
                }
        elif project_id_was_set and task.milestone_id is not None:
            if not await self._milestone_matches_project(task.milestone_id, project_id_requested):
                old_milestone_id = task.milestone_id
                task.milestone_id = None
                changed_fields["milestone_id"] = {
                    "old": old_milestone_id,
                    "new": None,
                }

        from app.services.task_domain_service import normalize_effort, require_owner
        if effective_project_id != previous_project_id or "owner_profile_id" in update_data and update_data["owner_profile_id"] != task.owner_profile_id:
            await require_owner(self.db, update_data.get("owner_profile_id", task.owner_profile_id), effective_project_id)
        if "owner_profile_id" in update_data:
            if update_data["owner_profile_id"] != task.owner_profile_id:
                update_data["ownership_provenance"] = "explicit" if update_data["owner_profile_id"] else "unassigned"
        if {"effort_days", "effort_hours", "estimate_provenance"}.intersection(update_data):
            estimate = normalize_effort(update_data, task.nominal_day_hours, current_hours=task.effort_hours)
            update_data.pop("effort_days", None)
            update_data.update({"effort_hours": estimate["effort_hours"], "_legacy_effort_days": estimate["effort_days"], "estimate_provenance": estimate["estimate_provenance"]})
        brief_input = update_data.pop("brief", None)
        from app.services.task_brief_service import TaskBriefService, render_brief
        if "brief" in data.model_fields_set and data.brief is None:
            raise ValueError("A canonical brief cannot be cleared; edit its fields instead")
        if task.brief is not None and "description" in update_data and update_data["description"] != render_brief(brief_input or task.brief):
            raise ValueError("This task has a canonical brief; reload and edit its structured fields")
        if brief_input is not None:
            if await TaskBriefService(self.db).apply_brief(task, data.brief):
                changed_fields["brief_revision"] = {"old": task.brief_revision - 1, "new": task.brief_revision}
            update_data.pop("description", None)

        # Convert tags list to JSON string
        if "tags" in update_data and update_data["tags"] is not None:
            update_data["tags"] = json.dumps(update_data["tags"])

        for field, value in update_data.items():
            old_value = getattr(task, field)
            if old_value != value:
                changed_fields[field] = {"old": old_value, "new": value}
                setattr(task, field, value)

        # Handle dependency updates
        if depends_on_ids is not None:
            await self._require_same_iteration_dependencies(task.iteration_id, depends_on_ids, task.project_id)
            await self._require_acyclic_dependencies(
                task_id,
                task.iteration_id,
                depends_on_ids,
            )
            # Get current dependency IDs
            current_dep_ids = {dep.depends_on_id for dep in task.dependencies}
            new_dep_ids = set(depends_on_ids)

            # Remove dependencies that are no longer in the list
            for dep in list(task.dependencies):
                if dep.depends_on_id not in new_dep_ids:
                    await self.db.delete(dep)

            # Add new dependencies
            for dep_id in new_dep_ids:
                if dep_id not in current_dep_ids:
                    # Avoid self-dependency
                    if dep_id != task_id:
                        new_dep = TaskDependency(task_id=task_id, depends_on_id=dep_id)
                        self.db.add(new_dep)
            if current_dep_ids != new_dep_ids:
                changed_fields["depends_on"] = {
                    "old": sorted(current_dep_ids),
                    "new": sorted(new_dep_ids),
                }

        if changed_fields and task.is_summary:
            for child_id in sorted((await self._task_subtree_ids(task.id)) - {task.id}):
                child = await self.db.get(Task, child_id)
                await self.reserve_task_version(child, child.version)
        if changed_fields:
            from app.services.task_brief_service import clear_acceptance, clear_execution_evidence
            if {"title", "description", "depends_on", "project_id"}.intersection(changed_fields):
                clear_execution_evidence(task)
            else:
                clear_acceptance(task)
            await self.reserve_task_version(task, expected_version)
            await self.record_task_event(
                task_id,
                "task_updated",
                {"changes": changed_fields, "version": task.version},
                actor_type=actor_type,
                actor_id=actor_id,
                trace_id=trace_id,
                span_id=span_id,
                correlation_id=correlation_id,
                idempotency_key=idempotency_key,
            )

        try:
            if changed_fields and task.parent_id is not None:
                await self.status_service.reconcile_parent_chain(task.parent_id, commit=False)
            if changed_fields:
                await emit_outbound_webhook_event(
                    self.db,
                    commit=False,
                    event_type="task.updated",
                    entity_type="task",
                    entity_id=task.id,
                    data={
                        "task_id": task.id,
                        "iteration_id": task.iteration_id,
                        "project_id": task.project_id,
                        "changes": changed_fields,
                        "version": task.version,
                    },
                )
            if commit:
                await commit_or_flush(self.db)
                await self.db.refresh(task)
            else:
                await self.db.flush()
        except Exception:
            await self.db.rollback()
            raise
        return await self.get_by_id(task_id)

    @atomic_command
    async def delete(
        self,
        task_id: int,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        *, expected_version: Optional[int] = None, expected_revision: Optional[int] = None,
    ) -> bool:
        """Delete a task and its subtasks."""
        iteration_id = await self.db.scalar(select(Task.iteration_id).where(Task.id == task_id))
        await self._lock_task_scope(task_id, expected_revisions={iteration_id: expected_revision} if expected_revision is not None else None, require_revisions=True, revision_field="expected_revision")
        task = await self.get_by_id(task_id)
        if not task:
            return False

        self.ensure_expected_version(task, expected_version)
        require_project(self.db, task.project_id, "edit")
        await self._require_unclaimed_structure(await self._task_subtree_ids(task_id))
        from app.services.delivery_dependency_service import DeliveryDependencyService
        from app.models.delivery_dependency import DeliveryDependency
        from sqlalchemy import delete
        subtree = await self._task_subtree_ids(task_id)
        await DeliveryDependencyService(self.db).require_unreferenced(subtree)
        await self.db.execute(delete(DeliveryDependency).where(DeliveryDependency.task_id.in_(subtree)))
        old_parent_id = task.parent_id
        # Create snapshot before deletion
        snapshot_service = SnapshotService(self.db)
        await snapshot_service.create_snapshot(task.iteration_id, f"before_delete_task_{task_id}")

        await self.record_task_event(
            task_id,
            "task_deleted",
            {"title": task.title, "iteration_id": task.iteration_id},
            actor_type=actor_type,
            actor_id=actor_id,
        )

        await self.db.flush()
        # The task is already authorized and locked; cleanup is restricted to its exact link rows.
        with self.db.no_autoflush, internal_authority(self.db):
            await ExternalLinkService(self.db).delete_for_entity("task", task_id)
        await self.db.delete(task)
        await self.db.flush()
        if old_parent_id is not None:
            await self.status_service.reconcile_parent_chain(old_parent_id, commit=False)
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="task.deleted",
                entity_type="task",
                entity_id=task_id,
                data={
                    "task_id": task_id,
                    "title": task.title,
                    "iteration_id": task.iteration_id,
                    "project_id": task.project_id,
                },
            )
            await commit_or_flush(self.db)
        except Exception:
            await self.db.rollback()
            raise
        return True

    @atomic_command
    async def add_dependency(
        self,
        task_id: int,
        depends_on_id: int,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        *, expected_version: Optional[int] = None,
    ) -> bool:
        """Add a dependency to a task."""
        task = await self._lock_dependency_task(task_id)
        if not task:
            return False
        require_project(self.db, task.project_id, "edit")
        self.ensure_expected_version(task, expected_version)

        # Prevent self-dependency
        if task_id == depends_on_id:
            return False

        await self._require_same_iteration_dependencies(
            task.iteration_id, [depends_on_id], task.project_id
        )
        await self._require_acyclic_dependencies(
            task_id,
            task.iteration_id,
            [dep.depends_on_id for dep in task.dependencies] + [depends_on_id],
        )

        # Check if dependency already exists
        existing = await self.db.execute(
            select(TaskDependency).where(
                TaskDependency.task_id == task_id,
                TaskDependency.depends_on_id == depends_on_id
            )
        )
        if existing.scalar_one_or_none():
            return True  # Already exists

        dependency = TaskDependency(task_id=task_id, depends_on_id=depends_on_id)
        self.db.add(dependency)
        from app.services.task_brief_service import clear_execution_evidence
        clear_execution_evidence(task)
        await self.reserve_task_version(task, task.version)
        await self.record_task_event(
            task_id,
            "dependency_added",
            {"depends_on_id": depends_on_id, "version": task.version},
            actor_type=actor_type,
            actor_id=actor_id,
        )
        await commit_or_flush(self.db)
        return True

    @atomic_command
    async def remove_dependency(
        self,
        task_id: int,
        depends_on_id: int,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        *, expected_version: Optional[int] = None,
    ) -> bool:
        """Remove a dependency from a task."""
        task = await self._lock_dependency_task(task_id)
        if not task:
            return False
        require_project(self.db, task.project_id, "edit")
        self.ensure_expected_version(task, expected_version)

        result = await self.db.execute(
            select(TaskDependency).where(
                TaskDependency.task_id == task_id,
                TaskDependency.depends_on_id == depends_on_id
            )
        )
        dependency = result.scalar_one_or_none()

        if not dependency:
            return False

        await self.db.delete(dependency)
        from app.services.task_brief_service import clear_execution_evidence
        clear_execution_evidence(task)
        await self.reserve_task_version(task, task.version)
        await self.record_task_event(
            task_id,
            "dependency_removed",
            {"depends_on_id": depends_on_id, "version": task.version},
            actor_type=actor_type,
            actor_id=actor_id,
        )
        await commit_or_flush(self.db)
        return True

    @atomic_command
    async def reorder_tasks(
        self,
        task_ids: list[int],
        iteration_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        expected_revision: int | None = None,
    ) -> bool:
        """Update sort_order for tasks within one declared sibling scope."""
        if iteration_id is not None:
            await lock_iterations(self.db, [iteration_id], expected={iteration_id: expected_revision} if expected_revision is not None else None, require_expected=True, revision_field="expected_revision")
        from sqlalchemy import update

        if not task_ids:
            raise ValueError("task_ids must not be empty")
        if len(set(task_ids)) != len(task_ids):
            raise ValueError("task_ids must not contain duplicates")
        if iteration_id is None:
            raise ValueError("iteration_id is required when reordering tasks")

        result = await self.db.execute(select(Task).where(Task.id.in_(task_ids)))
        tasks = list(result.scalars().all())
        if len(tasks) != len(task_ids):
            raise ValueError("All reordered tasks must exist")
        for task in tasks:
            if task.iteration_id != iteration_id:
                raise ValueError("All reordered tasks must belong to the declared iteration")
            if task.parent_id != parent_id:
                raise ValueError("All reordered tasks must belong to the declared parent scope")

        for task in tasks:
            require_project(self.db, task.project_id, "edit")
            await self._require_unclaimed_structure(await self._task_subtree_ids(task.id))
        by_id = {task.id: task for task in tasks}
        for index, task_id in enumerate(task_ids):
            task = by_id[task_id]
            await self._reserve_structural_version(task)
            task.sort_order = index
            await self.record_task_event(
                task_id,
                "task_reordered",
                {"sort_order": index},
                actor_type=actor_type,
                actor_id=actor_id,
            )
        await commit_or_flush(self.db)
        return True

    async def _reserve_structural_version(self, task: Task, *, preserve_inherited_facets=False):
        """Carry existing acceptance across a rearrangement that preserves leaf work meaning."""
        from app.services.work_metrics import task_signals
        signals = task_signals(task)
        previous_version = task.version
        accepted = signals["is_accepted"] and not task.is_summary
        if preserve_inherited_facets:
            task.is_deferred = signals["effective_is_deferred"]
            task.is_optional = signals["effective_is_optional"]
        await self.reserve_task_version(task, previous_version)
        if accepted:
            task.accepted_version = task.version
            await self.record_task_event(task.id, "acceptance_preserved_after_rearrangement", {
                "previous_version": previous_version, "current_version": task.version,
                "reason": "Hierarchy/order changed without changing the accepted leaf work or its effective facets",
            })

    @atomic_command
    async def merge_tasks(
        self,
        iteration_id: int,
        task_ids: list[int],
        parent_title: str,
        parent_description: Optional[str] = None,
        expected_revision: int | None = None,
    ) -> Optional[Task]:
        """
        Merge multiple leaf tasks under a new parent task.

        - All tasks must exist and belong to the same iteration
        - All tasks must have no children (leaf nodes only)
        - Creates a new parent task and updates parent_id for all merged tasks
        - Parent derives the lowest numeric priority from child tasks
        """
        if iteration_id is not None:
            await lock_iterations(self.db, [iteration_id], expected={iteration_id: expected_revision} if expected_revision is not None else None, require_expected=True, revision_field="expected_revision")
        import json

        # Validate minimum task count
        if len(task_ids) < 2 or len(set(task_ids)) != len(task_ids):
            return None

        iteration_project_id = await self._iteration_project_id(iteration_id)

        # Create snapshot before modification
        snapshot_service = SnapshotService(self.db)
        await snapshot_service.create_snapshot(iteration_id, "before_merge_tasks")

        # Fetch and validate all tasks
        tasks_to_merge: list[Task] = []
        project_ids: set[Optional[int]] = set()
        for task_id in task_ids:
            task = await self.get_by_id(task_id)
            if not task:
                return None  # Task doesn't exist
            if task.iteration_id != iteration_id:
                return None  # Task belongs to different iteration
            if task.is_summary or task.children:
                return None  # Task has children, cannot merge
            tasks_to_merge.append(task)
            project_ids.add(task.project_id)

        if iteration_project_id is not None:
            if any(project_id != iteration_project_id for project_id in project_ids):
                raise ValueError("Tasks in a scoped iteration must match the iteration project.")
            project_id = iteration_project_id
        else:
            if len(project_ids) != 1:
                return None  # All merged tasks must belong to the same project scope
            project_id = next(iter(project_ids))

        require_project(self.db, project_id, "edit")
        # Lower numeric values represent more urgent work.
        derived_priority = min(task.priority for task in tasks_to_merge)

        # Calculate date bounds from child tasks (if scheduled)
        start_dates = [task.start_date for task in tasks_to_merge if task.start_date]
        end_dates = [task.end_date for task in tasks_to_merge if task.end_date]

        parent_start_date = min(start_dates) if start_dates else None
        parent_end_date = max(end_dates) if end_dates else None

        # Create the new parent task
        parent_task = Task(
            iteration_id=iteration_id,
            project_id=project_id,
            parent_id=None,  # Root level
            title=parent_title,
            description=parent_description,
            priority=derived_priority,
            is_summary=True,
            effort_days=0.0,  # Composite tasks derive effort from children
            effort_hours=0.0,
            assignee_id=None,  # No assignee for composite tasks
            status=TaskStatus.PLANNED.value,
            is_optional=False,
            is_deferred=False,
            tags=json.dumps([]),
            sort_order=0,
            start_date=parent_start_date,
            end_date=parent_end_date,
        )
        self.db.add(parent_task)
        await commit_or_flush(self.db)
        await self.db.refresh(parent_task)

        old_parent_ids = {task.parent_id for task in tasks_to_merge if task.parent_id is not None}
        await self._require_unclaimed_structure([task.id for task in tasks_to_merge])
        # Update all merged tasks to have the new parent
        for idx, task in enumerate(tasks_to_merge):
            await self._reserve_structural_version(task, preserve_inherited_facets=True)
            task.parent_id = parent_task.id
            task.sort_order = idx
            await self.record_task_event(
                task.id,
                "task_merged",
                {"parent_task_id": parent_task.id, "sort_order": idx},
            )

        await self.record_task_event(
            parent_task.id,
            "task_created",
            {
                "title": parent_task.title,
                "iteration_id": iteration_id,
                "project_id": parent_task.project_id,
                "merged_task_ids": task_ids,
            },
        )

        await self.db.flush()
        await self.status_service.reconcile_parent_chain(parent_task.id, commit=False)
        for old_parent_id in sorted(old_parent_ids):
            await self.status_service.reconcile_parent_chain(old_parent_id, commit=False)
        await commit_or_flush(self.db)
        return await self.get_by_id(parent_task.id)

    @atomic_command
    async def unmerge_task(self, parent_task_id: int, delete_parent: bool = True, *, expected_revisions=None) -> list[Task]:
        """Promote children into the parent's sibling scope without losing referenced work."""
        await self._lock_task_scope(parent_task_id, expected_revisions=expected_revisions, require_revisions=True)
        parent = await self.get_by_id(parent_task_id)
        if parent is None or not parent.children:
            return []
        require_project(self.db, parent.project_id, "edit")
        await self._require_unclaimed_structure(await self._task_subtree_ids(parent.id))
        referenced = await self.db.scalar(select(TaskDependency.id).where(
            (TaskDependency.task_id == parent.id) | (TaskDependency.depends_on_id == parent.id)).limit(1))
        if referenced is not None:
            raise ValueError("A referenced summary cannot be unmerged until its dependencies are explicitly reconciled")
        await SnapshotService(self.db).create_snapshot(parent.iteration_id, "before_unmerge_task")
        children = list(parent.children)
        old_parent_id = parent.parent_id
        next_order = await self._get_next_child_sort_order(old_parent_id) if old_parent_id is not None else await self._get_next_root_sort_order(parent.iteration_id)
        for index, child in enumerate(children):
            await self._reserve_structural_version(child, preserve_inherited_facets=True)
            child.parent_id, child.sort_order = old_parent_id, next_order + index
            await self.record_task_event(child.id, "task_unmerged", {"previous_parent_id": parent.id, "parent_id": old_parent_id})
        await self.db.flush()
        from sqlalchemy.orm import attributes
        attributes.set_committed_value(parent, "children", [])
        if delete_parent:
            await self.db.delete(parent)
        else:
            await self.reserve_task_version(parent, parent.version)
            parent.is_summary = True
            parent.status = "planned"
            parent.effort_days = parent.effort_hours = 0.0
            parent.assignee_id = None
            parent.accepted_at = parent.accepted_by_principal_id = parent.accepted_version = None
        await self.db.flush()
        if old_parent_id is not None:
            await self.status_service.reconcile_parent_chain(old_parent_id, commit=False)
        return [await self.get_by_id(child.id) for child in children]

    async def _lock_task_scope(self, task_id, *, target_iteration_id=None, target_project_id=None, expected_revisions=None, require_revisions=False, revision_field="expected_revisions"):
        await lock_planning(self.db)
        hint = (await self.db.execute(select(Task.iteration_id, Task.project_id).where(Task.id == task_id))).first()
        if hint is None:
            return
        iteration_id, project_id = hint
        if iteration_id is None:
            from app.commands import lock_backlog_project
            projects = {project_id}
            if target_project_id is not None and target_project_id != project_id:
                require_project(self.db, project_id, "edit")
                require_project(self.db, target_project_id, "edit")
                projects.add(target_project_id)
            for scope in sorted(projects):
                await lock_backlog_project(self.db, scope)
            current = (await self.db.execute(select(Task.iteration_id, Task.project_id).where(Task.id == task_id))).first()
            if current != hint:
                from app.authority import AuthorityError
                raise AuthorityError("task_scope_changed", "Task scope changed. Reload before editing.", 409)
            from app.services.backlog_snapshot_service import BacklogSnapshotService
            for scope in sorted(projects):
                await BacklogSnapshotService(self.db).capture(scope, "before_task_change")
        ids = ([iteration_id] if iteration_id is not None else []) + ([target_iteration_id] if target_iteration_id is not None else [])
        await lock_iterations(self.db, ids, expected=expected_revisions, require_expected=require_revisions, revision_field=revision_field)

    async def _require_unclaimed_structure(self, task_ids):
        from app.models.agent import AgentTaskAssignment
        claimed = await self.db.scalar(select(Task.id).where(Task.id.in_(task_ids), Task.claimed_by.is_not(None)).limit(1))
        assignment = await self.db.scalar(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id.in_(task_ids),
            AgentTaskAssignment.state == "accepted").limit(1))
        if claimed is not None or assignment is not None:
            raise ValueError("Recover active execution before changing its hierarchy or assignment scope")

    async def _task_subtree_ids(self, root_task_id: int) -> set[int]:
        """Return the IDs in a task subtree, including the root."""
        subtree_ids = {root_task_id}
        frontier = [root_task_id]
        while frontier:
            result = await self.db.execute(
                select(Task.id).where(Task.parent_id.in_(frontier))
            )
            child_ids = [row[0] for row in result.all()]
            new_child_ids = [task_id for task_id in child_ids if task_id not in subtree_ids]
            if not new_child_ids:
                break
            subtree_ids.update(new_child_ids)
            frontier = new_child_ids
        return subtree_ids

    async def _require_no_cross_subtree_dependencies(
        self,
        subtree_ids: set[int],
    ) -> None:
        """Reject moves that would leave dependency edges crossing work scopes."""
        from app.authority import internal_authority
        # Inspect only edge existence so hidden neighboring work cannot be stranded.
        with internal_authority(self.db):
            crossing = await self.db.scalar(select(TaskDependency.id).where(or_(
                and_(TaskDependency.task_id.in_(subtree_ids), TaskDependency.depends_on_id.notin_(subtree_ids)),
                and_(TaskDependency.depends_on_id.in_(subtree_ids), TaskDependency.task_id.notin_(subtree_ids)),
            )).limit(1))
        if crossing is not None:
            raise ValueError("Task move would leave dependencies crossing work scopes.")

    async def _resolve_project_for_move(
        self,
        task: Task,
        target_iteration_id: int,
        target_parent: Optional[Task],
    ) -> Optional[int]:
        """Resolve the project assignment for a task subtree move."""
        target_scope_project_id = await self._iteration_project_id(target_iteration_id)
        if target_scope_project_id is not None:
            if task.project_id not in (None, target_scope_project_id):
                raise ValueError("Task project must match the scoped iteration project.")
            if target_parent is not None and target_parent.project_id != target_scope_project_id:
                raise ValueError("Parent task project must match the scoped iteration project.")
            return target_scope_project_id

        if target_parent is None:
            return task.project_id

        if task.project_id is None:
            return target_parent.project_id
        if task.project_id != target_parent.project_id:
            raise ValueError("Moved subtask project must match parent task project.")
        return task.project_id

    @atomic_command
    async def move_task(
        self,
        task_id: int,
        target_iteration_id: int,
        parent_id: Optional[int] = None,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        expected_version: Optional[int] = None,
        expected_revisions: dict[int, int] | None = None,
    ) -> Optional[Task]:
        """Move a task subtree to an iteration, applying scoped project inheritance."""
        await self._lock_task_scope(task_id, target_iteration_id=target_iteration_id, expected_revisions=expected_revisions, require_revisions=True)
        task = await self.get_by_id(task_id)
        if not task:
            return None
        self.ensure_expected_version(task, expected_version)

        await self.require_iteration_exists(target_iteration_id)
        subtree_ids = await self._task_subtree_ids(task_id)

        target_parent: Optional[Task] = None
        if parent_id is not None:
            if parent_id in subtree_ids:
                raise ValueError("Task cannot be moved under itself or its descendants.")
            target_parent = await self.get_by_id(parent_id)
            if target_parent is None:
                raise ValueError(f"Parent task with id {parent_id} not found")
            if target_parent.iteration_id != target_iteration_id:
                raise ValueError("Parent task must belong to the target iteration.")

        if target_iteration_id != task.iteration_id:
            await self._require_no_cross_subtree_dependencies(subtree_ids)

        effective_project_id = await self._resolve_project_for_move(
            task,
            target_iteration_id,
            target_parent,
        )

        result = await self.db.execute(select(Task).where(Task.id.in_(subtree_ids)))
        moving_tasks = list(result.scalars().all())
        for moving_task in moving_tasks:
            if moving_task.project_id not in (None, effective_project_id):
                raise ValueError("Moved task project must match the target iteration project.")
            if moving_task.milestone_id is not None and not await self._milestone_matches_project(
                moving_task.milestone_id,
                effective_project_id,
            ):
                raise ValueError("Task milestone must belong to the target iteration project.")
            from app.services.task_domain_service import require_owner
            if moving_task.project_id != effective_project_id:
                await require_owner(self.db, moving_task.owner_profile_id, effective_project_id)

        require_project(self.db, task.project_id, "edit")
        require_project(self.db, effective_project_id, "edit")
        await self._require_unclaimed_structure(subtree_ids)
        old_parent_id = task.parent_id
        if target_parent is not None:
            await self._require_unclaimed_structure([target_parent.id])
            if not target_parent.children and not target_parent.is_summary and target_parent.status != "planned":
                raise ValueError("Executed leaf work cannot be silently converted into a summary")
        snapshot_service = SnapshotService(self.db)
        await snapshot_service.create_snapshot(task.iteration_id, f"before_move_task_{task_id}")
        if target_iteration_id != task.iteration_id:
            await snapshot_service.create_snapshot(target_iteration_id, f"before_receive_task_{task_id}")

        next_sort_order = (
            await self._get_next_child_sort_order(parent_id)
            if parent_id is not None
            else await self._get_next_root_sort_order(target_iteration_id)
        )
        any_changes = any(
            moving_task.iteration_id != target_iteration_id
            or moving_task.project_id != effective_project_id
            for moving_task in moving_tasks
        ) or task.parent_id != parent_id or task.sort_order != next_sort_order
        if any_changes:
            await self.reserve_task_version(task, expected_version)

        changed_task_ids: list[int] = []
        for moving_task in moving_tasks:
            changes: dict[str, dict[str, Any]] = {}
            if moving_task.iteration_id != target_iteration_id:
                changes["iteration_id"] = {
                    "old": moving_task.iteration_id,
                    "new": target_iteration_id,
                }
                moving_task.iteration_id = target_iteration_id
                if moving_task.assignee_id is not None:
                    changes["assignee_id"] = {"old": moving_task.assignee_id, "new": None}
                    moving_task.assignee_id = None
                from app.services.task_domain_service import nominal_day_hours
                moving_task.nominal_day_hours = await nominal_day_hours(self.db, target_iteration_id)
                moving_task._legacy_effort_days = moving_task.effort_days
                moving_task.start_date = moving_task.end_date = moving_task.calculated_effort_days = None
            if moving_task.project_id != effective_project_id:
                changes["project_id"] = {
                    "old": moving_task.project_id,
                    "new": effective_project_id,
                }
                moving_task.project_id = effective_project_id

            if moving_task.id == task_id:
                if moving_task.parent_id != parent_id:
                    changes["parent_id"] = {"old": moving_task.parent_id, "new": parent_id}
                    moving_task.parent_id = parent_id
                if moving_task.sort_order != next_sort_order:
                    changes["sort_order"] = {
                        "old": moving_task.sort_order,
                        "new": next_sort_order,
                    }
                    moving_task.sort_order = next_sort_order

            should_record = bool(changes) or (moving_task.id == task_id and any_changes)
            if should_record:
                if moving_task.id != task_id:
                    moving_task.version += 1
                changed_task_ids.append(moving_task.id)
                await self.record_task_event(
                    moving_task.id,
                    "task_moved",
                    {
                        "changes": changes,
                        "version": moving_task.version,
                        "target_iteration_id": target_iteration_id,
                        "moved_subtree_root_id": task_id,
                    },
                    actor_type=actor_type,
                    actor_id=actor_id,
                )

        await self.db.flush()
        for affected_parent in sorted({pid for pid in [old_parent_id, parent_id] if pid is not None}):
            await self.status_service.reconcile_parent_chain(affected_parent, commit=False)
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="task.moved",
                entity_type="task",
                entity_id=task_id,
                data={
                    "task_id": task_id,
                    "target_iteration_id": target_iteration_id,
                    "parent_id": parent_id,
                    "project_id": effective_project_id,
                    "changed_task_ids": changed_task_ids,
                },
            )
            await commit_or_flush(self.db)
        except Exception:
            await self.db.rollback()
            raise
        return await self.get_by_id(task_id)

    def task_to_response(self, task: Task, iteration_end_date: Optional[date] = None) -> TaskResponse:
        """Convert Task model to TaskResponse schema."""
        from sqlalchemy.orm import attributes

        from app.models.iteration import Iteration
        from app.commands import current_command
        command = current_command(self.db)
        iteration = self.db.identity_map.get((Iteration, (task.iteration_id,), None))
        iteration_revision = (command.iterations[task.iteration_id] + 1
            if command and task.iteration_id in command.iterations
            else iteration.revision if iteration is not None else None)

        state = attributes.instance_state(task)

        # Safely check if relationships are loaded to avoid lazy loading in async
        children_loaded = 'children' in state.dict
        dependencies_loaded = 'dependencies' in state.dict
        project_loaded = 'project' in state.dict
        milestone_loaded = 'milestone' in state.dict
        assignee_loaded = 'assignee' in state.dict
        claimed_agent_loaded = 'claimed_agent' in state.dict
        external_links_loaded = 'external_links' in state.dict
        request_source_links_loaded = 'request_source_links' in state.dict

        loaded_children = task.children if children_loaded else []
        loaded_dependencies = task.dependencies if dependencies_loaded else []
        loaded_project = task.project if project_loaded else None
        loaded_milestone = task.milestone if milestone_loaded else None
        loaded_assignee = task.assignee if assignee_loaded else None
        loaded_claimed_agent = task.claimed_agent if claimed_agent_loaded else None
        loaded_external_links = task.external_links if external_links_loaded else []
        loaded_request_source_links = (
            task.request_source_links if request_source_links_loaded else []
        )

        is_composite = bool(task.is_summary) or len(loaded_children) > 0
        from app.services.work_metrics import task_signals
        signals = task_signals(task, iteration_end=iteration_end_date,
            project_target=loaded_project.target_date if loaded_project else None,
            timezone=loaded_project.timezone if loaded_project else (iteration.__dict__.get("calendar").timezone if iteration is not None and iteration.__dict__.get("calendar") else "UTC"), composite=is_composite)
        is_overdue, is_delayed = signals.pop("is_overdue"), signals["is_late_start"]

        assignee = None
        if loaded_assignee:
            assignee = TaskAssignee(id=loaded_assignee.id, name=loaded_assignee.name)

        project = None
        if loaded_project:
            project = TaskProject(
                id=loaded_project.id,
                name=loaded_project.name,
                status=loaded_project.status,
                health=loaded_project.health,
            )

        milestone = None
        if loaded_milestone:
            milestone = TaskMilestone(
                id=loaded_milestone.id,
                project_id=loaded_milestone.project_id,
                name=loaded_milestone.name,
                status=loaded_milestone.status,
                target_date=loaded_milestone.target_date,
            )

        claimed_by = None
        if loaded_claimed_agent:
            claimed_by = TaskClaimedBy(
                id=loaded_claimed_agent.id,
                name=loaded_claimed_agent.name,
                display_name=loaded_claimed_agent.display_name,
            )

        children = [
            self.task_to_response(child, iteration_end_date)
            for child in loaded_children
        ]

        dependencies = [dep.depends_on_id for dep in loaded_dependencies]

        # Parse tags from JSON string
        import json
        try:
            tags = json.loads(task.tags) if task.tags else []
        except (json.JSONDecodeError, TypeError):
            tags = []
        agent_readiness = evaluate_agent_readiness(
            task,
            tags=tags,
            children=loaded_children,
            dependencies=loaded_dependencies,
            capability_slugs=self.agent_capability_slugs,
        )

        return TaskResponse(
            id=task.id,
            iteration_revision=iteration_revision,
            iteration_id=task.iteration_id,
            project_id=task.project_id,
            milestone_id=task.milestone_id,
            parent_id=task.parent_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            effort_days=task.effort_days,
            effort_hours=task.effort_hours,
            nominal_day_hours=task.nominal_day_hours,
            estimate_provenance=task.estimate_provenance,
            owner_profile_id=task.owner_profile_id,
            owner=TaskAssignee(id=task.owner_profile_id, name=task.__dict__["_owner_name"]) if task.__dict__.get("_owner_name") else None,
            ownership_provenance=task.ownership_provenance,
            blocked_reason=task.blocked_reason, canceled_at=task.canceled_at, canceled_reason=task.canceled_reason,
            execution_mode=task.execution_mode, brief=task.brief, brief_revision=task.brief_revision,
            brief_provenance=task.brief_provenance, legacy_description=task.legacy_description,
            brief_migration_notes=task.brief_migration_notes or [], artifact_revision=task.artifact_revision, progress=task.progress,
            project=project,
            milestone=milestone,
            assignee=assignee,
            status=task.status,
            start_date=task.start_date,
            end_date=task.end_date,
            actual_start_date=task.actual_start_date,
            actual_end_date=task.actual_end_date,
            min_start_date=task.min_start_date,
            max_end_date=task.max_end_date,
            is_overdue=is_overdue,
            is_delayed=is_delayed,
            **signals,
            baseline_start_date=task.baseline_start_date, baseline_end_date=task.baseline_end_date,
            baseline_revision=task.baseline_revision, baseline_provenance=task.baseline_provenance,
            started_at=task.started_at, resolved_at=task.resolved_at, accepted_at=task.accepted_at,
            is_composite=is_composite,
            is_optional=task.is_optional,
            is_deferred=task.is_deferred,
            tags=tags,
            sort_order=task.sort_order,
            external_key=task.external_key,
            source=task.source,
            source_url=task.source_url,
            external_links=ExternalLinkService(self.db).task_links_to_response(
                task,
                loaded_external_links,
            ),
            request_count=len(loaded_request_source_links),
            agent_readiness=agent_readiness,
            version=task.version,
            claimed_by=claimed_by,
            claim_expires_at=task.claim_expires_at,
            updated_at=task.updated_at,
            children=children,
            dependencies=dependencies,
        )

    async def _get_next_root_sort_order(self, iteration_id: int) -> int:
        """Return the next root-level sort order for an iteration."""
        result = await self.db.execute(
            select(Task)
            .where(Task.iteration_id == iteration_id, Task.parent_id.is_(None))
            .order_by(Task.sort_order.desc(), Task.id.desc())
        )
        existing = result.scalars().first()
        return (existing.sort_order + 1) if existing else 0

    async def _get_next_child_sort_order(self, parent_id: int) -> int:
        """Return the next child sort order under a parent task."""
        result = await self.db.execute(
            select(Task)
            .where(Task.parent_id == parent_id)
            .order_by(Task.sort_order.desc(), Task.id.desc())
        )
        existing = result.scalars().first()
        return (existing.sort_order + 1) if existing else 0

    @property
    def import_service(self):
        """Return the focused text import collaborator behind this facade."""
        if self._import_service is None:
            from app.services.task_import_service import TaskImportService

            self._import_service = TaskImportService(self.db, self)
        return self._import_service

    @atomic_command
    async def import_tasks(
        self,
        iteration_id: int,
        text: str,
        destination: TaskImportDestination = "tasks",
        *, expected_revision: int | None = None,
    ) -> tuple[list[Task], list[TriageItem]]:
        """Delegate task and triage text imports to TaskImportService."""
        require_project(self.db, await self._iteration_project_id(iteration_id), "edit")
        await lock_iterations(self.db, [iteration_id], expected={iteration_id: expected_revision} if expected_revision is not None else None, require_expected=True, revision_field="expected_revision")
        return await self.import_service.import_tasks(iteration_id, text, destination)

    async def get_tasks_as_text(self, iteration_id: int) -> str:
        """Delegate editable task text serialization to TaskImportService."""
        return await self.import_service.get_tasks_as_text(iteration_id)

    @atomic_command
    async def bulk_update_tasks_from_text(
        self,
        iteration_id: int,
        text: str,
        destination: TaskImportDestination = "tasks",
        *, expected_revision: int | None = None,
    ) -> tuple[list[Task], list[TriageItem]]:
        """Delegate bulk text edits to TaskImportService."""
        require_project(self.db, await self._iteration_project_id(iteration_id), "edit")
        await lock_iterations(self.db, [iteration_id], expected={iteration_id: expected_revision} if expected_revision is not None else None, require_expected=True, revision_field="expected_revision")
        return await self.import_service.bulk_update_tasks_from_text(
            iteration_id,
            text,
            destination,
        )

    VALID_TRANSITIONS = {
        TaskStatus.PLANNED.value: [TaskStatus.ACTIVE.value],
        TaskStatus.ACTIVE.value: [TaskStatus.RESOLVED.value],
        TaskStatus.RESOLVED.value: [TaskStatus.ACTIVE.value, TaskStatus.CLOSED.value],
        TaskStatus.CLOSED.value: [],
    }

    @property
    def status_service(self):
        """Return the focused status collaborator behind this facade."""
        if self._status_service is None:
            from app.services.task_status_service import TaskStatusService

            self._status_service = TaskStatusService(self.db, self)
        return self._status_service

    @atomic_command
    async def change_status(
        self,
        task_id: int,
        new_status: TaskStatus | str,
        reason: Optional[str] = None,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        expected_version: Optional[int] = None,
        commit: bool = True,
        reserve_version: bool = True,
        manual_execution: bool = False,
        review_evidence: str = "",
        review_rework: bool = False,
    ) -> tuple[Optional[Task], list[dict], bool]:
        """Delegate status transitions to TaskStatusService."""
        return await self.status_service.change_status(
            task_id,
            new_status,
            reason=reason,
            actor_type=actor_type,
            actor_id=actor_id,
            trace_id=trace_id,
            span_id=span_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            expected_version=expected_version,
            commit=commit,
            reserve_version=reserve_version,
            manual_execution=manual_execution,
            review_evidence=review_evidence,
            review_rework=review_rework,
        )

    async def _update_parent_status(self, parent_id: int) -> None:
        """Compatibility seam for parent reconciliation."""
        await self.status_service.reconcile_parent_chain(parent_id)

    async def _cascade_update_dependents(
        self,
        source_task: Task,
        original_end_date: date,
        reason: str,
    ) -> list[dict]:
        """Compatibility seam for dependent date cascade."""
        return await self.status_service.cascade_update_dependents(
            source_task,
            original_end_date,
            reason,
        )

    async def get_status_history(self, task_id: int) -> list[Any]:
        """Delegate task status history reads."""
        return await self.status_service.get_status_history(task_id)

    async def get_overdue_tasks(self, iteration_id: int) -> Sequence[Task]:
        """Delegate overdue task reads."""
        return await self.status_service.get_overdue_tasks(iteration_id)

    async def get_iteration_status_history(
        self,
        iteration_id: int,
        limit: int = 50,
    ) -> list[Any]:
        """Delegate iteration status history reads."""
        return await self.status_service.get_iteration_status_history(iteration_id, limit)

    async def get_iteration_status_stats(self, iteration_id: int) -> list[dict]:
        """Delegate transition statistics."""
        return await self.status_service.get_iteration_status_stats(iteration_id)
