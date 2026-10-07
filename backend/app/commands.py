"""Explicit transaction ownership shared by HTTP, MCP and service commands."""

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from functools import wraps
from typing import Literal

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class CommandState:
    mode: Literal["apply", "preview"] = "apply"
    iterations: dict[int, int] = field(default_factory=dict)
    versioned_iterations: set[int] = field(default_factory=set)
    missing_revision_observations: set[tuple[str, str, int]] = field(default_factory=set)
    snapshots: set[int | tuple[str, int]] = field(default_factory=set)
    tasks: dict[int, int] = field(default_factory=dict)
    backlog_projects: set[int] = field(default_factory=set)
    failed: bool = False
    planning_revision: int | None = None


class AggregateVersionConflict(RuntimeError):
    def __init__(self, iteration_id: int, expected: int, current: int):
        self.iteration_id, self.expected, self.current = iteration_id, expected, current
        super().__init__("The iteration changed. Reload its current state before applying this command.")

    def detail(self):
        return {"code": "iteration_version_conflict", "iteration_id": self.iteration_id,
                "expected_revision": self.expected, "current_revision": self.current,
                "message": str(self)}


class HierarchyScopeError(RuntimeError):
    def detail(self):
        return {"code": "hierarchy_reconciliation_required", "message": "This scope contains unresolved hierarchy data. Ask an operator to run its hierarchy audit."}


class PlanningConflict(RuntimeError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)

    def detail(self):
        return {"code": self.code, "message": str(self)}


async def lock_planning(db, *, expected=None):
    """Reserve shared planning before narrower locks, once per command including previews."""
    from app.authority import internal_authority
    from app.models.capacity import PlanningState
    state = current_command(db)
    if state is None:
        raise RuntimeError("Shared planning requires a command transaction")
    if state.planning_revision is None:
        if db.bind.dialect.name == "postgresql":
            from sqlalchemy.dialects.postgresql import insert
        else:
            from sqlalchemy.dialects.sqlite import insert
        with internal_authority(db):
            await db.execute(insert(PlanningState).values(id=1, revision=0).on_conflict_do_nothing())
            # An actual write obtains the same serialization on SQLite as PostgreSQL.
            state.planning_revision = await db.scalar(update(PlanningState).where(PlanningState.id == 1)
                .values(revision=PlanningState.revision + 1).returning(PlanningState.revision)) - 1
    if expected is not None and expected != state.planning_revision:
        raise PlanningConflict("planning_version_conflict", "Shared availability changed. Calculate the schedule again.")
    return state.planning_revision


def current_command(db) -> CommandState | None:
    info = getattr(db, "info", None)
    return info.get("command") if isinstance(info, dict) else None


async def commit_or_flush(db) -> None:
    """Collaborators flush under an owner; standalone legacy calls retain commit behavior."""
    if current_command(db) is not None:
        await db.flush()
    else:
        await db.commit()


@asynccontextmanager
async def command_transaction(db: AsyncSession, *, mode="apply", commit=True):
    previous = current_command(db)
    if previous is not None:
        if mode == "preview" and previous.mode != "preview":
            raise RuntimeError("A preview must own its rollback boundary")
        try:
            yield previous
        except BaseException:
            previous.failed = True
            raise
        return
    state = CommandState(mode=mode)
    db.info["command"] = state
    try:
        yield state
        if state.failed:
            raise RuntimeError("A failed nested command cannot commit")
        await db.flush()
        if db.info.get("delivery_changed_nodes") or db.info.get("delivery_graph_changed") or db.info.get("delivery_scope_changed"):
            from app.services.delivery_dependency_service import DeliveryDependencyService
            await DeliveryDependencyService(db).reconcile()
        for task_id, version, kind in sorted(db.info.pop("discussion_events", set())):
            from app.services.discussion_service import DiscussionService
            await DiscussionService(db).enqueue(task_id, kind, f"task:{task_id}:{version}:{kind}")
        if mode == "preview":
            await db.rollback()
        elif commit:
            await db.commit()
        else:
            await db.flush()
    except BaseException:
        await db.rollback()
        raise
    finally:
        db.info.pop("command", None)
        db.info.pop("time_entry_commands", None)
        for key in ["request_expected_revisions", "command_triage_projects", "review_rework_tasks", "domain_queue_actors", "command_task_projects", "derived_rollups", "authority_audited", "authority_audit_pending", "delivery_changed_nodes", "delivery_graph_changed", "delivery_reconciling", "delivery_scope_changed", "discussion_events"]:
            db.info.pop(key, None)


