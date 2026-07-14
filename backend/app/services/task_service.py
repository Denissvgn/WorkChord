"""Task service with business logic."""
import json
from datetime import date
from typing import Any, Optional, Sequence

from sqlalchemy import select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import attributes, selectinload

from app.models.agent import TaskEvent
from app.models.iteration import Iteration
from app.models.project import Project, ProjectMilestone
from app.models.request_source import RequestSourceLink
from app.models.task import Task, TaskDependency, TaskStatus
from app.models.team_member import TeamMember
from app.models.triage import TriageItem
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
    ) -> None:
        """Validate that task dependencies stay inside one iteration schedule graph."""
        dependency_id_set = set(dependency_ids)
        if not dependency_id_set:
            return

        result = await self.db.execute(
            select(Task.id, Task.iteration_id).where(Task.id.in_(dependency_id_set))
        )
        dependency_iterations = {
            task_id: dependency_iteration_id
            for task_id, dependency_iteration_id in result.all()
        }

        for dependency_id in dependency_id_set:
            dependency_iteration_id = dependency_iterations.get(dependency_id)
            if dependency_iteration_id is None:
                raise ValueError(f"Dependency task with id {dependency_id} not found")
            if dependency_iteration_id != iteration_id:
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
        hint_result = await self.db.execute(
            select(Task.iteration_id).where(Task.id == task_id)
        )
        iteration_id = hint_result.scalar_one_or_none()
        if iteration_id is None:
            return None
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
                child.version += 1
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
        if expected_version is not None and task.version != expected_version:
            raise TaskVersionConflictError(expected_version, self._metadata_from_task(task))

    async def reserve_task_version(
        self,
        task: Task,
        expected_version: int | None,
    ) -> int:
        """Atomically reserve the next task version at the database write boundary."""
        statement = sql_update(Task).where(Task.id == task.id)
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
            current = await self._current_task_metadata(task.id)
            if current is None:
                raise ValueError(f"Task with id {task.id} not found")
            if expected_version is None:
                expected_version = task.version
            raise TaskVersionConflictError(expected_version, current)

        attributes.set_committed_value(task, "version", row.version)
        if row.updated_at is not None:
            attributes.set_committed_value(task, "updated_at", row.updated_at)
        return row.version

    async def get_by_iteration(
        self,
        iteration_id: int,
        include_children: bool = True
    ) -> Sequence[Task]:
        """Get an unbounded iteration tree assembled from one flat task query."""
        if not include_children:
            result = await self.db.execute(
                self._task_graph_query(iteration_id).where(Task.parent_id.is_(None))
            )
            return result.scalars().all()
        roots, _ = await self._load_iteration_tree(iteration_id)
        return roots

    def _task_graph_query(self, iteration_id: int):
        """Build the bounded relationship query used before in-memory tree assembly."""
        return (
            select(Task)
            .where(Task.iteration_id == iteration_id)
            .execution_options(populate_existing=True)
            .options(
                selectinload(Task.project),
                selectinload(Task.milestone),
                selectinload(Task.assignee).selectinload(TeamMember.vacations),
                selectinload(Task.claimed_agent),
                selectinload(Task.external_links),
                selectinload(Task.request_source_links).selectinload(
                    RequestSourceLink.request_source
                ),
                selectinload(Task.dependencies).selectinload(TaskDependency.depends_on),
            )
            .order_by(Task.sort_order, Task.id)
        )

    async def _load_iteration_tree(
        self,
        iteration_id: int,
    ) -> tuple[list[Task], dict[int, Task]]:
        """Load and defensively assemble every task in one iteration."""
        result = await self.db.execute(self._task_graph_query(iteration_id))
        tasks = list(result.scalars().all())
        tasks_by_id = {task.id: task for task in tasks}

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
        result = await self.db.execute(select(Task.iteration_id).where(Task.id == task_id))
        iteration_id = result.scalar_one_or_none()
        if iteration_id is None:
            return None
        _, tasks_by_id = await self._load_iteration_tree(iteration_id)
        return tasks_by_id.get(task_id)

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
        await self.require_iteration_exists(iteration_id)
        await self._require_same_iteration_dependencies(iteration_id, data.depends_on)

        effort_hours = data.effort_hours if data.effort_hours else data.effort_days * 8
        project_id = data.project_id
        milestone_id = data.milestone_id

        if data.parent_id is not None:
            parent = await self.get_by_id(data.parent_id)
            if not parent:
                raise ValueError(f"Parent task with id {data.parent_id} not found")
            if parent.iteration_id != iteration_id:
                raise ValueError("Parent task must belong to the same iteration.")
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
        await self._require_milestone_compatible(milestone_id, project_id)
        await self.require_iteration_assignee(data.assignee_id, iteration_id)

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
            effort_days=data.effort_days,
            effort_hours=effort_hours,
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
                await self.db.commit()
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
        task = await self.get_by_id(task_id)
        if not task:
            return None

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

        # Auto-calculate effort_hours if effort_days changed
        if "effort_days" in update_data and "effort_hours" not in update_data:
            update_data["effort_hours"] = update_data["effort_days"] * 8

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
            await self._require_same_iteration_dependencies(task.iteration_id, depends_on_ids)
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

        if changed_fields:
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
                await self.db.commit()
                await self.db.refresh(task)
            else:
                await self.db.flush()
        except Exception:
            await self.db.rollback()
            raise
        return await self.get_by_id(task_id)

    async def delete(
        self,
        task_id: int,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
    ) -> bool:
        """Delete a task and its subtasks."""
        task = await self.get_by_id(task_id)
        if not task:
            return False

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

        await ExternalLinkService(self.db).delete_for_entity("task", task_id)
        await self.db.delete(task)
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
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        return True

    async def add_dependency(
        self,
        task_id: int,
        depends_on_id: int,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
    ) -> bool:
        """Add a dependency to a task."""
        task = await self._lock_dependency_task(task_id)
        if not task:
            return False

        # Prevent self-dependency
        if task_id == depends_on_id:
            return False

        await self._require_same_iteration_dependencies(
            task.iteration_id, [depends_on_id]
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
        await self.reserve_task_version(task, task.version)
        await self.record_task_event(
            task_id,
            "dependency_added",
            {"depends_on_id": depends_on_id, "version": task.version},
            actor_type=actor_type,
            actor_id=actor_id,
        )
        await self.db.commit()
        return True

    async def remove_dependency(
        self,
        task_id: int,
        depends_on_id: int,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
    ) -> bool:
        """Remove a dependency from a task."""
        task = await self._lock_dependency_task(task_id)
        if not task:
            return False

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
        await self.reserve_task_version(task, task.version)
        await self.record_task_event(
            task_id,
            "dependency_removed",
            {"depends_on_id": depends_on_id, "version": task.version},
            actor_type=actor_type,
            actor_id=actor_id,
        )
        await self.db.commit()
        return True

    async def reorder_tasks(
        self,
        task_ids: list[int],
        iteration_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
    ) -> bool:
        """Update sort_order for tasks within one declared sibling scope."""
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

        for index, task_id in enumerate(task_ids):
            await self.db.execute(
                update(Task)
                .where(
                    Task.id == task_id,
                    Task.iteration_id == iteration_id,
                    Task.parent_id == parent_id,
                )
                .values(sort_order=index)
            )
            await self.record_task_event(
                task_id,
                "task_reordered",
                {"sort_order": index},
                actor_type=actor_type,
                actor_id=actor_id,
            )
        await self.db.commit()
        return True

    async def merge_tasks(
        self,
        iteration_id: int,
        task_ids: list[int],
        parent_title: str,
        parent_description: Optional[str] = None,
    ) -> Optional[Task]:
        """
        Merge multiple leaf tasks under a new parent task.

        - All tasks must exist and belong to the same iteration
        - All tasks must have no children (leaf nodes only)
        - Creates a new parent task and updates parent_id for all merged tasks
        - Parent inherits maximum priority from child tasks
        """
        import json

        # Validate minimum task count
        if len(task_ids) < 2:
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
            if task.children and len(task.children) > 0:
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

        # Calculate maximum priority from child tasks
        max_priority = max(task.priority for task in tasks_to_merge)

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
            priority=max_priority,
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
        await self.db.commit()
        await self.db.refresh(parent_task)

        # Update all merged tasks to have the new parent
        for idx, task in enumerate(tasks_to_merge):
            task.parent_id = parent_task.id
            task.sort_order = idx
            task.version += 1
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

        await self.db.commit()

        return await self.get_by_id(parent_task.id)

    async def unmerge_task(
        self,
        parent_task_id: int,
        delete_parent: bool = True
    ) -> list[Task]:
        """
        Promote all child tasks of a parent to the top level.

        - Parent task must exist and have children
        - All children become root-level tasks (parent_id = None)
        - Optionally deletes the parent task after unmerging

        Returns list of promoted tasks.
        """
        from sqlalchemy import update, delete as sql_delete, text

        # First, get the parent task info and children IDs using raw SQL
        result = await self.db.execute(
            select(Task.id, Task.iteration_id)
            .where(Task.id == parent_task_id)
        )
        parent_row = result.first()
        if not parent_row:
            return []

        iteration_id = parent_row.iteration_id

        # Get child IDs
        children_result = await self.db.execute(
            select(Task.id).where(Task.parent_id == parent_task_id)
        )
        child_ids = [row[0] for row in children_result.fetchall()]

        if not child_ids:
            return []

        # Create snapshot before modification
        snapshot_service = SnapshotService(self.db)
        await snapshot_service.create_snapshot(iteration_id, "before_unmerge_task")

        # Get current max sort_order for root tasks
        result = await self.db.execute(
            select(Task.sort_order)
            .where(Task.iteration_id == iteration_id, Task.parent_id.is_(None))
            .order_by(Task.sort_order.desc())
            .limit(1)
        )
        max_order_row = result.first()
        next_sort_order = (max_order_row[0] + 1) if max_order_row else 0

        # Update all children to have no parent using raw SQL
        for idx, child_id in enumerate(child_ids):
            await self.db.execute(
                update(Task)
                .where(Task.id == child_id)
                .values(parent_id=None, sort_order=next_sort_order + idx, version=Task.version + 1)
            )
            await self.record_task_event(
                child_id,
                "task_unmerged",
                {
                    "previous_parent_id": parent_task_id,
                    "sort_order": next_sort_order + idx,
                },
            )

        await self.db.commit()

        # Delete the parent using raw SQL (completely bypasses ORM)
        if delete_parent:
            await self.db.execute(
                sql_delete(Task).where(Task.id == parent_task_id)
            )
            await self.db.commit()

        # Clear session to avoid stale data
        await self.db.close()

        # Return empty list - the API will refetch via frontend
        # This avoids any ORM state issues
        return []

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
        """Reject moves that would leave dependency edges crossing iterations."""
        result = await self.db.execute(
            select(TaskDependency).where(
                TaskDependency.task_id.in_(subtree_ids),
                TaskDependency.depends_on_id.notin_(subtree_ids),
            )
        )
        if result.scalars().first() is not None:
            raise ValueError("Task move would leave dependencies crossing iterations.")

        result = await self.db.execute(
            select(TaskDependency).where(
                TaskDependency.depends_on_id.in_(subtree_ids),
                TaskDependency.task_id.notin_(subtree_ids),
            )
        )
        if result.scalars().first() is not None:
            raise ValueError("Task move would leave dependencies crossing iterations.")

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

    async def move_task(
        self,
        task_id: int,
        target_iteration_id: int,
        parent_id: Optional[int] = None,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        expected_version: Optional[int] = None,
    ) -> Optional[Task]:
        """Move a task subtree to an iteration, applying scoped project inheritance."""
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
            await self.require_iteration_assignee(
                moving_task.assignee_id,
                target_iteration_id,
            )

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
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        return await self.get_by_id(task_id)

    def task_to_response(self, task: Task, iteration_end_date: Optional[date] = None) -> TaskResponse:
        """Convert Task model to TaskResponse schema."""
        from sqlalchemy.orm import attributes

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

        is_composite = len(loaded_children) > 0
        is_overdue = False
        is_delayed = False

        today = date.today()

        if iteration_end_date and task.end_date:
            is_overdue = task.end_date > iteration_end_date

        # Task is delayed if: status is PLANNED and start_date has passed
        if task.status == TaskStatus.PLANNED.value and task.start_date:
            is_delayed = task.start_date < today

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
            iteration_id=task.iteration_id,
            project_id=task.project_id,
            milestone_id=task.milestone_id,
            parent_id=task.parent_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            effort_days=task.effort_days,
            effort_hours=task.effort_hours,
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
            .order_by(Task.sort_order.desc())
        )
        existing = result.scalars().first()
        return (existing.sort_order + 1) if existing else 0

    async def _get_next_child_sort_order(self, parent_id: int) -> int:
        """Return the next child sort order under a parent task."""
        result = await self.db.execute(
            select(Task)
            .where(Task.parent_id == parent_id)
            .order_by(Task.sort_order.desc())
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

    async def import_tasks(
        self,
        iteration_id: int,
        text: str,
        destination: TaskImportDestination = "tasks",
    ) -> tuple[list[Task], list[TriageItem]]:
        """Delegate task and triage text imports to TaskImportService."""
        return await self.import_service.import_tasks(iteration_id, text, destination)

    async def get_tasks_as_text(self, iteration_id: int) -> str:
        """Delegate editable task text serialization to TaskImportService."""
        return await self.import_service.get_tasks_as_text(iteration_id)

    async def bulk_update_tasks_from_text(
        self,
        iteration_id: int,
        text: str,
        destination: TaskImportDestination = "tasks",
    ) -> tuple[list[Task], list[TriageItem]]:
        """Delegate bulk text edits to TaskImportService."""
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
