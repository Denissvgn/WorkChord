"""Safe PM setup commands for authenticated agent actors.

The adapter delegates validation and mutation behavior to the existing domain
services, then stores an exact actor-attributed receipt in the same transaction.
"""

import hashlib
import json
import secrets
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import AgentActor, AgentIdempotencyRecord
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.task import Task, TaskDependency
from app.models.team_member import TeamMember, Vacation
from app.schemas.agent import AgentTaskCreate, AgentTaskPatch
from app.schemas.agent_planning import (
    AgentPlanningCommandContext,
    AgentPlanningReceipt,
    AgentScheduleCommand,
    AgentScheduleResult,
    AgentScheduleTaskState,
)
from app.schemas.iteration import IterationCreate, IterationUpdate
from app.schemas.project import (
    ProjectCreate,
    ProjectMilestoneCreateRequest,
    ProjectMilestoneResponse,
    ProjectMilestoneUpdate,
    ProjectResponse,
    ProjectUpdate,
)
from app.schemas.team import (
    TeamMemberCreate,
    TeamMemberProfileCreate,
    TeamMemberProfileResponse,
    TeamMemberProfileUpdate,
    TeamMemberResponse,
    TeamMemberUpdate,
    VacationCreate,
    VacationResponse,
    VacationUpdate,
)
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.agent_service import (
    AgentConflictError,
    require_scope,
    validate_idempotency_key,
)
from app.services.agent_profile_catalog_service import AgentProfileCatalogService
from app.services.iteration_service import IterationService
from app.services.project_service import ProjectService
from app.services.scheduler_service import SchedulerService
from app.services.task_service import TaskService
from app.services.team_service import TeamService


MutationResult = tuple[int, dict[str, Any]]
Mutation = Callable[[], Awaitable[MutationResult]]


class _SchedulePreviewComplete(Exception):
    """Internal signal used to roll back a schedule preview savepoint."""

    def __init__(self, result: dict[str, Any]):
        self.result = result
        super().__init__("schedule preview complete")