def atomic_command(function):
    """Give standalone service commands an owner without committing inside another command."""
    @wraps(function)
    async def wrapped(self, *args, **kwargs):
        preview = kwargs.get("dry_run", False) or bool(args and getattr(args[0], "dry_run", False))
        async with command_transaction(self.db, mode="preview" if preview else "apply", commit=kwargs.get("commit", True)):
            return await function(self, *args, **kwargs)
    return wrapped


def preview_command(function):
    """Give a calculation a rollback boundary in every transport and direct invocation."""
    @wraps(function)
    async def wrapped(self, *args, **kwargs):
        async with command_transaction(self.db, mode="preview"):
            return await function(self, *args, **kwargs)
    return wrapped


async def lock_backlog_project(db, project_id):
    """Serialize unscheduled hierarchy writes without manufacturing an iteration."""
    from app.authority import internal_authority, require_project
    from app.models.project import Project
    require_project(db, project_id, "read")
    await lock_planning(db)
    state = current_command(db)
    if state is None:
        raise RuntimeError("Backlog reservations require a command transaction")
    if project_id in state.backlog_projects:
        return
    exists = await db.scalar(select(Project.id).where(Project.id == project_id).with_for_update())
    if exists is None:
        raise ValueError("Project not found or inaccessible")
    # SQLite needs an actual writer reservation; the predicate was authorized
    # above, and this no-op never changes project content or grants.
    with internal_authority(db):
        await db.execute(update(Project).where(Project.id == project_id).values(id=Project.id, updated_at=Project.updated_at).execution_options(synchronize_session=False))
    state.backlog_projects.add(project_id)


async def lock_iterations(db: AsyncSession, iteration_ids, *, expected=None, require_expected=False, revision_field="expected_revisions") -> dict[int, int]:
    """Acquire aggregate locks in ascending ID order, then task locks in ascending ID order."""
    from app.models.iteration import Iteration
    from app.runtime_telemetry import metrics

    await lock_planning(db)

    state = current_command(db)
    if state is None:
        raise RuntimeError("Iteration reservations require a command transaction")
    expected = dict(expected or {})
    request_expected = db.info.get("request_expected_revisions", {})
    if any(key in expected and expected[key] != value for key, value in request_expected.items()):
        raise PlanningConflict("conflicting_revision_context", "Body and header revisions disagree. Send one observed revision for each iteration.")
    expected = {**request_expected, **expected}
    for iteration_id in sorted({item for item in iteration_ids if item is not None}):
        if require_expected and iteration_id not in state.versioned_iterations:
            from app.mutation_versions import require_mutation_revision
            require_mutation_revision(db, expected.get(iteration_id), field=revision_field, resource="iteration", resource_id=iteration_id)
        if iteration_id in state.iterations:
            if iteration_id in expected and expected[iteration_id] != state.iterations[iteration_id]:
                raise AggregateVersionConflict(iteration_id, expected[iteration_id], state.iterations[iteration_id])
            if iteration_id in expected:
                state.versioned_iterations.add(iteration_id)
            continue
        current = await db.scalar(select(Iteration.revision).where(Iteration.id == iteration_id).with_for_update())
        if current is None:
            raise ValueError("Iteration not found or inaccessible")
        authority = db.info.get("authority")
        if authority is not None and not authority.operator and not authority.local and not db.info.get("authority_internal"):
            from app.models.task import Task
            from app.authority import AuthorityError, internal_authority
            with internal_authority(db):
                scopes = (await db.scalars(select(Task.project_id).where(Task.iteration_id == iteration_id).distinct())).all()
            if any(not authority.allows(scope, "read") for scope in scopes):
                raise AuthorityError("incomplete_authorized_graph", "This command requires access to all of its scheduling inputs.")
        wanted = expected.get(iteration_id, current)
        if wanted != current:
            raise AggregateVersionConflict(iteration_id, wanted, current)
        reserved = await db.execute(update(Iteration).where(Iteration.id == iteration_id, Iteration.revision == current)
                                    .values(revision=current + 1).execution_options(synchronize_session=False))
        if reserved.rowcount != 1:
            fresh = await db.scalar(select(Iteration.revision).where(Iteration.id == iteration_id))
            raise AggregateVersionConflict(iteration_id, wanted, fresh or current)
        from sqlalchemy.orm.attributes import set_committed_value
        loaded = db.identity_map.get((Iteration, (iteration_id,), None))
        if loaded is not None:
            set_committed_value(loaded, "revision", current + 1)
        state.iterations[iteration_id] = current
        if iteration_id in expected:
            state.versioned_iterations.add(iteration_id)
        if iteration_id not in expected and state.mode == "apply":
            metrics.increment("workchord_legacy_aggregate_commands_total")
    return dict(state.iterations)


def schedule_input_command(kind):
    """Capture and revise every affected iteration before editing shared planning inputs."""
    import inspect as python_inspect

    def decorate(function):
        signature = python_inspect.signature(function)
        @wraps(function)
        async def wrapped(self, *args, **kwargs):
            from app.models.iteration import Iteration
            from app.models.team_member import TeamMember, Vacation
            from app.models.task import Task
            from app.services.snapshot_service import SnapshotService
            from app.services.task_service import TaskService

            values = signature.bind(self, *args, **kwargs).arguments
            async with command_transaction(self.db, commit=kwargs.get("commit", True)):
                await lock_planning(self.db)
                ids = []
                if kind == "calendar":
                    ids = list((await self.db.scalars(select(Iteration.id).where(Iteration.calendar_id == values["calendar_id"])) ).all())
                    from app.models.capacity import ProfileAvailability
                    ids.extend((await self.db.scalars(select(TeamMember.iteration_id).join(
                        ProfileAvailability, ProfileAvailability.profile_id == TeamMember.profile_id).where(
                        ProfileAvailability.calendar_id == values["calendar_id"], TeamMember.iteration_id.is_not(None)))).all())
                elif kind == "project":
                    direct = select(Iteration.id).where(Iteration.project_id == values["project_id"])
                    linked = select(Task.iteration_id).where(Task.project_id == values["project_id"])
                    ids = [item for item in (await self.db.scalars(direct.union(linked))).all() if item is not None]
                elif kind == "iteration":
                    ids = [values["iteration_id"]]
                elif kind == "profile":
                    ids = list((await self.db.scalars(select(TeamMember.iteration_id).where(TeamMember.profile_id == values["profile_id"], TeamMember.iteration_id.is_not(None)).distinct())).all())
                else:
                    member_id = values.get("member_id")
                    if "vacation_id" in values:
                        member_id = await self.db.scalar(select(Vacation.team_member_id).where(Vacation.id == values["vacation_id"]))
                    if member_id is not None:
                        member = await self.db.get(TeamMember, member_id)
                        if member is not None and member.iteration_id is not None:
                            ids = [member.iteration_id]
                    elif values.get("iteration_id") is not None:
                        ids = [values["iteration_id"]]
                if ids:
                    data = values.get("data")
                    await lock_iterations(self.db, ids, expected=values.get("expected_revisions", getattr(data, "expected_revisions", None)), require_expected=True)
                    for iteration_id in sorted(set(ids)):
                        await SnapshotService(self.db).create_snapshot(iteration_id, "before_planning_input_change")
                    tasks = list((await self.db.scalars(select(Task).where(Task.iteration_id.in_(ids), Task.status != "closed").order_by(Task.id))).all())
                    service = TaskService(self.db)
                    for task in tasks:
                        await service.reserve_task_version(task, task.version)
                return await function(self, *args, **kwargs)
        return wrapped
    return decorate