class AgentPlanningService:
    """Expose bounded PM setup commands without bypassing domain services."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.projects = ProjectService(db)
        self.iterations = IterationService(db)
        self.team = TeamService(db)
        self.scheduler = SchedulerService(db)
        self.tasks = TaskService(db)
        self.profile_catalog = AgentProfileCatalogService(db)

    @staticmethod
    def _request_hash(payload: dict[str, Any]) -> str:
        canonical = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    async def _replay(
        self,
        *,
        actor: AgentActor,
        operation: str,
        target_type: str,
        idempotency_target_id: int,
        idempotency_key: str,
        request_payload: dict[str, Any],
    ) -> AgentPlanningReceipt | None:
        result = await self.db.execute(
            select(AgentIdempotencyRecord).where(
                AgentIdempotencyRecord.actor_id == actor.id,
                AgentIdempotencyRecord.operation == operation,
                AgentIdempotencyRecord.target_type == target_type,
                AgentIdempotencyRecord.target_id == idempotency_target_id,
                AgentIdempotencyRecord.idempotency_key == idempotency_key,
            )
        )
        record = result.scalar_one_or_none()
        if record is None:
            return None
        request_hash = self._request_hash(request_payload)
        if not secrets.compare_digest(record.request_hash, request_hash):
            raise AgentConflictError("idempotency_mismatch")
        try:
            payload = json.loads(record.response_payload)
            return AgentPlanningReceipt.model_validate(payload["response"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise AgentConflictError(
                "Idempotent PM setup receipt is invalid"
            ) from exc

    async def _execute(
        self,
        *,
        actor: AgentActor,
        scope: str,
        operation: str,
        target_type: str,
        idempotency_target_id: int,
        command: AgentPlanningCommandContext,
        request_payload: dict[str, Any],
        mutate: Mutation,
    ) -> AgentPlanningReceipt:
        require_scope(actor, scope)
        validated_key = validate_idempotency_key(
            command.idempotency_key,
            required=True,
        )
        assert validated_key is not None
        audited_request = {
            "command": {
                "rationale": command.rationale,
                "correlation_id": command.correlation_id,
            },
            "payload": request_payload,
        }

        replay = await self._replay(
            actor=actor,
            operation=operation,
            target_type=target_type,
            idempotency_target_id=idempotency_target_id,
            idempotency_key=validated_key,
            request_payload=audited_request,
        )
        if replay is not None:
            return replay

        try:
            actual_target_id, result = await mutate()
            receipt = AgentPlanningReceipt(
                operation=operation,
                actor_id=actor.id,
                target_type=target_type,
                target_id=actual_target_id,
                idempotency_key=validated_key,
                rationale=command.rationale,
                correlation_id=command.correlation_id,
                result=result,
            )
            self.db.add(
                AgentIdempotencyRecord(
                    actor_id=actor.id,
                    operation=operation,
                    target_type=target_type,
                    target_id=idempotency_target_id,
                    idempotency_key=validated_key,
                    request_hash=self._request_hash(audited_request),
                    response_payload=json.dumps(
                        {"response": receipt.model_dump(mode="json")},
                        sort_keys=True,
                    ),
                )
            )
            await self.db.commit()
            return receipt
        except IntegrityError:
            await self.db.rollback()
            replay = await self._replay(
                actor=actor,
                operation=operation,
                target_type=target_type,
                idempotency_target_id=idempotency_target_id,
                idempotency_key=validated_key,
                request_payload=audited_request,
            )
            if replay is None:
                raise
            return replay
        except AgentConflictError:
            # A same-key concurrent command can lose the initial replay race,
            # block on domain locks, then observe the winner's state change.
            # Recheck the durable exact receipt before surfacing that conflict.
            await self.db.rollback()
            replay = await self._replay(
                actor=actor,
                operation=operation,
                target_type=target_type,
                idempotency_target_id=idempotency_target_id,
                idempotency_key=validated_key,
                request_payload=audited_request,
            )
            if replay is not None:
                return replay
            raise
        except Exception:
            await self.db.rollback()
            replay = await self._replay(
                actor=actor,
                operation=operation,
                target_type=target_type,
                idempotency_target_id=idempotency_target_id,
                idempotency_key=validated_key,
                request_payload=audited_request,
            )
            if replay is not None:
                return replay
            raise

    async def create_project(
        self,
        actor: AgentActor,
        data: ProjectCreate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = data.model_dump(mode="json")

        async def mutate() -> MutationResult:
            project = await self.projects.create(data, commit=False)
            result = ProjectResponse.model_validate(project).model_dump(mode="json")
            return project.id, result

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.project.create",
            target_type="project",
            idempotency_target_id=0,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def update_project(
        self,
        project_id: int,
        actor: AgentActor,
        data: ProjectUpdate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = data.model_dump(mode="json", exclude_unset=True)

        async def mutate() -> MutationResult:
            project = await self.projects.update(project_id, data, commit=False)
            if project is None:
                raise LookupError(f"Project with id {project_id} not found")
            result = ProjectResponse.model_validate(project).model_dump(mode="json")
            return project.id, result

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.project.update",
            target_type="project",
            idempotency_target_id=project_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def create_milestone(
        self,
        project_id: int,
        actor: AgentActor,
        data: ProjectMilestoneCreateRequest,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        """Create one project milestone with an exact planning receipt."""
        payload = {
            "project_id": project_id,
            "data": data.model_dump(mode="json"),
        }

        async def mutate() -> MutationResult:
            milestone = await self.projects.create_milestone(
                project_id,
                data,
                commit=False,
            )
            if milestone is None:
                raise LookupError(f"Project with id {project_id} not found")
            result = ProjectMilestoneResponse.model_validate(milestone).model_dump(
                mode="json"
            )
            return milestone.id, result

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.milestone.create",
            target_type="project_milestone",
            idempotency_target_id=project_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def update_milestone(
        self,
        project_id: int,
        milestone_id: int,
        actor: AgentActor,
        data: ProjectMilestoneUpdate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        """Update one project-scoped milestone with exact replay semantics."""
        payload = {
            "project_id": project_id,
            "milestone_id": milestone_id,
            "data": data.model_dump(mode="json", exclude_unset=True),
        }

        async def mutate() -> MutationResult:
            milestone = await self.projects.update_milestone(
                project_id,
                milestone_id,
                data,
                commit=False,
            )
            if milestone is None:
                raise LookupError(
                    f"Milestone with id {milestone_id} not found in project {project_id}"
                )
            result = ProjectMilestoneResponse.model_validate(milestone).model_dump(
                mode="json"
            )
            return milestone.id, result

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.milestone.update",
            target_type="project_milestone",
            idempotency_target_id=milestone_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def delete_milestone(
        self,
        project_id: int,
        milestone_id: int,
        actor: AgentActor,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        """Delete one project-scoped milestone and preserve its exact result."""
        payload = {
            "project_id": project_id,
            "milestone_id": milestone_id,
        }

        async def mutate() -> MutationResult:
            detached_task_count = await self.projects.delete_milestone(
                project_id,
                milestone_id,
                commit=False,
            )
            if detached_task_count is None:
                raise LookupError(
                    f"Milestone with id {milestone_id} not found in project {project_id}"
                )
            return milestone_id, {
                "success": True,
                "project_id": project_id,
                "milestone_id": milestone_id,
                "detached_task_count": detached_task_count,
            }

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.milestone.delete",
            target_type="project_milestone",
            idempotency_target_id=milestone_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def create_task(
        self,
        iteration_id: int,
        actor: AgentActor,
        data: AgentTaskCreate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        """Create one decomposed task with a complete planning audit context."""
        payload = {
            "iteration_id": iteration_id,
            "data": data.model_dump(mode="json"),
        }

        async def mutate() -> MutationResult:
            task = await self.tasks.create(
                iteration_id,
                TaskCreate.model_validate(data.model_dump()),
                actor_type="agent",
                actor_id=actor.id,
                correlation_id=command.correlation_id,
                idempotency_key=command.idempotency_key,
                commit=False,
            )
            await self.tasks.record_task_event(
                task.id,
                "agent_planning_task_created",
                {
                    "operation": "planning.task.create",
                    "rationale": command.rationale,
                },
                actor_type="agent",
                actor_id=actor.id,
                correlation_id=command.correlation_id,
                idempotency_key=command.idempotency_key,
            )
            loaded = await self.tasks.get_by_id(task.id)
            response = self.tasks.task_to_response(loaded or task)
            return task.id, TaskResponse.model_validate(response).model_dump(mode="json")

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.task.create",
            target_type="task",
            idempotency_target_id=iteration_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def patch_task(
        self,
        task_id: int,
        actor: AgentActor,
        data: AgentTaskPatch,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        """Patch decomposition fields under optimistic version and exact replay."""
        unsupported = data.model_fields_set.intersection(
            {"claim_id", "claim_generation", "status"}
        )
        if unsupported:
            raise ValueError(
                "Planning task patch cannot mutate lifecycle or claim fields: "
                + ", ".join(sorted(unsupported))
            )
        payload = {
            "task_id": task_id,
            "data": data.model_dump(mode="json", exclude_unset=True),
        }

        async def mutate() -> MutationResult:
            task_update = TaskUpdate.model_validate(
                data.model_dump(
                    exclude_unset=True,
                    exclude={"claim_id", "claim_generation"},
                )
            )
            task = await self.tasks.update(
                task_id,
                task_update,
                actor_type="agent",
                actor_id=actor.id,
                correlation_id=command.correlation_id,
                idempotency_key=command.idempotency_key,
                commit=False,
            )
            if task is None:
                raise LookupError(f"Task with id {task_id} not found")
            await self.tasks.record_task_event(
                task.id,
                "agent_planning_task_patched",
                {
                    "operation": "planning.task.patch",
                    "rationale": command.rationale,
                    "version": task.version,
                },
                actor_type="agent",
                actor_id=actor.id,
                correlation_id=command.correlation_id,
                idempotency_key=command.idempotency_key,
            )
            response = self.tasks.task_to_response(task)
            return task.id, TaskResponse.model_validate(response).model_dump(mode="json")

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.task.patch",
            target_type="task",
            idempotency_target_id=task_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def create_iteration(
        self,
        actor: AgentActor,
        data: IterationCreate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = data.model_dump(mode="json")

        async def mutate() -> MutationResult:
            iteration = await self.iterations.create(data, commit=False)
            result = self.iterations.to_response(iteration).model_dump(mode="json")
            return iteration.id, result

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.iteration.create",
            target_type="iteration",
            idempotency_target_id=0,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def update_iteration(
        self,
        iteration_id: int,
        actor: AgentActor,
        data: IterationUpdate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = data.model_dump(mode="json", exclude_unset=True)

        async def mutate() -> MutationResult:
            iteration = await self.iterations.update(
                iteration_id,
                data,
                commit=False,
            )
            if iteration is None:
                raise LookupError(f"Iteration with id {iteration_id} not found")
            result = self.iterations.to_response(iteration).model_dump(mode="json")
            return iteration.id, result

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.iteration.update",
            target_type="iteration",
            idempotency_target_id=iteration_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def create_profile(
        self,
        actor: AgentActor,
        data: TeamMemberProfileCreate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = data.model_dump(mode="json")

        async def mutate() -> MutationResult:
            if data.seed_key is not None:
                raise ValueError(
                    "seed_key is reserved for server-owned profile presets"
                )
            profile = await self.team.create_profile(data, commit=False)
            result = TeamMemberProfileResponse.model_validate(profile).model_dump(
                mode="json"
            )
            return profile.id, result

        return await self._execute(
            actor=actor,
            scope="team:write",
            operation="planning.profile.create",
            target_type="team_member_profile",
            idempotency_target_id=0,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def update_profile(
        self,
        profile_id: int,
        actor: AgentActor,
        data: TeamMemberProfileUpdate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = data.model_dump(mode="json", exclude_unset=True)

        async def mutate() -> MutationResult:
            profile = await self.team.update_profile(profile_id, data, commit=False)
            if profile is None:
                raise LookupError(
                    f"Team member profile with id {profile_id} not found"
                )
            result = TeamMemberProfileResponse.model_validate(profile).model_dump(
                mode="json"
            )
            return profile.id, result

        return await self._execute(
            actor=actor,
            scope="team:write",
            operation="planning.profile.update",
            target_type="team_member_profile",
            idempotency_target_id=profile_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def apply_profile_preset(
        self,
        preset_key: str,
        actor: AgentActor,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = {"preset_key": preset_key}

        async def mutate() -> MutationResult:
            try:
                profile = await self.profile_catalog.apply_preset(
                    preset_key,
                    commit=False,
                )
            except ValueError as exc:
                if str(exc) == "Unknown agent profile preset":
                    raise LookupError(str(exc)) from exc
                raise
            result = TeamMemberProfileResponse.model_validate(profile).model_dump(
                mode="json"
            )
            return profile.id, result

        return await self._execute(
            actor=actor,
            scope="team:write",
            operation="planning.profile_preset.apply",
            target_type="team_member_profile",
            idempotency_target_id=0,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def create_team_member(
        self,
        iteration_id: int,
        actor: AgentActor,
        data: TeamMemberCreate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = {
            "iteration_id": iteration_id,
            "data": data.model_dump(mode="json"),
        }

        async def mutate() -> MutationResult:
            if await self.iterations.get_by_id(iteration_id) is None:
                raise LookupError(f"Iteration with id {iteration_id} not found")
            member = await self.team.create(iteration_id, data, commit=False)
            loaded = await self.team.get_by_id(member.id)
            if loaded is None:
                raise RuntimeError("Created team member could not be reloaded")
            result = TeamMemberResponse.model_validate(loaded).model_dump(mode="json")
            return member.id, result

        return await self._execute(
            actor=actor,
            scope="team:write",
            operation="planning.team_member.create",
            target_type="team_member",
            idempotency_target_id=iteration_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def update_team_member(
        self,
        member_id: int,
        actor: AgentActor,
        data: TeamMemberUpdate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = data.model_dump(mode="json", exclude_unset=True)

        async def mutate() -> MutationResult:
            member = await self.team.update(member_id, data, commit=False)
            if member is None:
                raise LookupError(f"Team member with id {member_id} not found")
            loaded = await self.team.get_by_id(member.id)
            if loaded is None:
                raise RuntimeError("Updated team member could not be reloaded")
            result = TeamMemberResponse.model_validate(loaded).model_dump(mode="json")
            return member.id, result

        return await self._execute(
            actor=actor,
            scope="team:write",
            operation="planning.team_member.update",
            target_type="team_member",
            idempotency_target_id=member_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def create_vacation(
        self,
        member_id: int,
        actor: AgentActor,
        data: VacationCreate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = {"member_id": member_id, "data": data.model_dump(mode="json")}

        async def mutate() -> MutationResult:
            vacation = await self.team.add_vacation(member_id, data, commit=False)
            if vacation is None:
                raise LookupError(f"Team member with id {member_id} not found")
            result = VacationResponse.model_validate(vacation).model_dump(mode="json")
            return vacation.id, result

        return await self._execute(
            actor=actor,
            scope="team:write",
            operation="planning.vacation.create",
            target_type="vacation",
            idempotency_target_id=member_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def update_vacation(
        self,
        vacation_id: int,
        actor: AgentActor,
        data: VacationUpdate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = data.model_dump(mode="json", exclude_unset=True)

        async def mutate() -> MutationResult:
            vacation = await self.team.update_vacation(
                vacation_id,
                data,
                commit=False,
            )
            if vacation is None:
                raise LookupError(f"Vacation with id {vacation_id} not found")
            result = VacationResponse.model_validate(vacation).model_dump(mode="json")
            return vacation.id, result

        return await self._execute(
            actor=actor,
            scope="team:write",
            operation="planning.vacation.update",
            target_type="vacation",
            idempotency_target_id=vacation_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def _iteration_tasks_for_update(self, iteration_id: int) -> list[Task]:
        result = await self.db.execute(
            select(Task)
            .where(Task.iteration_id == iteration_id)
            .order_by(Task.id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return list(result.scalars().unique().all())

    async def _require_iteration_for_update(self, iteration_id: int) -> Iteration:
        """Lock the schedule aggregate root for preview/apply serialization."""
        result = await self.db.execute(
            select(Iteration)
            .where(Iteration.id == iteration_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        iteration = result.scalar_one_or_none()
        if iteration is None:
            raise LookupError(f"Iteration with id {iteration_id} not found")
        return iteration

    async def _lock_schedule_task_set(self, iteration_id: int) -> None:
        """Lock only the mutable rows in one scheduling aggregate.

        The aggregate-root ``FOR UPDATE`` lock also fences new tasks and team
        members because their foreign-key checks need a conflicting key-share
        lock. Existing child rows are locked explicitly so updates and deletes
        cannot change the snapshot. A shared calendar lock prevents calendar
        edits while still allowing unrelated iterations that use the same
        calendar to schedule concurrently.
        """
        dialect = self.db.get_bind().dialect.name
        if dialect == "postgresql":
            iteration = await self._require_iteration_for_update(iteration_id)
            calendar_result = await self.db.execute(
                select(Calendar.id)
                .where(Calendar.id == iteration.calendar_id)
                .with_for_update(read=True)
            )
            if calendar_result.scalar_one_or_none() is None:
                raise AgentConflictError(
                    "Iteration scheduling calendar is unavailable"
                )

            task_result = await self.db.execute(
                select(Task.id)
                .where(Task.iteration_id == iteration_id)
                .order_by(Task.id)
                .with_for_update()
            )
            task_ids = list(task_result.scalars().all())
            await self.db.execute(
                select(TaskDependency.id)
                .where(TaskDependency.task_id.in_(task_ids or [-1]))
                .order_by(
                    TaskDependency.task_id,
                    TaskDependency.depends_on_id,
                    TaskDependency.id,
                )
                .with_for_update()
            )

            member_result = await self.db.execute(
                select(TeamMember.id)
                .where(TeamMember.iteration_id == iteration_id)
                .order_by(TeamMember.id)
                .with_for_update()
            )
            member_ids = list(member_result.scalars().all())
            await self.db.execute(
                select(Vacation.id)
                .where(Vacation.team_member_id.in_(member_ids or [-1]))
                .order_by(
                    Vacation.team_member_id,
                    Vacation.start_date,
                    Vacation.end_date,
                    Vacation.id,
                )
                .with_for_update()
            )
            return
        if dialect == "sqlite":
            # SQLite ignores SELECT FOR UPDATE. A harmless write acquires its
            # database write lock before the task-set snapshot is read.
            await self.db.execute(
                text("UPDATE iterations SET name = name WHERE id = :iteration_id"),
                {"iteration_id": iteration_id},
            )
            return
        raise AgentConflictError(
            f"Atomic schedule apply is unsupported for database dialect {dialect}"
        )

    @staticmethod
    def _schedule_task_states(tasks: list[Task]) -> list[AgentScheduleTaskState]:
        return [
            AgentScheduleTaskState(
                task_id=task.id,
                version=task.version,
                start_date=task.start_date,
                end_date=task.end_date,
                calculated_effort_days=task.calculated_effort_days,
            )
            for task in sorted(tasks, key=lambda item: item.id)
        ]

    @staticmethod
    def _canonical_digest(payload: dict[str, Any]) -> str:
        """Return a deterministic SHA-256 digest for one JSON-safe payload."""
        return hashlib.sha256(
            json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()

    def _scheduling_rules_digest(self) -> str:
        """Return the digest of the rules currently used by the scheduler."""
        return self._canonical_digest(
            self.scheduler.rules_service.get_rules_as_dict()
        )

    async def _schedule_input_digest(
        self,
        iteration_id: int,
        *,
        schedule_output_overrides: Mapping[
            int, tuple[Any, Any, Any]
        ] | None = None,
    ) -> tuple[str, str]:
        """Hash every mutable input consumed by ``SchedulerService``."""
        iteration = await self._require_iteration_for_update(iteration_id)
        calendar_result = await self.db.execute(
            select(Calendar)
            .where(Calendar.id == iteration.calendar_id)
            .execution_options(populate_existing=True)
        )
        calendar = calendar_result.scalar_one_or_none()
        if calendar is None:
            raise AgentConflictError("Iteration scheduling calendar is unavailable")

        task_result = await self.db.execute(
            select(Task)
            .where(Task.iteration_id == iteration_id)
            .order_by(Task.id)
            .execution_options(populate_existing=True)
        )
        tasks = list(task_result.scalars().unique().all())
        task_ids = [task.id for task in tasks]

        dependency_result = await self.db.execute(
            select(TaskDependency)
            .where(TaskDependency.task_id.in_(task_ids or [-1]))
            .order_by(
                TaskDependency.task_id,
                TaskDependency.depends_on_id,
                TaskDependency.id,
            )
        )
        dependencies = list(dependency_result.scalars().all())

        member_result = await self.db.execute(
            select(TeamMember)
            .where(TeamMember.iteration_id == iteration_id)
            .order_by(TeamMember.id)
            .execution_options(populate_existing=True)
        )
        members = list(member_result.scalars().unique().all())
        member_ids = [member.id for member in members]
        vacation_result = await self.db.execute(
            select(Vacation)
            .where(Vacation.team_member_id.in_(member_ids or [-1]))
            .order_by(
                Vacation.team_member_id,
                Vacation.start_date,
                Vacation.end_date,
                Vacation.id,
            )
        )
        vacations = list(vacation_result.scalars().all())

        rules = self.scheduler.rules_service.get_rules_as_dict()
        snapshot = {
            "schema": "workchord-schedule-input/v1",
            "iteration": {
                "id": iteration.id,
                "calendar_id": iteration.calendar_id,
                "start_date": iteration.start_date.isoformat(),
                "end_date": iteration.end_date.isoformat(),
            },
            "calendar": {
                "id": calendar.id,
                "name": calendar.name,
                "year": calendar.year,
                "holidays": sorted(calendar.holidays or []),
                "weekend_days": sorted(calendar.weekend_days or []),
                "short_days": sorted(calendar.short_days or []),
            },
            "members": [
                {
                    "id": member.id,
                    "name": member.name,
                    "availability_percent": member.availability_percent,
                    "professionalism_coefficient": (
                        member.professionalism_coefficient
                    ),
                    "operational_utilization": member.operational_utilization,
                }
                for member in members
            ],
            "vacations": [
                {
                    "id": vacation.id,
                    "team_member_id": vacation.team_member_id,
                    "start_date": vacation.start_date.isoformat(),
                    "end_date": vacation.end_date.isoformat(),
                }
                for vacation in vacations
            ],
            "tasks": [
                {
                    "id": task.id,
                    "version": task.version,
                    "title": task.title,
                    "parent_id": task.parent_id,
                    "assignee_id": task.assignee_id,
                    "priority": task.priority,
                    "effort_days": task.effort_days,
                    "status": task.status,
                    "start_date": (
                        (
                            schedule_output_overrides[task.id][0].isoformat()
                            if schedule_output_overrides
                            and task.id in schedule_output_overrides
                            and schedule_output_overrides[task.id][0]
                            else None
                        )
                        if schedule_output_overrides
                        and task.id in schedule_output_overrides
                        else (
                            task.start_date.isoformat() if task.start_date else None
                        )
                    ),
                    "end_date": (
                        (
                            schedule_output_overrides[task.id][1].isoformat()
                            if schedule_output_overrides
                            and task.id in schedule_output_overrides
                            and schedule_output_overrides[task.id][1]
                            else None
                        )
                        if schedule_output_overrides
                        and task.id in schedule_output_overrides
                        else task.end_date.isoformat() if task.end_date else None
                    ),
                    "calculated_effort_days": (
                        schedule_output_overrides[task.id][2]
                        if schedule_output_overrides
                        and task.id in schedule_output_overrides
                        else task.calculated_effort_days
                    ),
                    "min_start_date": (
                        task.min_start_date.isoformat()
                        if task.min_start_date
                        else None
                    ),
                    "max_end_date": (
                        task.max_end_date.isoformat() if task.max_end_date else None
                    ),
                    "is_optional": task.is_optional,
                    "is_deferred": task.is_deferred,
                    "sort_order": task.sort_order,
                }
                for task in tasks
            ],
            "dependencies": [
                {
                    "task_id": dependency.task_id,
                    "depends_on_id": dependency.depends_on_id,
                }
                for dependency in dependencies
            ],
            "rules": rules,
        }
        return self._canonical_digest(snapshot), self._canonical_digest(rules)

    @staticmethod
    def _schedule_result_payload(
        schedule: Any,
        tasks: list[Task],
        input_digest: str,
    ) -> dict[str, Any]:
        return AgentScheduleResult(
            success=schedule.success,
            decisions=[item.model_dump(mode="json") for item in schedule.decisions],
            workload_balanced=schedule.workload_balanced,
            workload_issues=[
                item.model_dump(mode="json") for item in schedule.workload_issues
            ],
            input_digest=input_digest,
            task_states=AgentPlanningService._schedule_task_states(tasks),
        ).model_dump(mode="json")

    async def preview_schedule(
        self,
        iteration_id: int,
        actor: AgentActor,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = {"iteration_id": iteration_id}

        async def mutate() -> MutationResult:
            await self._require_iteration_for_update(iteration_id)
            try:
                async with self.db.begin_nested():
                    await self._lock_schedule_task_set(iteration_id)
                    await self._iteration_tasks_for_update(iteration_id)
                    input_digest, _rules_digest = await self._schedule_input_digest(
                        iteration_id
                    )
                    schedule = await self.scheduler.schedule_iteration(
                        iteration_id,
                        commit=False,
                    )
                    tasks = await self._iteration_tasks_for_update(iteration_id)
                    result = self._schedule_result_payload(
                        schedule,
                        tasks,
                        input_digest,
                    )
                    raise _SchedulePreviewComplete(result)
            except _SchedulePreviewComplete as complete:
                return iteration_id, complete.result
            raise RuntimeError("Schedule preview transaction did not complete")

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.schedule.preview",
            target_type="iteration",
            idempotency_target_id=iteration_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )

    async def apply_schedule(
        self,
        iteration_id: int,
        actor: AgentActor,
        data: AgentScheduleCommand,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentPlanningReceipt:
        payload = {
            "iteration_id": iteration_id,
            "data": data.model_dump(mode="json"),
        }

        async def mutate() -> MutationResult:
            await self._require_iteration_for_update(iteration_id)
            await self._lock_schedule_task_set(iteration_id)
            tasks = await self._iteration_tasks_for_update(iteration_id)
            current_versions = {task.id: task.version for task in tasks}
            if data.expected_task_versions != current_versions:
                raise AgentConflictError(
                    "Schedule task versions changed; run a new preview before apply"
                )
            current_digest, rules_digest = await self._schedule_input_digest(
                iteration_id
            )
            if not secrets.compare_digest(
                data.expected_input_digest,
                current_digest,
            ):
                raise AgentConflictError(
                    "Schedule inputs changed; run a new preview before apply"
                )
            before = {
                task.id: (
                    task.start_date,
                    task.end_date,
                    task.calculated_effort_days,
                    task.version,
                )
                for task in tasks
            }
            schedule = await self.scheduler.schedule_iteration(
                iteration_id,
                commit=False,
            )
            if not secrets.compare_digest(
                rules_digest,
                self._scheduling_rules_digest(),
            ):
                raise AgentConflictError(
                    "Scheduling rules changed during apply; run a new preview"
                )
            tasks = await self._iteration_tasks_for_update(iteration_id)
            if {task.id for task in tasks} != set(before):
                raise AgentConflictError(
                    "Iteration task set changed during schedule apply; run a new preview"
                )
            post_schedule_digest, post_rules_digest = (
                await self._schedule_input_digest(
                    iteration_id,
                    schedule_output_overrides={
                        task_id: values[:3]
                        for task_id, values in before.items()
                    },
                )
            )
            if not secrets.compare_digest(current_digest, post_schedule_digest):
                raise AgentConflictError(
                    "Schedule inputs changed during apply; run a new preview"
                )
            if not secrets.compare_digest(rules_digest, post_rules_digest):
                raise AgentConflictError(
                    "Scheduling rules changed during apply; run a new preview"
                )
            for task in tasks:
                previous = before[task.id]
                changed = (
                    task.start_date,
                    task.end_date,
                    task.calculated_effort_days,
                ) != previous[:3]
                if not changed:
                    continue
                await self.tasks.reserve_task_version(task, previous[3])
                await self.tasks.record_task_event(
                    task.id,
                    "task_schedule_applied",
                    {
                        "changes": {
                            "start_date": {
                                "old": previous[0].isoformat() if previous[0] else None,
                                "new": task.start_date.isoformat() if task.start_date else None,
                            },
                            "end_date": {
                                "old": previous[1].isoformat() if previous[1] else None,
                                "new": task.end_date.isoformat() if task.end_date else None,
                            },
                            "calculated_effort_days": {
                                "old": previous[2],
                                "new": task.calculated_effort_days,
                            },
                        },
                        "version": task.version,
                        "iteration_id": iteration_id,
                    },
                    actor_type="agent",
                    actor_id=actor.id,
                    correlation_id=command.correlation_id,
                    idempotency_key=command.idempotency_key,
                )
            await self.db.flush()
            result = self._schedule_result_payload(
                schedule,
                tasks,
                current_digest,
            )
            return iteration_id, result

        return await self._execute(
            actor=actor,
            scope="planning:write",
            operation="planning.schedule.apply",
            target_type="iteration",
            idempotency_target_id=iteration_id,
            command=command,
            request_payload=payload,
            mutate=mutate,
        )
