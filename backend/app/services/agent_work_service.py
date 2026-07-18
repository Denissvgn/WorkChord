"""Durable agent assignment, current-work, verification, and recovery services."""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import logging
import secrets
from datetime import date, datetime, timedelta
from typing import Any, Callable, Iterable, Optional

from sqlalchemy import func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import (
    AgentActor,
    AgentIdempotencyRecord,
    AgentRun,
    AgentTaskAssignment,
    TaskEvent,
)
from app.models.task import Task, TaskDependency, TaskStatus
from app.models.project import Project, ProjectUpdateEntry
from app.models.team_member import TeamMember, TeamMemberProfile
from app.models.triage import TriageItem
from app.schemas.agent import (
    AgentActorResponse,
    AgentDiscoveryTriageCreate,
    AgentDiscoveryTriageResponse,
    AgentProjectUpdateCreate,
    AgentProjectUpdateResponse,
    AgentActorRosterItem,
    AgentCollectionPageMetadata,
    AgentDependencyContext,
    AgentPaginationMetadata,
    AgentRecoveryListResponse,
    AgentReviewVerdict,
    AgentReviewVerdictResponse,
    AgentReviewQueueResponse,
    AgentRecoveryItem,
    AgentRecoveryRequeue,
    AgentRecoveryRequeueResponse,
    AgentRunResponse,
    AgentTaskAssignmentCreate,
    AgentTaskAssignmentResponse,
    AgentTaskAssignmentUpdate,
    AgentTaskContextResponse,
    AgentWorkBegin,
    AgentWorkBeginResponse,
    AgentWorkDecisionResponse,
    AgentWorkItem,
    AgentWorkPaginationMetadata,
    AgentWorkRenew,
    AgentWorkSubmit,
    AgentWorkTerminal,
    AgentWorkTerminalResponse,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    actor_has_scope,
    actor_scopes,
    validate_idempotency_key,
)
from app.services.task_service import TaskService, TaskVersionConflictError
from app.services.project_service import ProjectService
from app.schemas.project import ProjectUpdateEntryCreate
from app.schemas.triage import TriageItemCreate
from app.services.triage_service import TriageService
from app.utils.time import as_utc, utc_now


logger = logging.getLogger(__name__)


LIVE_ASSIGNMENT_STATES = ("queued", "accepted")
QUEUE_CLASS_RANK = {"rework": 0, "recovery": 1, "normal": 2}
REQUIRED_BRIEF_SECTIONS = (
    "goal",
    "context and sources",
    "scope",
    "out of scope",
    "acceptance criteria",
    "verification",
)
RECOVERY_LIFECYCLE_EVENT_TYPES = (
    "agent.work_began",
    "agent.work_submitted",
    "agent.work_recovery_required",
    "agent.recovery_requeued",
    "agent.verification_verdict",
)
PENDING_RECOVERY_SIGNAL_TYPES = {
    "agent.work_began",
    "agent.work_recovery_required",
    "agent.recovery_requeued",
}


def _json_loads(value: Optional[str], fallback: Any) -> Any:
    try:
        return json.loads(value) if value else fallback
    except (json.JSONDecodeError, TypeError):
        return fallback


def parse_task_brief(description: Optional[str]) -> dict[str, str]:
    """Parse level-two Markdown sections from the portable task-brief template."""
    sections: dict[str, list[str]] = {}
    current: Optional[str] = None
    for raw_line in (description or "").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return {
        key: "\n".join(lines).strip()
        for key, lines in sections.items()
        if "\n".join(lines).strip()
    }


class AgentWorkService:
    """Coordinate PM dispatch and low-freedom worker lifecycle commands."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_service = TaskService(db)

    @staticmethod
    def _audited_command_request(
        data: Any,
        *,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
        exclude_unset: bool = False,
    ) -> tuple[AgentPlanningCommandContext, dict[str, Any]]:
        """Validate PM audit metadata and bind it into the exact request hash."""
        command = AgentPlanningCommandContext(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
        payload = data.model_dump(mode="json", exclude_unset=exclude_unset)
        return command, {
            "command": {
                "rationale": command.rationale,
                "correlation_id": command.correlation_id,
            },
            "payload": payload,
        }

    @staticmethod
    def _require_any_scope(actor: AgentActor, *scopes: str) -> None:
        if not any(actor_has_scope(actor, scope) for scope in scopes):
            raise AgentPermissionError(
                f"Missing required scope; expected one of: {', '.join(scopes)}"
            )

    @staticmethod
    def actor_response(actor: AgentActor) -> AgentActorResponse:
        return AgentActorResponse(
            id=actor.id,
            name=actor.name,
            display_name=actor.display_name,
            scopes=actor_scopes(actor),
            enabled=actor.enabled,
            role=actor.role,
            profile_id=actor.profile_id,
            work_policy=actor.work_policy or "assigned_only",
            max_parallel_work=actor.max_parallel_work or 1,
            queue_revision=actor.queue_revision or 1,
            created_at=actor.created_at,
            last_seen_at=actor.last_seen_at,
        )

    @staticmethod
    def assignment_response(assignment: AgentTaskAssignment) -> AgentTaskAssignmentResponse:
        return AgentTaskAssignmentResponse(
            id=assignment.id,
            task_id=assignment.task_id,
            actor_id=assignment.actor_id,
            team_member_id=assignment.team_member_id,
            purpose=assignment.purpose,
            queue_class=assignment.queue_class,
            state=assignment.state,
            queue_rank=assignment.queue_rank,
            not_before=assignment.not_before,
            assigned_by_actor_id=assignment.assigned_by_actor_id,
            reviewer_profile_id=assignment.reviewer_profile_id,
            task_version=assignment.task_version,
            model_binding_id=assignment.model_binding_id,
            model_binding_revision=assignment.model_binding_revision,
            routing_snapshot=_json_loads(assignment.routing_snapshot, {}),
            reason=assignment.reason,
            created_at=assignment.created_at,
            updated_at=assignment.updated_at,
        )

    @staticmethod
    def run_response(run: AgentRun) -> AgentRunResponse:
        return AgentRunResponse(
            id=run.id,
            task_id=run.task_id,
            actor_id=run.actor_id,
            assignment_id=run.assignment_id,
            claim_generation=run.claim_generation,
            status=run.status,
            trace_id=run.trace_id,
            model_binding_id=run.model_binding_id,
            model_binding_revision=run.model_binding_revision,
            configured_model_alias=run.configured_model_alias,
            resolved_model_id=run.resolved_model_id,
            model=run.model,
            tool_name=run.tool_name,
            metadata=_json_loads(run.run_metadata, {}),
            artifact_links=_json_loads(run.artifact_links, []),
            commit_url=run.commit_url,
            pr_url=run.pr_url,
            summary=run.summary,
            error=run.error,
            started_at=run.started_at,
            ended_at=run.ended_at,
            heartbeat_at=run.heartbeat_at,
        )

    async def list_actor_roster(self, actor: AgentActor) -> list[AgentActorRosterItem]:
        """Return enabled actor dispatch metadata without any key material."""
        self._require_any_scope(actor, "assignments:write", "planning:read")
        result = await self.db.execute(
            select(AgentActor)
            .where(AgentActor.enabled.is_(True))
            .order_by(AgentActor.display_name, AgentActor.id)
        )
        actors = result.scalars().all()
        roster: list[AgentActorRosterItem] = []
        for item in actors:
            queued = await self._assignment_count(item.id, "queued")
            accepted = await self._assignment_count(item.id, "accepted")
            running_result = await self.db.execute(
                select(func.count(AgentRun.id)).where(
                    AgentRun.actor_id == item.id,
                    AgentRun.status == "running",
                )
            )
            roster.append(
                AgentActorRosterItem(
                    **self.actor_response(item).model_dump(),
                    queued_assignments=queued,
                    accepted_assignments=accepted,
                    running_runs=int(running_result.scalar_one()),
                )
            )
        return roster

    async def _assignment_count(self, actor_id: int, state: str) -> int:
        result = await self.db.execute(
            select(func.count(AgentTaskAssignment.id)).where(
                AgentTaskAssignment.actor_id == actor_id,
                AgentTaskAssignment.state == state,
            )
        )
        return int(result.scalar_one())

    async def _assignment_lock_hint(
        self, assignment_id: int
    ) -> Optional[tuple[int, int]]:
        """Read immutable lock-routing keys before taking canonical row locks.

        Mutating commands must not lock an assignment merely to discover its task:
        doing so would invert the shared Task -> Actor -> Assignment -> Run order.
        The task lock serializes every supported assignment mutation, after which
        callers lock and revalidate the assignment row.
        """
        result = await self.db.execute(
            select(
                AgentTaskAssignment.task_id,
                AgentTaskAssignment.actor_id,
            ).where(AgentTaskAssignment.id == assignment_id)
        )
        row = result.one_or_none()
        if row is None:
            return None
        return int(row.task_id), int(row.actor_id)

    async def _lock_task(self, task_id: int) -> Optional[Task]:
        """Lock a task first and then load its complete response relationships."""
        if self.db.get_bind().dialect.name == "sqlite":
            # SQLite ignores SELECT ... FOR UPDATE. A no-op write acquires its
            # database write reservation before any mutable graph state is
            # evaluated, giving the default deployment the same serialized
            # command boundary as row-locking databases.
            await self.db.execute(
                text("UPDATE tasks SET id = id WHERE id = :task_id"),
                {"task_id": task_id},
            )
        result = await self.db.execute(
            select(Task.id).where(Task.id == task_id).with_for_update()
        )
        if result.scalar_one_or_none() is None:
            return None
        return await self.task_service.get_by_id(task_id)

    async def _lock_actors(self, actor_ids: Iterable[int]) -> dict[int, AgentActor]:
        """Lock actor rows in primary-key order, refreshing identity-map state."""
        ordered_ids = sorted({int(actor_id) for actor_id in actor_ids})
        if not ordered_ids:
            return {}
        result = await self.db.execute(
            select(AgentActor)
            .where(AgentActor.id.in_(ordered_ids))
            .order_by(AgentActor.id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return {item.id: item for item in result.scalars().all()}

    async def _lock_task_assignments(
        self,
        task_id: int,
        *,
        states: Optional[Iterable[str]] = None,
    ) -> list[AgentTaskAssignment]:
        """Lock a task's selected assignment rows in primary-key order."""
        query = select(AgentTaskAssignment).where(
            AgentTaskAssignment.task_id == task_id
        )
        if states is not None:
            query = query.where(AgentTaskAssignment.state.in_(tuple(states)))
        result = await self.db.execute(
            query.order_by(AgentTaskAssignment.id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return list(result.scalars().all())

    async def _lock_task_runs(
        self,
        task_id: int,
        *,
        run_ids: Optional[Iterable[int]] = None,
        status: Optional[str] = None,
    ) -> list[AgentRun]:
        """Lock selected run rows last and in primary-key order."""
        query = select(AgentRun).where(AgentRun.task_id == task_id)
        if run_ids is not None:
            ordered_ids = sorted({int(run_id) for run_id in run_ids})
            if not ordered_ids:
                return []
            query = query.where(AgentRun.id.in_(ordered_ids))
        if status is not None:
            query = query.where(AgentRun.status == status)
        result = await self.db.execute(
            query.order_by(AgentRun.id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return list(result.scalars().all())

    async def _has_pending_recovery_signal(self, task_id: int) -> bool:
        """Return whether the latest agent lifecycle evidence still needs ownership."""
        result = await self.db.execute(
            select(TaskEvent.event_type)
            .where(
                TaskEvent.task_id == task_id,
                TaskEvent.event_type.in_(RECOVERY_LIFECYCLE_EVENT_TYPES),
            )
            .order_by(TaskEvent.created_at.desc(), TaskEvent.id.desc())
            .limit(1)
        )
        latest = result.scalar_one_or_none()
        return latest in PENDING_RECOVERY_SIGNAL_TYPES

    @staticmethod
    def _validate_assignment_actor(actor: AgentActor, purpose: str) -> None:
        """Require an enabled role plus the scope needed to perform its purpose."""
        if not actor.enabled:
            raise ValueError("Assignment actor must be enabled")
        if purpose == "execution":
            if actor.role not in {"worker", "pm"} or not actor_has_scope(
                actor, "work:execute"
            ):
                raise ValueError(
                    "Execution assignments require a worker or PM actor with work:execute"
                )
            return
        if actor.role not in {"verifier", "pm"} or not actor_has_scope(
            actor, "verification:write"
        ):
            raise ValueError(
                "Verification assignments require a verifier or PM actor with verification:write"
            )

    async def _validate_assignment_context(
        self,
        task: Task,
        *,
        team_member_id: Optional[int],
        reviewer_profile_id: Optional[int],
    ) -> None:
        """Validate optional capacity and reviewer references against live records."""
        if team_member_id is not None:
            member = await self.db.get(TeamMember, team_member_id)
            if member is None or member.iteration_id != task.iteration_id:
                raise ValueError(
                    "Assignment team member must belong to the task iteration"
                )
            if task.assignee_id is not None and task.assignee_id != team_member_id:
                raise ValueError(
                    "Assignment team member must match the task capacity owner"
                )
        if reviewer_profile_id is not None:
            reviewer = await self.db.get(TeamMemberProfile, reviewer_profile_id)
            if reviewer is None:
                raise ValueError("Reviewer profile not found")

    async def list_assignments(
        self,
        principal: AgentActor,
        *,
        task_id: Optional[int] = None,
        actor_id: Optional[int] = None,
        purpose: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 200,
    ) -> list[AgentTaskAssignmentResponse]:
        """Return a secret-free durable assignment projection for restart-safe reads."""
        self._require_any_scope(principal, "assignments:read", "planning:read")
        can_read_team_queue = actor_has_scope(principal, "planning:read")
        if not can_read_team_queue:
            if actor_id is not None and actor_id != principal.id:
                raise AgentPermissionError("Actors may read only their own assignments")
            actor_id = principal.id
        query = select(AgentTaskAssignment)
        if task_id is not None:
            query = query.where(AgentTaskAssignment.task_id == task_id)
        if actor_id is not None:
            query = query.where(AgentTaskAssignment.actor_id == actor_id)
        if purpose is not None:
            query = query.where(AgentTaskAssignment.purpose == purpose)
        if state is not None:
            query = query.where(AgentTaskAssignment.state == state)
        result = await self.db.execute(
            query.order_by(
                AgentTaskAssignment.actor_id,
                AgentTaskAssignment.queue_rank,
                AgentTaskAssignment.id,
            ).limit(limit)
        )
        return [self.assignment_response(item) for item in result.scalars().all()]

    async def create_assignment(
        self,
        principal: AgentActor,
        data: AgentTaskAssignmentCreate,
        *,
        idempotency_key: Optional[str] = None,
        rationale: str,
        correlation_id: str,
    ) -> AgentTaskAssignmentResponse:
        """Dispatch one task to one provisioned actor."""
        self._require_any_scope(principal, "assignments:write")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        assert idempotency_key is not None
        task = await self._lock_task(data.task_id)
        command, request_payload = self._audited_command_request(
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
        replay = await self._idempotent_replay(
            principal,
            "assignment.create",
            "task",
            data.task_id,
            idempotency_key,
            request_payload,
        )
        if replay:
            snapshot = replay.get("response")
            if snapshot is not None:
                return AgentTaskAssignmentResponse.model_validate(snapshot)
            raise AgentConflictError("Idempotent assignment receipt is unavailable")

        if task is None:
            raise ValueError("Task not found")
        if task.version != data.expected_task_version:
            raise TaskVersionConflictError(
                data.expected_task_version,
                self.task_service._metadata_from_task(task),
            )
        locked_actors = await self._lock_actors((data.actor_id,))
        target = locked_actors.get(data.actor_id)
        if target is None:
            raise ValueError("Assignment actor must exist and be enabled")
        self._validate_assignment_actor(target, data.purpose)
        await self._validate_assignment_context(
            task,
            team_member_id=data.team_member_id or task.assignee_id,
            reviewer_profile_id=data.reviewer_profile_id,
        )
        task_assignments = await self._lock_task_assignments(task.id)
        expected_status = (
            TaskStatus.RESOLVED.value
            if data.purpose == "verification"
            else TaskStatus.PLANNED.value
            if data.queue_class == "normal"
            else TaskStatus.ACTIVE.value
        )
        if task.status != expected_status:
            raise AgentConflictError(
                f"{data.purpose}/{data.queue_class} assignment requires task status {expected_status}"
            )
        if data.purpose == "execution" and data.queue_class == "normal":
            definition_blockers = self._definition_blockers(task)
            if definition_blockers:
                raise ValueError(
                    "Task is not definition-ready: " + ", ".join(definition_blockers)
                )
        if data.purpose == "verification":
            running_runs = await self._lock_task_runs(task.id, status="running")
            execution_assignments = [
                item for item in task_assignments if item.purpose == "execution"
            ]
            if (
                task.claimed_by is not None
                or running_runs
                or any(item.state in LIVE_ASSIGNMENT_STATES for item in execution_assignments)
            ):
                raise AgentConflictError(
                    "Verification requires released execution ownership and a terminal run"
                )
            if any(
                item.actor_id == target.id and item.state == "fulfilled"
                for item in execution_assignments
            ):
                raise AgentConflictError(
                    "Verification actor must be independent from the implementation actor"
                )

        if any(
            item.purpose == data.purpose and item.state in LIVE_ASSIGNMENT_STATES
            for item in task_assignments
        ):
            raise AgentConflictError("Task already has a live assignment for this purpose")

        assignment = AgentTaskAssignment(
            task_id=task.id,
            actor_id=target.id,
            team_member_id=data.team_member_id or task.assignee_id,
            purpose=data.purpose,
            queue_class=data.queue_class,
            state="queued",
            queue_rank=data.queue_rank,
            not_before=data.not_before,
            assigned_by_actor_id=principal.id if principal.id else None,
            reviewer_profile_id=data.reviewer_profile_id,
            task_version=task.version,
            routing_snapshot=json.dumps(data.routing_snapshot, ensure_ascii=False, default=str),
            reason=data.reason,
        )
        self.db.add(assignment)
        target.queue_revision += 1
        await self.db.flush()
        await self.task_service.record_task_event(
            task.id,
            "agent.assignment_created",
            {
                "assignment_id": assignment.id,
                "actor_id": target.id,
                "purpose": assignment.purpose,
                "queue_class": assignment.queue_class,
                "queue_rank": assignment.queue_rank,
                "queue_revision": target.queue_revision,
                "rationale": command.rationale,
            },
            actor_type="agent",
            actor_id=principal.id if principal.id else None,
            correlation_id=command.correlation_id,
            idempotency_key=idempotency_key,
        )
        response = self.assignment_response(assignment)
        await self._record_idempotency(
            principal,
            "assignment.create",
            "task",
            task.id,
            idempotency_key,
            request_payload,
            {"response": response.model_dump(mode="json")},
        )
        await self.db.commit()
        return response

    async def update_assignment(
        self,
        assignment_id: int,
        principal: AgentActor,
        data: AgentTaskAssignmentUpdate,
        *,
        idempotency_key: Optional[str] = None,
        rationale: str,
        correlation_id: str,
    ) -> AgentTaskAssignmentResponse:
        """Reassign, reorder, or cancel queued work."""
        self._require_any_scope(principal, "assignments:write")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        assert idempotency_key is not None
        hint = await self._assignment_lock_hint(assignment_id)
        if hint is None:
            raise ValueError("Assignment not found")
        task = await self._lock_task(hint[0])
        if task is None:
            raise AgentConflictError("Assigned task is missing")
        current_hint = await self._assignment_lock_hint(assignment_id)
        if current_hint is None or current_hint[0] != task.id:
            raise AgentConflictError("Assignment changed while acquiring task ownership")
        actor_ids = {current_hint[1]}
        if data.actor_id is not None:
            actor_ids.add(data.actor_id)
        locked_actors = await self._lock_actors(actor_ids)
        task_assignments = await self._lock_task_assignments(task.id)
        assignment = next(
            (item for item in task_assignments if item.id == assignment_id),
            None,
        )
        if (
            assignment is None
            or assignment.task_id != task.id
            or assignment.actor_id != current_hint[1]
        ):
            raise AgentConflictError("Assignment changed while acquiring row locks")
        command, request_payload = self._audited_command_request(
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
            exclude_unset=True,
        )
        replay = await self._idempotent_replay(
            principal,
            "assignment.update",
            "assignment",
            assignment_id,
            idempotency_key,
            request_payload,
        )
        if replay:
            snapshot = replay.get("response")
            if snapshot is not None:
                return AgentTaskAssignmentResponse.model_validate(snapshot)
            raise AgentConflictError("Idempotent assignment receipt is unavailable")
        if assignment.state != "queued":
            raise AgentConflictError("Only queued assignments can be changed by PM control")
        current_actor = locked_actors.get(assignment.actor_id)
        if current_actor is None:
            raise AgentConflictError("Assignment actor is missing")
        if current_actor.queue_revision != data.expected_queue_revision:
            raise AgentConflictError(
                f"Queue revision conflict: expected {data.expected_queue_revision}, "
                f"current {current_actor.queue_revision}"
            )
        old_actor = current_actor
        if data.actor_id is not None and data.actor_id != assignment.actor_id:
            replacement = locked_actors.get(data.actor_id)
            if replacement is None:
                raise ValueError("Replacement actor must exist and be enabled")
            self._validate_assignment_actor(replacement, assignment.purpose)
            if assignment.purpose == "verification":
                if any(
                    item.purpose == "execution"
                    and item.actor_id == replacement.id
                    and item.state == "fulfilled"
                    for item in task_assignments
                ):
                    raise AgentConflictError(
                        "Verification actor must be independent from the implementation actor"
                    )
            assignment.actor_id = replacement.id
            replacement.queue_revision += 1
            current_actor = replacement
        if data.queue_rank is not None:
            assignment.queue_rank = data.queue_rank
        if "not_before" in data.model_fields_set:
            assignment.not_before = data.not_before
        if "reviewer_profile_id" in data.model_fields_set:
            await self._validate_assignment_context(
                task,
                team_member_id=assignment.team_member_id,
                reviewer_profile_id=data.reviewer_profile_id,
            )
            assignment.reviewer_profile_id = data.reviewer_profile_id
        if data.state is not None:
            assignment.state = data.state
        if "reason" in data.model_fields_set:
            assignment.reason = data.reason
        old_actor.queue_revision += 1
        await self.task_service.record_task_event(
            assignment.task_id,
            "agent.assignment_updated",
            {
                "assignment_id": assignment.id,
                "actor_id": assignment.actor_id,
                "state": assignment.state,
                "queue_rank": assignment.queue_rank,
                "queue_revision": current_actor.queue_revision,
                "reason": assignment.reason,
                "rationale": command.rationale,
            },
            actor_type="agent",
            actor_id=principal.id if principal.id else None,
            correlation_id=command.correlation_id,
            idempotency_key=idempotency_key,
        )
        response = self.assignment_response(assignment)
        await self._record_idempotency(
            principal,
            "assignment.update",
            "assignment",
            assignment.id,
            idempotency_key,
            request_payload,
            {"response": response.model_dump(mode="json")},
        )
        await self.db.commit()
        return response

    async def get_work(
        self,
        actor: AgentActor,
        *,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> AgentWorkDecisionResponse:
        """Return the authoritative resume/begin/wait/recovery decision."""
        self._require_any_scope(actor, "assignments:read", "tasks:read")
        self._validate_page_limit(limit)
        now = utc_now()
        await self.db.refresh(actor)
        self._require_any_scope(actor, "assignments:read", "tasks:read")
        queue_revision = int(actor.queue_revision)
        accepted_result = await self.db.execute(
            select(AgentTaskAssignment)
            .where(
                AgentTaskAssignment.actor_id == actor.id,
                AgentTaskAssignment.purpose == "execution",
                AgentTaskAssignment.state == "accepted",
            )
            .order_by(AgentTaskAssignment.id)
        )
        accepted = accepted_result.scalars().all()
        running_result = await self.db.execute(
            select(AgentRun).where(
                AgentRun.actor_id == actor.id,
                AgentRun.status == "running",
            )
        )
        running = running_result.scalars().all()
        recovery_codes = await self._current_recovery_codes(actor, accepted, running, now)
        if recovery_codes:
            current_item = None
            if accepted:
                current_item = await self._work_item(accepted[0], 0, now, running=running)
            ownership_records = [
                {
                    "bucket": "running_ownership",
                    "run": self.run_response(run).model_dump(mode="json"),
                }
                for run in running
            ]
            if current_item is not None:
                ownership_records.append(
                    self._work_snapshot_record("current", current_item)
                )
            _, _, pagination = self._paginate_work_collections(
                actor_id=actor.id,
                queue_revision=queue_revision,
                ready=[],
                blocked=[],
                limit=limit,
                cursor=cursor,
                extra_records=ownership_records,
            )
            if await self._read_actor_queue_revision(actor.id) != queue_revision:
                raise AgentConflictError("queue_changed_during_read")
            return AgentWorkDecisionResponse(
                actor=self.actor_response(actor),
                server_time=now,
                queue_revision=queue_revision,
                pagination=pagination,
                cursor=pagination.next_cursor,
                state="attention_required",
                current=current_item,
                recovery_codes=recovery_codes,
                next_poll_after=now + timedelta(minutes=5),
            )
        if accepted:
            current = await self._work_item(accepted[0], 0, now, running=running)
            _, _, pagination = self._paginate_work_collections(
                actor_id=actor.id,
                queue_revision=queue_revision,
                ready=[],
                blocked=[],
                limit=limit,
                cursor=cursor,
                extra_records=[self._work_snapshot_record("current", current)],
            )
            if await self._read_actor_queue_revision(actor.id) != queue_revision:
                raise AgentConflictError("queue_changed_during_read")
            return AgentWorkDecisionResponse(
                actor=self.actor_response(actor),
                server_time=now,
                queue_revision=queue_revision,
                pagination=pagination,
                cursor=pagination.next_cursor,
                state="resume",
                current=current,
                next_poll_after=now + timedelta(minutes=5),
            )

        queued_result = await self.db.execute(
            select(AgentTaskAssignment)
            .where(
                AgentTaskAssignment.actor_id == actor.id,
                AgentTaskAssignment.purpose == "execution",
                AgentTaskAssignment.state == "queued",
            )
            .order_by(
                AgentTaskAssignment.queue_rank,
                AgentTaskAssignment.not_before,
                AgentTaskAssignment.id,
            )
        )
        assignments = queued_result.scalars().all()
        items: list[AgentWorkItem] = []
        blocked: list[AgentWorkItem] = []
        for assignment in assignments:
            item = await self._work_item(assignment, 0, now)
            if item.blocker_codes:
                blocked.append(item)
            else:
                items.append(item)
        items.sort(key=lambda item: tuple(item.selection_key))
        blocked.sort(key=lambda item: tuple(item.selection_key))
        for position, item in enumerate(items, start=1):
            item.queue_position = position
        for position, item in enumerate(blocked, start=1):
            item.queue_position = position
        page, blocked_page, pagination = self._paginate_work_collections(
            actor_id=actor.id,
            queue_revision=queue_revision,
            ready=items,
            blocked=blocked,
            limit=limit,
            cursor=cursor,
        )
        if await self._read_actor_queue_revision(actor.id) != queue_revision:
            raise AgentConflictError("queue_changed_during_read")
        if items:
            return AgentWorkDecisionResponse(
                actor=self.actor_response(actor),
                server_time=now,
                queue_revision=queue_revision,
                pagination=pagination,
                cursor=pagination.next_cursor,
                state="start_assigned",
                next=items[0],
                queue=page,
                blocked_assigned=blocked_page,
                next_poll_after=now + timedelta(minutes=5),
            )
        if blocked:
            future_times = [
                item.assignment.not_before
                for item in blocked
                if item.assignment.not_before is not None
                and as_utc(item.assignment.not_before) > as_utc(now)
            ]
            return AgentWorkDecisionResponse(
                actor=self.actor_response(actor),
                server_time=now,
                queue_revision=queue_revision,
                pagination=pagination,
                cursor=pagination.next_cursor,
                state="wait",
                next=blocked[0],
                blocked_assigned=blocked_page,
                next_poll_after=min(future_times) if future_times else now + timedelta(minutes=5),
            )
        return AgentWorkDecisionResponse(
            actor=self.actor_response(actor),
            server_time=now,
            queue_revision=queue_revision,
            pagination=pagination,
            cursor=pagination.next_cursor,
            state="no_work",
            next_poll_after=now + timedelta(minutes=5),
        )

    async def get_reviews(
        self,
        actor: AgentActor,
        *,
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> AgentReviewQueueResponse:
        """Return the separate verifier-assignment queue."""
        self._require_any_scope(actor, "verification:read", "verification:write")
        self._validate_page_limit(limit)
        now = utc_now()
        await self.db.refresh(actor)
        self._require_any_scope(actor, "verification:read", "verification:write")
        queue_revision = int(actor.queue_revision)
        result = await self.db.execute(
            select(AgentTaskAssignment).where(
                AgentTaskAssignment.actor_id == actor.id,
                AgentTaskAssignment.purpose == "verification",
                AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES),
            )
        )
        items = [
            await self._work_item(assignment, 0, now)
            for assignment in result.scalars().all()
        ]
        items.sort(key=lambda item: tuple(item.selection_key))
        for position, item in enumerate(items, start=1):
            item.queue_position = position
        page, pagination = self._paginate_single_collection(
            kind="reviews",
            actor_id=actor.id,
            queue_revision=queue_revision,
            items=items,
            records=[self._work_snapshot_record("review", item) for item in items],
            limit=limit,
            cursor=cursor,
            key=self._work_item_key,
        )
        if await self._read_actor_queue_revision(actor.id) != queue_revision:
            raise AgentConflictError("queue_changed_during_read")
        return AgentReviewQueueResponse(items=page, pagination=pagination)

    async def get_task_context(
        self,
        actor: AgentActor,
        task_id: int,
        *,
        assignment_id: Optional[int] = None,
    ) -> AgentTaskContextResponse:
        """Return complete worker context with brief and dependency states."""
        self._require_any_scope(actor, "assignments:read", "tasks:read", "verification:read")
        task = await self.task_service.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found")
        assignment = None
        if assignment_id is not None:
            assignment = await self.db.get(AgentTaskAssignment, assignment_id)
            if assignment is None or assignment.task_id != task.id:
                raise ValueError("Assignment not found for task")
            privileged_context_reader = actor_has_scope(
                actor, "planning:read"
            ) or actor_has_scope(actor, "admin")
            if assignment.actor_id != actor.id and not privileged_context_reader:
                raise AgentPermissionError("Assignment context belongs to another actor")
            if (
                assignment.state not in LIVE_ASSIGNMENT_STATES
                and not privileged_context_reader
            ):
                raise AgentPermissionError(
                    "Task context requires a live assignment to this actor"
                )
        else:
            result = await self.db.execute(
                select(AgentTaskAssignment)
                .where(
                    AgentTaskAssignment.task_id == task.id,
                    AgentTaskAssignment.actor_id == actor.id,
                    AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES),
                )
                .order_by(AgentTaskAssignment.created_at.desc())
            )
            assignment = result.scalars().first()
        if (
            assignment is None
            and not actor_has_scope(actor, "admin")
            and not actor_has_scope(actor, "planning:read")
        ):
            raise AgentPermissionError("Task context requires a live assignment to this actor")
        brief = parse_task_brief(task.description)
        definition_blockers = self._definition_blockers(task)
        start_blockers = await self._start_blockers(task, assignment, utc_now())
        parent_chain: list[dict[str, Any]] = []
        parent = task.parent
        seen: set[int] = set()
        while parent is not None and parent.id not in seen:
            seen.add(parent.id)
            parent_chain.append(
                {"id": parent.id, "title": parent.title, "status": parent.status, "version": parent.version}
            )
            parent = parent.parent
        dependencies: list[AgentDependencyContext] = []
        for edge in task.dependencies:
            dependency = edge.depends_on
            dependencies.append(
                AgentDependencyContext(
                    task_id=dependency.id,
                    title=dependency.title,
                    status=dependency.status,
                    version=dependency.version,
                )
            )
        request_sources = [
            {
                "id": link.id,
                "request_source_id": link.request_source_id,
                "triage_item_id": link.triage_item_id,
                "task_id": link.task_id,
                "project_id": link.project_id,
                "created_at": link.created_at,
                "request_source": link.request_source,
            }
            for link in task.request_source_links
        ]
        from app.services.agent_service import AgentService

        timeline = await AgentService(self.db).get_task_timeline(task.id)
        return AgentTaskContextResponse(
            task=self.task_service.task_to_response(task),
            assignment=self.assignment_response(assignment) if assignment else None,
            task_brief=brief,
            parent_chain=parent_chain,
            dependencies=dependencies,
            request_sources=request_sources,
            timeline=timeline,
            definition_ready=not definition_blockers,
            start_ready=not start_blockers,
            blocker_codes=sorted(set(definition_blockers + start_blockers)),
        )

    async def begin(
        self,
        actor: AgentActor,
        data: AgentWorkBegin,
        *,
        idempotency_key: str,
    ) -> AgentWorkBeginResponse:
        """Atomically accept, fence, claim, run, and activate selected work."""
        self._require_any_scope(actor, "work:execute")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        hint = await self._assignment_lock_hint(data.assignment_id)
        if hint is None or hint[1] != actor.id:
            raise AgentPermissionError("Assignment does not belong to this actor")
        task = await self._lock_task(hint[0])
        if task is None:
            raise ValueError("Task not found")
        current_hint = await self._assignment_lock_hint(data.assignment_id)
        if (
            current_hint is None
            or current_hint[0] != task.id
            or current_hint[1] != actor.id
        ):
            raise AgentPermissionError("Assignment does not belong to this actor")
        actor = (await self._lock_actors((actor.id,))).get(actor.id)
        if actor is None:
            raise AgentPermissionError("Assignment actor is missing")
        task_assignments = await self._lock_task_assignments(task.id)
        assignment = next(
            (item for item in task_assignments if item.id == data.assignment_id),
            None,
        )
        if assignment is None or assignment.actor_id != actor.id:
            raise AgentPermissionError("Assignment does not belong to this actor")
        request_payload = data.model_dump(mode="json")
        replay = await self._idempotent_replay(
            actor,
            "work.begin",
            "assignment",
            data.assignment_id,
            idempotency_key,
            request_payload,
        )
        if replay:
            return await self._replay_live_fence_receipt(actor, replay)
        if assignment.purpose != "execution" or assignment.state != "queued":
            raise AgentConflictError("Assignment is not queued execution work")
        if actor.queue_revision != data.queue_revision:
            raise AgentConflictError(
                f"Queue revision conflict: expected {data.queue_revision}, current {actor.queue_revision}"
            )
        if await self._assignment_count(actor.id, "accepted") >= actor.max_parallel_work:
            raise AgentConflictError("Actor has reached max_parallel_work")
        decision = await self.get_work(actor, limit=1)
        if (
            decision.state != "start_assigned"
            or decision.next is None
            or decision.next.assignment.id != assignment.id
        ):
            raise AgentConflictError(
                "Assignment is not the server-selected next work item"
            )
        if assignment.task_version != task.version:
            raise TaskVersionConflictError(
                assignment.task_version,
                self.task_service._metadata_from_task(task),
            )
        blockers = await self._start_blockers(task, assignment, utc_now())
        if blockers:
            raise AgentConflictError("Work is not start-ready: " + ", ".join(blockers))
        now = utc_now()
        if assignment.queue_class == "normal":
            task, _, _ = await self.task_service.change_status(
                task.id,
                TaskStatus.ACTIVE,
                reason="Atomic agent work begin",
                actor_type="agent",
                actor_id=actor.id,
                trace_id=data.trace_id,
                expected_version=task.version,
                commit=False,
            )
            if task is None:
                raise AgentConflictError("Task could not be activated")
        else:
            await self.task_service.reserve_task_version(task, task.version)
        task.claim_generation += 1
        task.claim_id = secrets.token_hex(24)
        task.claimed_by = actor.id
        task.claim_expires_at = now + timedelta(seconds=data.lease_seconds)
        assignment.state = "accepted"
        assignment.task_version = task.version
        actor.queue_revision += 1
        run = AgentRun(
            task_id=task.id,
            actor_id=actor.id,
            assignment_id=assignment.id,
            claim_generation=task.claim_generation,
            status="running",
            trace_id=data.trace_id,
            model=data.model,
            tool_name=data.tool_name,
            run_metadata=json.dumps(data.metadata, ensure_ascii=False, default=str),
            artifact_links="[]",
            idempotency_key=idempotency_key,
            heartbeat_at=now,
        )
        self.db.add(run)
        await self.db.flush()
        response = AgentWorkBeginResponse(
            assignment=self.assignment_response(assignment),
            task=self.task_service.task_to_response(task),
            run=self.run_response(run),
            claim_id=task.claim_id,
            claim_generation=task.claim_generation,
            claim_expires_at=task.claim_expires_at,
            queue_revision=actor.queue_revision,
        )
        await self.task_service.record_task_event(
            task.id,
            "agent.work_began",
            {
                "assignment_id": assignment.id,
                "run_id": run.id,
                "queue_class": assignment.queue_class,
                "claim_generation": task.claim_generation,
                "claim_expires_at": task.claim_expires_at.isoformat(),
                "task_version": task.version,
            },
            actor_type="agent",
            actor_id=actor.id,
            trace_id=data.trace_id,
            idempotency_key=idempotency_key,
        )
        await self._record_idempotency(
            actor,
            "work.begin",
            "assignment",
            assignment.id,
            idempotency_key,
            request_payload,
            self._live_fence_receipt(response),
        )
        await self.db.commit()
        return response

    async def submit(
        self,
        actor: AgentActor,
        data: AgentWorkSubmit,
        *,
        idempotency_key: str,
    ) -> AgentWorkTerminalResponse:
        """Atomically finish, resolve, fulfill, and release assigned work."""
        return await self._terminal_work(
            actor,
            data,
            idempotency_key=idempotency_key,
            success=True,
        )

    async def renew_work(
        self,
        actor: AgentActor,
        data: AgentWorkRenew,
        *,
        idempotency_key: str,
    ) -> AgentWorkBeginResponse:
        """Atomically renew an accepted assignment's live claim and heartbeat."""
        self._require_any_scope(actor, "work:execute")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        hint = await self._assignment_lock_hint(data.assignment_id)
        if hint is None or hint[1] != actor.id:
            raise AgentPermissionError("Assignment does not belong to this actor")
        task = await self._lock_task(hint[0])
        if task is None:
            raise ValueError("Assignment, task, or run not found")
        current_hint = await self._assignment_lock_hint(data.assignment_id)
        if (
            current_hint is None
            or current_hint[0] != task.id
            or current_hint[1] != actor.id
        ):
            raise AgentPermissionError("Assignment does not belong to this actor")
        actor = (await self._lock_actors((actor.id,))).get(actor.id)
        if actor is None:
            raise AgentPermissionError("Assignment actor is missing")
        task_assignments = await self._lock_task_assignments(task.id)
        assignment = next(
            (item for item in task_assignments if item.id == data.assignment_id),
            None,
        )
        if assignment is None or assignment.actor_id != actor.id:
            raise AgentPermissionError("Assignment does not belong to this actor")
        request_payload = data.model_dump(mode="json")
        replay = await self._idempotent_replay(
            actor,
            "work.renew",
            "assignment",
            assignment.id,
            idempotency_key,
            request_payload,
        )
        if replay:
            return await self._replay_live_fence_receipt(actor, replay)
        try:
            self._validate_assignment_actor(actor, "execution")
        except ValueError as exc:
            raise AgentConflictError(
                "Assignment actor is no longer eligible for execution"
            ) from exc
        runs = await self._lock_task_runs(task.id, run_ids=(data.run_id,))
        run = runs[0] if runs else None
        if task is None or run is None:
            raise ValueError("Assignment, task, or run not found")
        if (
            assignment.state != "accepted"
            or run.status != "running"
            or run.assignment_id != assignment.id
            or run.actor_id != actor.id
        ):
            raise AgentConflictError("Work is not active and renewable")
        if assignment.task_version != task.version:
            raise AgentConflictError(
                "Assignment scope changed during execution; recovery and redispatch are required"
            )
        self._validate_fence(task, actor, data.claim_id, data.claim_generation)
        if task.version != data.expected_task_version:
            raise TaskVersionConflictError(
                data.expected_task_version,
                self.task_service._metadata_from_task(task),
            )
        await self.task_service.reserve_task_version(task, task.version)
        now = utc_now()
        task.claim_expires_at = now + timedelta(seconds=data.lease_seconds)
        run.heartbeat_at = now
        assignment.task_version = task.version
        response_ids = {
            "assignment_id": assignment.id,
            "run_id": run.id,
            "task_id": task.id,
        }
        response = AgentWorkBeginResponse(
            assignment=self.assignment_response(assignment),
            task=self.task_service.task_to_response(task),
            run=self.run_response(run),
            claim_id=task.claim_id,
            claim_generation=task.claim_generation,
            claim_expires_at=task.claim_expires_at,
            queue_revision=actor.queue_revision,
        )
        await self.task_service.record_task_event(
            task.id,
            "agent.work_renewed",
            {
                **response_ids,
                "claim_generation": task.claim_generation,
                "claim_expires_at": task.claim_expires_at.isoformat(),
                "task_version": task.version,
            },
            actor_type="agent",
            actor_id=actor.id,
            idempotency_key=idempotency_key,
        )
        await self._record_idempotency(
            actor,
            "work.renew",
            "assignment",
            assignment.id,
            idempotency_key,
            request_payload,
            self._live_fence_receipt(response),
        )
        await self.db.commit()
        return response

    async def fail(
        self,
        actor: AgentActor,
        data: AgentWorkTerminal,
        *,
        idempotency_key: str,
    ) -> AgentWorkTerminalResponse:
        """Atomically finish failure, release the fence, and signal recovery."""
        return await self._terminal_work(
            actor,
            data,
            idempotency_key=idempotency_key,
            success=False,
        )

    async def _terminal_work(
        self,
        actor: AgentActor,
        data: AgentWorkSubmit | AgentWorkTerminal,
        *,
        idempotency_key: str,
        success: bool,
    ) -> AgentWorkTerminalResponse:
        self._require_any_scope(actor, "work:execute")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        operation = "work.submit" if success else "work.fail"
        hint = await self._assignment_lock_hint(data.assignment_id)
        if hint is None or hint[1] != actor.id:
            raise AgentPermissionError("Assignment does not belong to this actor")
        task = await self._lock_task(hint[0])
        if task is None:
            raise ValueError("Assignment, task, or run not found")
        current_hint = await self._assignment_lock_hint(data.assignment_id)
        if (
            current_hint is None
            or current_hint[0] != task.id
            or current_hint[1] != actor.id
        ):
            raise AgentPermissionError("Assignment does not belong to this actor")
        actor = (await self._lock_actors((actor.id,))).get(actor.id)
        if actor is None:
            raise AgentPermissionError("Assignment actor is missing")
        task_assignments = await self._lock_task_assignments(task.id)
        assignment = next(
            (item for item in task_assignments if item.id == data.assignment_id),
            None,
        )
        if assignment is None or assignment.actor_id != actor.id:
            raise AgentPermissionError("Assignment does not belong to this actor")
        request_payload = data.model_dump(mode="json")
        replay = await self._idempotent_replay(
            actor,
            operation,
            "assignment",
            data.assignment_id,
            idempotency_key,
            request_payload,
        )
        if replay:
            snapshot = replay.get("response")
            if snapshot is not None:
                return AgentWorkTerminalResponse.model_validate(snapshot)
            raise AgentConflictError("Idempotent terminal receipt is unavailable")
        try:
            self._validate_assignment_actor(actor, "execution")
        except ValueError as exc:
            raise AgentConflictError(
                "Assignment actor is no longer eligible for execution"
            ) from exc
        runs = await self._lock_task_runs(task.id, run_ids=(data.run_id,))
        run = runs[0] if runs else None
        if task is None or run is None:
            raise ValueError("Assignment, task, or run not found")
        if assignment.actor_id != actor.id or run.actor_id != actor.id:
            raise AgentPermissionError("Work belongs to another actor")
        if (
            assignment.state != "accepted"
            or run.status != "running"
            or run.assignment_id != assignment.id
            or run.task_id != task.id
            or run.claim_generation != data.claim_generation
        ):
            raise AgentConflictError("Work is not active")
        if assignment.task_version != task.version:
            raise AgentConflictError(
                "Assignment scope changed during execution; recovery and redispatch are required"
            )
        self._validate_fence(task, actor, data.claim_id, data.claim_generation)
        if task.version != data.expected_task_version:
            raise TaskVersionConflictError(
                data.expected_task_version,
                self.task_service._metadata_from_task(task),
            )
        now = utc_now()
        run.status = "succeeded" if success else data.status
        run.ended_at = now
        run.heartbeat_at = now
        run.summary = data.summary
        run.error = None if success else data.error
        if success:
            run.artifact_links = json.dumps(data.artifact_links, ensure_ascii=False)
            run.commit_url = data.commit_url
            run.pr_url = data.pr_url
            task, _, _ = await self.task_service.change_status(
                task.id,
                TaskStatus.RESOLVED,
                reason="Agent submitted evidence for verification",
                actor_type="agent",
                actor_id=actor.id,
                expected_version=task.version,
                commit=False,
            )
            if task is None:
                raise AgentConflictError("Task could not be resolved")
            assignment.state = "fulfilled"
            event_type = "agent.work_submitted"
        else:
            await self.task_service.reserve_task_version(task, task.version)
            assignment.state = "cancelled"
            assignment.reason = data.error or data.summary or "Worker requested recovery"
            event_type = "agent.work_recovery_required"
        task.claimed_by = None
        task.claim_expires_at = None
        task.claim_id = None
        assignment.task_version = task.version
        actor.queue_revision += 1
        evidence = data.evidence
        response = AgentWorkTerminalResponse(
            assignment=self.assignment_response(assignment),
            task=self.task_service.task_to_response(task),
            run=self.run_response(run),
            recovery_required=not success,
        )
        await self.task_service.record_task_event(
            task.id,
            event_type,
            {
                "assignment_id": assignment.id,
                "run_id": run.id,
                "run_status": run.status,
                "task_version": task.version,
                "summary": data.summary,
                "evidence": evidence,
            },
            actor_type="agent",
            actor_id=actor.id,
            idempotency_key=idempotency_key,
        )
        await self._record_idempotency(
            actor,
            operation,
            "assignment",
            assignment.id,
            idempotency_key,
            request_payload,
            {"response": response.model_dump(mode="json")},
        )
        await self.db.commit()
        return response

    async def review(
        self,
        actor: AgentActor,
        data: AgentReviewVerdict,
        *,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> AgentReviewVerdictResponse:
        """Apply an independent verification verdict and optional rework handback."""
        self._require_any_scope(actor, "verification:write")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        assert idempotency_key is not None
        hint = await self._assignment_lock_hint(data.assignment_id)
        if hint is None:
            raise ValueError("Review assignment or task not found")
        if hint[1] != actor.id and not actor_has_scope(actor, "admin"):
            raise AgentPermissionError("Review belongs to another actor")
        task = await self._lock_task(hint[0])
        if task is None:
            raise ValueError("Review assignment or task not found")
        current_hint = await self._assignment_lock_hint(data.assignment_id)
        if current_hint is None or current_hint[0] != task.id:
            raise AgentConflictError("Review assignment changed while acquiring task ownership")
        actor_ids = {actor.id, current_hint[1]}
        if data.rework_actor_id is not None:
            actor_ids.add(data.rework_actor_id)
        locked_actors = await self._lock_actors(actor_ids)
        principal = locked_actors.get(actor.id)
        if principal is None:
            raise AgentPermissionError("Review actor is missing")
        self._require_any_scope(principal, "verification:write")
        actor = principal
        task_assignments = await self._lock_task_assignments(task.id)
        assignment = next(
            (item for item in task_assignments if item.id == data.assignment_id),
            None,
        )
        if (
            assignment is None
            or assignment.task_id != task.id
            or assignment.actor_id != current_hint[1]
        ):
            raise AgentConflictError("Review assignment changed while acquiring row locks")
        command, request_payload = self._audited_command_request(
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
        replay = await self._idempotent_replay(
            actor,
            "verification.verdict",
            "assignment",
            data.assignment_id,
            idempotency_key,
            request_payload,
        )
        if replay:
            snapshot = replay.get("response")
            if snapshot is not None:
                return AgentReviewVerdictResponse.model_validate(snapshot)
            raise AgentConflictError("Idempotent verification receipt is unavailable")
        if assignment.actor_id != actor.id and not actor_has_scope(actor, "admin"):
            raise AgentPermissionError("Review belongs to another actor")
        assignment_actor = locked_actors.get(assignment.actor_id)
        if assignment_actor is None:
            raise AgentConflictError("Review assignment actor is missing")
        try:
            self._validate_assignment_actor(assignment_actor, "verification")
        except ValueError as exc:
            raise AgentConflictError(
                "Review assignment actor is no longer eligible for verification"
            ) from exc
        if assignment.purpose != "verification" or assignment.state not in LIVE_ASSIGNMENT_STATES:
            raise AgentConflictError("Assignment is not active verification work")
        if task.status != TaskStatus.RESOLVED.value:
            raise AgentConflictError("Verification requires a resolved task")
        if (
            assignment.not_before is not None
            and as_utc(assignment.not_before) > as_utc(utc_now())
        ):
            raise AgentConflictError(
                "Verification assignment is not actionable before not_before"
            )
        if assignment.task_version != task.version:
            raise AgentConflictError(
                "Verification assignment is stale; PM must refresh verification ownership"
            )
        if task.version != data.expected_task_version:
            raise TaskVersionConflictError(
                data.expected_task_version,
                self.task_service._metadata_from_task(task),
            )
        rework_worker: Optional[AgentActor] = None
        if data.verdict == "reject":
            if data.rework_actor_id is None:
                raise ValueError("rework_actor_id is required for rejection")
            rework_worker = locked_actors.get(data.rework_actor_id)
            if rework_worker is None:
                raise ValueError("Rework actor must be an enabled worker or PM")
            self._validate_assignment_actor(rework_worker, "execution")
        new_status = TaskStatus.CLOSED if data.verdict == "pass" else TaskStatus.ACTIVE
        task, _, _ = await self.task_service.change_status(
            task.id,
            new_status,
            reason=data.reason or f"Verification {data.verdict}",
            actor_type="agent",
            actor_id=actor.id,
            correlation_id=command.correlation_id,
            expected_version=task.version,
            idempotency_key=idempotency_key,
            commit=False,
        )
        if task is None:
            raise AgentConflictError("Verification transition failed")
        assignment.state = "fulfilled"
        assignment.task_version = task.version
        assignment_actor.queue_revision += 1
        rework: Optional[AgentTaskAssignment] = None
        if data.verdict == "reject":
            assert rework_worker is not None
            rework = AgentTaskAssignment(
                task_id=task.id,
                actor_id=rework_worker.id,
                team_member_id=task.assignee_id,
                purpose="execution",
                queue_class="rework",
                state="queued",
                queue_rank=data.rework_queue_rank,
                assigned_by_actor_id=actor.id,
                task_version=task.version,
                routing_snapshot="{}",
                reason=data.reason or "Verification rejected",
            )
            self.db.add(rework)
            rework_worker.queue_revision += 1
            await self.db.flush()
        response = AgentReviewVerdictResponse(
            review_assignment=self.assignment_response(assignment),
            task=self.task_service.task_to_response(task),
            rework_assignment=self.assignment_response(rework) if rework else None,
        )
        await self.task_service.record_task_event(
            task.id,
            "agent.verification_verdict",
            {
                "assignment_id": assignment.id,
                "verdict": data.verdict,
                "reason": data.reason,
                "evidence": data.evidence,
                "rework_assignment_id": rework.id if rework else None,
                "task_version": task.version,
                "rationale": command.rationale,
            },
            actor_type="agent",
            actor_id=actor.id,
            correlation_id=command.correlation_id,
            idempotency_key=idempotency_key,
        )
        await self._record_idempotency(
            actor,
            "verification.verdict",
            "assignment",
            assignment.id,
            idempotency_key,
            request_payload,
            {"response": response.model_dump(mode="json")},
        )
        await self.db.commit()
        return response

    async def list_my_claims(self, actor: AgentActor) -> list[dict[str, Any]]:
        """Return current claims owned by an actor."""
        self._require_any_scope(actor, "assignments:read", "tasks:read")
        result = await self.db.execute(
            select(Task).where(Task.claimed_by == actor.id).order_by(Task.id)
        )
        return [
            {
                "task_id": task.id,
                "claim_id": task.claim_id,
                "claim_generation": task.claim_generation,
                "claim_expires_at": task.claim_expires_at,
                "version": task.version,
            }
            for task in result.scalars().all()
        ]

    async def list_my_runs(self, actor: AgentActor, *, limit: int = 50) -> list[AgentRunResponse]:
        """Return recent runs owned by an actor."""
        self._require_any_scope(actor, "assignments:read", "runs:write")
        result = await self.db.execute(
            select(AgentRun)
            .where(AgentRun.actor_id == actor.id)
            .order_by(AgentRun.started_at.desc(), AgentRun.id.desc())
            .limit(limit)
        )
        return [self.run_response(run) for run in result.scalars().all()]

    async def list_recovery_tasks(
        self,
        actor: AgentActor,
        *,
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> AgentRecoveryListResponse:
        """Return typed active/resolved recovery diagnoses and ownership tuples."""
        self._require_any_scope(actor, "recovery:read")
        self._validate_page_limit(limit)
        now = utc_now()
        latest_lifecycle_type = (
            select(TaskEvent.event_type)
            .where(
                TaskEvent.task_id == Task.id,
                TaskEvent.event_type.in_(RECOVERY_LIFECYCLE_EVENT_TYPES),
            )
            .order_by(TaskEvent.created_at.desc(), TaskEvent.id.desc())
            .limit(1)
            .correlate(Task)
            .scalar_subquery()
        )
        has_live_execution_assignment = (
            select(AgentTaskAssignment.id)
            .where(
                AgentTaskAssignment.task_id == Task.id,
                AgentTaskAssignment.purpose == "execution",
                AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES),
            )
            .correlate(Task)
            .exists()
        )
        has_running_run = (
            select(AgentRun.id)
            .where(
                AgentRun.task_id == Task.id,
                AgentRun.status == "running",
            )
            .correlate(Task)
            .exists()
        )
        result = await self.db.execute(
            select(Task)
            .where(
                Task.status.in_((TaskStatus.ACTIVE.value, TaskStatus.RESOLVED.value)),
                or_(
                    Task.claimed_by.is_not(None),
                    has_live_execution_assignment,
                    has_running_run,
                    latest_lifecycle_type.in_(tuple(PENDING_RECOVERY_SIGNAL_TYPES)),
                ),
            )
            .order_by(Task.priority, Task.id)
        )
        tasks = list(result.scalars().all())
        task_ids = [task.id for task in tasks]

        assignments_by_task: dict[int, list[AgentTaskAssignment]] = {}
        running_by_task: dict[int, list[AgentRun]] = {}
        recent_runs_by_task: dict[int, list[AgentRun]] = {}
        actors_by_id: dict[int, AgentActor] = {}
        latest_events_by_task: dict[int, str] = {}
        if task_ids:
            assignment_result = await self.db.execute(
                select(AgentTaskAssignment)
                .where(
                    AgentTaskAssignment.task_id.in_(task_ids),
                    AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES),
                )
                .order_by(AgentTaskAssignment.task_id, AgentTaskAssignment.id)
            )
            for assignment in assignment_result.scalars().all():
                assignments_by_task.setdefault(assignment.task_id, []).append(
                    assignment
                )

            claim_actor_ids = sorted(
                {
                    int(task.claimed_by)
                    for task in tasks
                    if task.claimed_by is not None
                }
            )
            if claim_actor_ids:
                actor_result = await self.db.execute(
                    select(AgentActor).where(AgentActor.id.in_(claim_actor_ids))
                )
                actors_by_id = {
                    claim_actor.id: claim_actor
                    for claim_actor in actor_result.scalars().all()
                }

            running_result = await self.db.execute(
                select(AgentRun)
                .where(
                    AgentRun.task_id.in_(task_ids),
                    AgentRun.status == "running",
                )
                .order_by(AgentRun.task_id, AgentRun.id)
            )
            for run in running_result.scalars().all():
                running_by_task.setdefault(run.task_id, []).append(run)

            ranked_runs = (
                select(
                    AgentRun.id.label("run_id"),
                    func.row_number()
                    .over(
                        partition_by=AgentRun.task_id,
                        order_by=[
                            AgentRun.started_at.desc(),
                            AgentRun.id.desc(),
                        ],
                    )
                    .label("run_rank"),
                )
                .where(AgentRun.task_id.in_(task_ids))
                .subquery()
            )
            recent_result = await self.db.execute(
                select(AgentRun)
                .join(ranked_runs, AgentRun.id == ranked_runs.c.run_id)
                .where(ranked_runs.c.run_rank <= 10)
                .order_by(
                    AgentRun.task_id,
                    AgentRun.started_at.desc(),
                    AgentRun.id.desc(),
                )
            )
            for run in recent_result.scalars().all():
                recent_runs_by_task.setdefault(run.task_id, []).append(run)

            ranked_events = (
                select(
                    TaskEvent.task_id.label("task_id"),
                    TaskEvent.event_type.label("event_type"),
                    func.row_number()
                    .over(
                        partition_by=TaskEvent.task_id,
                        order_by=[
                            TaskEvent.created_at.desc(),
                            TaskEvent.id.desc(),
                        ],
                    )
                    .label("event_rank"),
                )
                .where(
                    TaskEvent.task_id.in_(task_ids),
                    TaskEvent.event_type.in_(RECOVERY_LIFECYCLE_EVENT_TYPES),
                )
                .subquery()
            )
            latest_event_result = await self.db.execute(
                select(ranked_events.c.task_id, ranked_events.c.event_type).where(
                    ranked_events.c.event_rank == 1
                )
            )
            latest_events_by_task = {
                int(row.task_id): str(row.event_type)
                for row in latest_event_result.all()
            }

        recovery: list[AgentRecoveryItem] = []
        for task in tasks:
            live_assignments = assignments_by_task.get(task.id, [])
            execution_assignments = [
                item for item in live_assignments if item.purpose == "execution"
            ]
            accepted = [
                item for item in execution_assignments if item.state == "accepted"
            ]
            queued = [
                item for item in execution_assignments if item.state == "queued"
            ]
            claim_actor = actors_by_id.get(task.claimed_by)
            claim_actor_compatible = False
            if claim_actor is not None:
                try:
                    self._validate_assignment_actor(claim_actor, "execution")
                except ValueError:
                    logger.warning(
                        "Recovery scan found a claim owned by an incompatible actor",
                        extra={"task_id": task.id, "actor_id": claim_actor.id},
                        exc_info=True,
                    )
                else:
                    claim_actor_compatible = True
            live_claim = (
                task.claimed_by is not None
                and task.claim_id is not None
                and task.claim_expires_at is not None
                and as_utc(task.claim_expires_at) > as_utc(now)
                and claim_actor_compatible
            )
            running = running_by_task.get(task.id, [])
            recent_runs = recent_runs_by_task.get(task.id, [])
            pending_recovery_signal = (
                latest_events_by_task.get(task.id)
                in PENDING_RECOVERY_SIGNAL_TYPES
            )
            if (
                not execution_assignments
                and not running
                and task.claimed_by is None
                and not pending_recovery_signal
            ):
                continue
            if task.status == TaskStatus.RESOLVED.value:
                inconsistent = bool(running or execution_assignments or live_claim)
            elif queued and not accepted and not running and not live_claim:
                inconsistent = False
            else:
                consistent_current = (
                    len(accepted) == 1
                    and len(running) == 1
                    and live_claim
                    and accepted[0].actor_id == task.claimed_by
                    and running[0].actor_id == task.claimed_by
                    and running[0].assignment_id == accepted[0].id
                    and running[0].task_id == accepted[0].task_id == task.id
                    and running[0].claim_generation == task.claim_generation
                    and accepted[0].task_version == task.version
                )
                inconsistent = not consistent_current
            if inconsistent:
                codes: list[str] = []
                if task.status == TaskStatus.RESOLVED.value:
                    codes.append("resolved_execution_inconsistent")
                else:
                    codes.append("active_execution_inconsistent")
                if len(execution_assignments) > 1:
                    codes.append("multiple_live_execution_assignments")
                if any(
                    item.purpose == "verification" for item in live_assignments
                ):
                    codes.append("live_verification_assignment_present")
                if len(running) > 1:
                    codes.append("multiple_running_runs")
                if running and not accepted:
                    codes.append("running_run_without_accepted_assignment")
                if accepted and not running:
                    codes.append("accepted_assignment_without_running_run")
                if any(
                    run.assignment_id == assignment.id
                    and run.task_id != assignment.task_id
                    for run in running
                    for assignment in accepted
                ):
                    codes.append("run_task_assignment_mismatch")
                if (accepted or running or task.claimed_by is not None) and not live_claim:
                    codes.append("claim_missing_expired_or_unauthorized")
                if claim_actor is not None and not claim_actor_compatible:
                    codes.append("claim_actor_execution_authority_revoked")
                if any(
                    run.claim_generation != task.claim_generation for run in running
                ):
                    codes.append("run_claim_generation_mismatch")
                if any(
                    assignment.task_version != task.version
                    for assignment in accepted
                ):
                    codes.append("assignment_task_version_stale")
                if (
                    not execution_assignments
                    and not running
                    and task.claimed_by is None
                ):
                    codes.append("pending_recovery_signal")
                recovery.append(
                    AgentRecoveryItem(
                        task=self.task_service.task_to_response(task),
                        recovery_codes=sorted(set(codes)),
                        live_assignments=[
                            self.assignment_response(item) for item in live_assignments
                        ],
                        recent_runs=[self.run_response(run) for run in recent_runs],
                        running_run_ids=sorted(run.id for run in running),
                        claim_actor_id=task.claimed_by,
                        claim_present=task.claim_id is not None,
                        claim_generation=task.claim_generation,
                        claim_expires_at=task.claim_expires_at,
                        server_time=now,
                    )
                )
        page, pagination = self._paginate_single_collection(
            kind="recovery",
            actor_id=actor.id,
            queue_revision=None,
            items=recovery,
            records=[self._recovery_snapshot_record(item) for item in recovery],
            limit=limit,
            cursor=cursor,
            key=self._recovery_item_key,
        )
        return AgentRecoveryListResponse(items=page, pagination=pagination)

    async def requeue_recovery(
        self,
        principal: AgentActor,
        task_id: int,
        data: AgentRecoveryRequeue,
        *,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> AgentRecoveryRequeueResponse:
        """Cancel stale ownership and create one ordered recovery assignment."""
        self._require_any_scope(principal, "recovery:write")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        assert idempotency_key is not None
        task = await self._lock_task(task_id)
        command, request_payload = self._audited_command_request(
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
        replay = await self._idempotent_replay(
            principal,
            "recovery.requeue",
            "task",
            task_id,
            idempotency_key,
            request_payload,
        )
        if replay:
            snapshot = replay.get("response")
            if snapshot is not None:
                return AgentRecoveryRequeueResponse.model_validate(snapshot)
            raise AgentConflictError("Idempotent recovery receipt is unavailable")
        if task is None:
            raise ValueError("Task not found")
        if task.status not in {
            TaskStatus.ACTIVE.value,
            TaskStatus.RESOLVED.value,
        }:
            raise AgentConflictError(
                "Recovery requeue requires an active or inconsistent resolved task"
            )
        if task.version != data.expected_task_version:
            raise TaskVersionConflictError(
                data.expected_task_version,
                self.task_service._metadata_from_task(task),
            )
        owner_result = await self.db.execute(
            select(AgentTaskAssignment.actor_id).where(
                AgentTaskAssignment.task_id == task.id,
                AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES),
            )
        )
        actor_ids = {data.actor_id, *owner_result.scalars().all()}
        if task.claimed_by is not None:
            actor_ids.add(task.claimed_by)
        locked_actors = await self._lock_actors(actor_ids)
        target = locked_actors.get(data.actor_id)
        if target is None:
            raise ValueError("Recovery actor must be an enabled worker or PM")
        self._validate_assignment_actor(target, "execution")

        live_assignments = await self._lock_task_assignments(
            task.id,
            states=LIVE_ASSIGNMENT_STATES,
        )
        if any(item.actor_id not in locked_actors for item in live_assignments):
            raise AgentConflictError(
                "Recovery ownership changed while acquiring canonical row locks"
            )
        stale_assignments = [
            item for item in live_assignments if item.purpose == "execution"
        ]
        live_verification_assignments = [
            item for item in live_assignments if item.purpose == "verification"
        ]
        accepted_assignments = [
            item for item in stale_assignments if item.state == "accepted"
        ]
        queued_assignments = [item for item in stale_assignments if item.state == "queued"]

        stale_runs = await self._lock_task_runs(task.id, status="running")
        now = utc_now()
        if sorted(item.id for item in live_assignments) != sorted(
            data.expected_live_assignment_ids
        ):
            raise AgentConflictError(
                "Recovery assignment ownership changed; refetch typed recovery state"
            )
        if sorted(run.id for run in stale_runs) != sorted(
            data.expected_running_run_ids
        ):
            raise AgentConflictError(
                "Recovery run ownership changed; refetch typed recovery state"
            )
        if task.claim_generation != data.expected_claim_generation:
            raise AgentConflictError(
                "Recovery claim generation changed; refetch typed recovery state"
            )
        if live_verification_assignments:
            raise AgentConflictError(
                "Recovery cannot cancel live verification ownership; "
                "PM must cancel or complete verification separately"
            )
        if (
            not stale_assignments
            and not stale_runs
            and task.claimed_by is None
            and not await self._has_pending_recovery_signal(task.id)
        ):
            raise AgentConflictError(
                "Task has no agent execution ownership or history to recover"
            )
        claim_actor = locked_actors.get(task.claimed_by) if task.claimed_by else None
        claim_actor_compatible = False
        if claim_actor is not None:
            try:
                self._validate_assignment_actor(claim_actor, "execution")
            except ValueError:
                logger.warning(
                    "Recovery command found a claim owned by an incompatible actor",
                    extra={"task_id": task.id, "actor_id": claim_actor.id},
                    exc_info=True,
                )
            else:
                claim_actor_compatible = True
        live_claim = (
            task.claimed_by is not None
            and task.claim_id is not None
            and task.claim_expires_at is not None
            and as_utc(task.claim_expires_at) > as_utc(now)
            and claim_actor_compatible
        )
        healthy_execution = (
            task.status == TaskStatus.ACTIVE.value
            and len(accepted_assignments) == 1
            and len(stale_runs) == 1
            and live_claim
            and accepted_assignments[0].actor_id == task.claimed_by
            and stale_runs[0].actor_id == task.claimed_by
            and stale_runs[0].assignment_id == accepted_assignments[0].id
            and stale_runs[0].claim_generation == task.claim_generation
            and accepted_assignments[0].task_version == task.version
        )
        if healthy_execution:
            raise AgentConflictError(
                "Recovery cannot cancel a healthy accepted assignment, claim, and run"
            )
        if (
            task.status == TaskStatus.ACTIVE.value
            and queued_assignments
            and not accepted_assignments
            and not stale_runs
            and not live_claim
        ):
            raise AgentConflictError(
                "Task already has queued rework or recovery ownership"
            )
        if (
            task.status == TaskStatus.RESOLVED.value
            and not stale_assignments
            and not stale_runs
            and not live_claim
        ):
            raise AgentConflictError(
                "Resolved task has no inconsistent execution ownership to recover"
            )

        cancelled_assignment_ids: list[int] = []
        for assignment in stale_assignments:
            assignment.state = "cancelled"
            assignment.reason = f"Superseded by recovery: {data.reason}"
            cancelled_assignment_ids.append(assignment.id)
            owner = locked_actors.get(assignment.actor_id)
            if owner is not None:
                owner.queue_revision += 1

        for run in stale_runs:
            run.status = "canceled"
            run.ended_at = now
            run.heartbeat_at = now
            run.error = f"Reconciled by PM recovery: {data.reason}"

        if task.status == TaskStatus.RESOLVED.value:
            task, _, _ = await self.task_service.change_status(
                task.id,
                TaskStatus.ACTIVE,
                reason=f"PM recovery reopened inconsistent resolved work: {data.reason}",
                actor_type="agent",
                actor_id=principal.id,
                correlation_id=command.correlation_id,
                expected_version=task.version,
                idempotency_key=idempotency_key,
                commit=False,
            )
            if task is None:
                raise AgentConflictError("Resolved recovery transition failed")
        else:
            await self.task_service.reserve_task_version(task, task.version)
        task.claimed_by = None
        task.claim_expires_at = None
        task.claim_id = None
        recovery_assignment = AgentTaskAssignment(
            task_id=task.id,
            actor_id=target.id,
            team_member_id=task.assignee_id,
            purpose="execution",
            queue_class="recovery",
            state="queued",
            queue_rank=data.queue_rank,
            assigned_by_actor_id=principal.id,
            task_version=task.version,
            routing_snapshot="{}",
            reason=data.reason,
        )
        self.db.add(recovery_assignment)
        target.queue_revision += 1
        await self.db.flush()
        response_ids = {
            "task_id": task.id,
            "assignment_id": recovery_assignment.id,
            "cancelled_assignment_ids": cancelled_assignment_ids,
            "cancelled_run_ids": [run.id for run in stale_runs],
        }
        response = AgentRecoveryRequeueResponse(
            task=self.task_service.task_to_response(task),
            assignment=self.assignment_response(recovery_assignment),
            cancelled_assignment_ids=cancelled_assignment_ids,
            cancelled_run_ids=[run.id for run in stale_runs],
        )
        await self.task_service.record_task_event(
            task.id,
            "agent.recovery_requeued",
            {
                **response_ids,
                "actor_id": target.id,
                "task_version": task.version,
                "reason": data.reason,
                "rationale": command.rationale,
            },
            actor_type="agent",
            actor_id=principal.id,
            correlation_id=command.correlation_id,
            idempotency_key=idempotency_key,
        )
        await self._record_idempotency(
            principal,
            "recovery.requeue",
            "task",
            task.id,
            idempotency_key,
            request_payload,
            {"response": response.model_dump(mode="json")},
        )
        await self.db.commit()
        return response

    async def create_project_update(
        self,
        actor: AgentActor,
        project_id: int,
        data: AgentProjectUpdateCreate,
        *,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> AgentProjectUpdateResponse:
        """Append one evidence-backed project update with agent attribution."""
        self._require_any_scope(actor, "reports:write")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        assert idempotency_key is not None
        if self.db.get_bind().dialect.name == "sqlite":
            await self.db.execute(
                text("UPDATE projects SET id = id WHERE id = :project_id"),
                {"project_id": project_id},
            )
        await self.db.execute(
            select(Project.id).where(Project.id == project_id).with_for_update()
        )
        command, request_payload = self._audited_command_request(
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
        if (
            data.correlation_id is not None
            and data.correlation_id != command.correlation_id
        ):
            raise ValueError(
                "Project update body correlation_id must match X-Correlation-ID"
            )
        replay = await self._idempotent_replay(
            actor,
            "project_update.create",
            "project",
            project_id,
            idempotency_key,
            request_payload,
        )
        if replay:
            snapshot = replay.get("response")
            if snapshot is not None:
                return AgentProjectUpdateResponse.model_validate(snapshot)
            raise AgentConflictError("Idempotent project update receipt is unavailable")
        project = await self.db.get(Project, project_id)
        if project is None:
            raise ValueError("Project not found")
        entry = await ProjectService(self.db).create_project_update(
            project_id,
            ProjectUpdateEntryCreate(
                health=data.health,
                summary=data.summary,
                progress_text=data.progress_text,
                risks_text=data.risks_text,
                decisions_text=data.decisions_text,
                next_steps_text=data.next_steps_text,
            ),
            None,
            created_by_actor_id=actor.id,
            evidence_json={
                **data.evidence,
                "_agent_audit": {"rationale": command.rationale},
            },
            correlation_id=command.correlation_id,
            idempotency_key=idempotency_key,
            commit=False,
        )
        if entry is None:
            raise ValueError("Project not found")
        response = AgentProjectUpdateResponse.model_validate(entry)
        await self._record_idempotency(
            actor,
            "project_update.create",
            "project",
            project_id,
            idempotency_key,
            request_payload,
            {"response": response.model_dump(mode="json")},
        )
        await self.db.commit()
        return response

    async def report_discovery(
        self,
        actor: AgentActor,
        data: AgentDiscoveryTriageCreate,
        *,
        idempotency_key: str,
    ) -> AgentDiscoveryTriageResponse:
        """Create one claim-bound discovery Triage item without expanding scope."""
        self._require_any_scope(actor, "triage:write")
        idempotency_key = validate_idempotency_key(idempotency_key, required=True)
        hint = await self._assignment_lock_hint(data.assignment_id)
        if hint is None or hint[1] != actor.id or hint[0] != data.task_id:
            raise AgentPermissionError("Discovery requires this actor's accepted assignment")
        task = await self._lock_task(data.task_id)
        current_hint = await self._assignment_lock_hint(data.assignment_id)
        if (
            task is None
            or current_hint is None
            or current_hint[0] != task.id
            or current_hint[1] != actor.id
        ):
            raise AgentPermissionError("Discovery requires this actor's accepted assignment")
        actor = (await self._lock_actors((actor.id,))).get(actor.id)
        if actor is None:
            raise AgentPermissionError("Discovery assignment actor is missing")
        self._require_any_scope(actor, "triage:write")
        task_assignments = await self._lock_task_assignments(task.id)
        assignment = next(
            (item for item in task_assignments if item.id == data.assignment_id),
            None,
        )
        if (
            assignment is None
            or assignment.actor_id != actor.id
            or assignment.task_id != data.task_id
            or assignment.purpose != "execution"
            or assignment.state != "accepted"
        ):
            raise AgentPermissionError("Discovery requires this actor's accepted assignment")
        request_payload = data.model_dump(mode="json")
        replay = await self._idempotent_replay(
            actor,
            "discovery.report",
            "assignment",
            assignment.id,
            idempotency_key,
            request_payload,
        )
        if replay:
            snapshot = replay.get("response")
            if snapshot is not None:
                return AgentDiscoveryTriageResponse.model_validate(snapshot)
            raise AgentConflictError("Idempotent discovery receipt is unavailable")
        try:
            self._validate_assignment_actor(actor, "execution")
        except ValueError as exc:
            raise AgentConflictError(
                "Assignment actor is no longer eligible for execution"
            ) from exc
        runs = await self._lock_task_runs(task.id, run_ids=(data.run_id,))
        run = runs[0] if runs else None
        if (
            run is None
            or run.assignment_id != assignment.id
            or run.actor_id != actor.id
            or run.status != "running"
        ):
            raise AgentConflictError("Discovery requires the assignment's running run")
        if assignment.task_version != task.version:
            raise AgentConflictError(
                "Assignment scope changed during execution; recovery and redispatch are required"
            )
        self._validate_fence(task, actor, data.claim_id, data.claim_generation)
        if task.version != data.expected_task_version:
            raise TaskVersionConflictError(
                data.expected_task_version,
                self.task_service._metadata_from_task(task),
            )
        labels = list(dict.fromkeys(["agent-discovery", *data.suggested_labels]))
        item = await TriageService(self.db).create(
            TriageItemCreate(
                title=data.title,
                description=data.description,
                source="agent-discovery",
                priority_hint=data.priority_hint,
                project_hint_id=task.project_id,
                iteration_hint_id=task.iteration_id,
                labels=labels,
                metadata_json={
                    "source_task_id": task.id,
                    "source_assignment_id": assignment.id,
                    "source_run_id": run.id,
                    "source_actor_id": actor.id,
                    "blocking": data.blocking,
                    "evidence": data.evidence,
                },
            ),
            commit=False,
        )
        response = AgentDiscoveryTriageResponse.model_validate(item)
        await self.task_service.record_task_event(
            task.id,
            "agent.discovery_reported",
            {
                "triage_item_id": item.id,
                "assignment_id": assignment.id,
                "run_id": run.id,
                "blocking": data.blocking,
            },
            actor_type="agent",
            actor_id=actor.id,
            idempotency_key=idempotency_key,
        )
        await self._record_idempotency(
            actor,
            "discovery.report",
            "assignment",
            assignment.id,
            idempotency_key,
            request_payload,
            {"response": response.model_dump(mode="json")},
        )
        await self.db.commit()
        return response

    def _definition_blockers(self, task: Task) -> list[str]:
        brief = parse_task_brief(task.description)
        blockers: list[str] = []
        if task.status != TaskStatus.PLANNED.value or task.is_deferred:
            blockers.append("definition_status")
        if task.children:
            blockers.append("composite_task")
        tags = set(_json_loads(task.tags, []))
        if "agent" not in tags or not any(tag.startswith("cap:") for tag in tags):
            blockers.append("agent_capability_labels")
        for section in REQUIRED_BRIEF_SECTIONS:
            if not brief.get(section):
                blockers.append(f"brief_{section.replace(' ', '_')}")
        open_questions = brief.get("open questions", "").strip().lower()
        if open_questions and open_questions not in {"none", "- none", "n/a", "- n/a"}:
            blockers.append("brief_open_questions_unresolved")
        if task.effort_days <= 0 or not 1 <= task.priority <= 10:
            blockers.append("effort_priority")
        return blockers

    async def _start_blockers(
        self,
        task: Task,
        assignment: Optional[AgentTaskAssignment],
        now: datetime,
    ) -> list[str]:
        blockers: list[str] = []
        if assignment is None:
            return ["assignment_missing"]
        if assignment.task_version != task.version:
            blockers.append("assignment_task_version_stale")
        assignment_actor = await self.db.get(AgentActor, assignment.actor_id)
        try:
            if assignment_actor is None:
                raise ValueError("Assignment actor is missing")
            self._validate_assignment_actor(assignment_actor, assignment.purpose)
        except ValueError:
            blockers.append("assignment_actor_ineligible")
        if assignment.purpose != "execution" or assignment.state != "queued":
            blockers.append("assignment_not_queued_execution")
        if assignment.not_before is not None and as_utc(assignment.not_before) > as_utc(now):
            blockers.append("not_before_future")
        expected_status = (
            TaskStatus.PLANNED.value
            if assignment.queue_class == "normal"
            else TaskStatus.ACTIVE.value
        )
        if task.status != expected_status:
            blockers.append(f"task_status_{expected_status}_required")
        if task.is_deferred:
            blockers.append("task_deferred")
        if task.children:
            blockers.append("composite_task")
        if task.start_date is None or task.end_date is None:
            blockers.append("schedule_missing")
        elif assignment.queue_class == "normal" and task.start_date > date.today():
            blockers.append("scheduled_start_future")
        for edge in task.dependencies:
            dependency = edge.depends_on
            if dependency.status not in {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}:
                blockers.append(f"dependency_{dependency.id}_unresolved")
        if task.claimed_by is not None:
            if task.claim_expires_at is None or as_utc(task.claim_expires_at) > as_utc(now):
                blockers.append("foreign_or_unknown_claim")
        brief = parse_task_brief(task.description)
        for section in REQUIRED_BRIEF_SECTIONS:
            if not brief.get(section):
                blockers.append(f"brief_{section.replace(' ', '_')}")
        open_questions = brief.get("open questions", "").strip().lower()
        if open_questions and open_questions not in {"none", "- none", "n/a", "- n/a"}:
            blockers.append("brief_open_questions_unresolved")
        tags = set(_json_loads(task.tags, []))
        if "agent" not in tags or not any(tag.startswith("cap:") for tag in tags):
            blockers.append("agent_capability_labels")
        return sorted(set(blockers))

    async def _work_item(
        self,
        assignment: AgentTaskAssignment,
        position: int,
        now: datetime,
        *,
        running: Optional[Iterable[AgentRun]] = None,
    ) -> AgentWorkItem:
        task = await self.task_service.get_by_id(assignment.task_id)
        if task is None:
            raise AgentConflictError("Assigned task is missing")
        if assignment.purpose == "verification":
            blockers = []
            if assignment.task_version != task.version:
                blockers.append("assignment_task_version_stale")
            verifier = await self.db.get(AgentActor, assignment.actor_id)
            try:
                if verifier is None:
                    raise ValueError("Verification actor is missing")
                self._validate_assignment_actor(verifier, "verification")
            except ValueError:
                blockers.append("assignment_actor_ineligible")
            if task.status != TaskStatus.RESOLVED.value:
                blockers.append("task_status_resolved_required")
            if assignment.not_before is not None and as_utc(assignment.not_before) > as_utc(now):
                blockers.append("not_before_future")
        else:
            if assignment.state == "accepted":
                blockers = []
                if assignment.task_version != task.version:
                    blockers.append("assignment_task_version_stale")
            else:
                blockers = await self._start_blockers(task, assignment, now)
        queue_class_rank = QUEUE_CLASS_RANK.get(assignment.queue_class, 99)
        not_before = assignment.not_before.isoformat() if assignment.not_before else ""
        start_date = task.start_date.isoformat() if task.start_date else ""
        selection_key: list[Any] = [
            queue_class_rank,
            assignment.queue_rank,
            task.priority,
            not_before or start_date,
            task.sort_order,
            task.id,
        ]
        run = next(
            (
                item
                for item in (running or [])
                if item.assignment_id == assignment.id and item.status == "running"
            ),
            None,
        )
        claim = None
        if task.claimed_by is not None:
            claim = {
                "actor_id": task.claimed_by,
                "claim_generation": task.claim_generation,
                "claim_expires_at": task.claim_expires_at,
            }
            if (
                assignment.purpose == "execution"
                and assignment.state == "accepted"
                and task.claimed_by == assignment.actor_id
            ):
                claim["claim_id"] = task.claim_id
        return AgentWorkItem(
            assignment=self.assignment_response(assignment),
            task=self.task_service.task_to_response(task),
            queue_position=position,
            selection_key=selection_key,
            selection_reason=(
                f"{assignment.queue_class} assignment rank {assignment.queue_rank}, "
                f"priority {task.priority}"
            ),
            blocker_codes=blockers,
            claim=claim,
            run=self.run_response(run) if run else None,
        )

    async def _current_recovery_codes(
        self,
        actor: AgentActor,
        accepted: list[AgentTaskAssignment],
        running: list[AgentRun],
        now: datetime,
    ) -> list[str]:
        codes: list[str] = []
        if accepted or running:
            try:
                self._validate_assignment_actor(actor, "execution")
            except ValueError:
                codes.append("actor_execution_authority_revoked")
        if len(accepted) > actor.max_parallel_work:
            codes.append("too_many_accepted_assignments")
        if len(running) > actor.max_parallel_work:
            codes.append("too_many_running_runs")
        if not accepted and running:
            codes.append("running_run_without_accepted_assignment")
        if accepted and not running:
            codes.append("accepted_assignment_without_running_run")
        for assignment in accepted:
            task = await self.task_service.get_by_id(assignment.task_id)
            run = next((item for item in running if item.assignment_id == assignment.id), None)
            if run is None:
                codes.append(f"assignment_{assignment.id}_run_missing")
            elif run.task_id != assignment.task_id:
                codes.append(f"assignment_{assignment.id}_run_task_mismatch")
            if task is None:
                codes.append(f"assignment_{assignment.id}_task_missing")
                continue
            if assignment.task_version != task.version:
                codes.append(f"assignment_{assignment.id}_task_version_stale")
            live_claim = (
                task.claimed_by == actor.id
                and task.claim_id is not None
                and task.claim_expires_at is not None
                and as_utc(task.claim_expires_at) > as_utc(now)
            )
            if not live_claim:
                codes.append(f"assignment_{assignment.id}_claim_invalid")
            if run is not None and run.claim_generation != task.claim_generation:
                codes.append(f"assignment_{assignment.id}_fence_mismatch")
            if task.status != TaskStatus.ACTIVE.value:
                codes.append(f"assignment_{assignment.id}_task_not_active")
        return sorted(set(codes))

    @staticmethod
    def _validate_fence(
        task: Task,
        actor: AgentActor,
        claim_id: str,
        claim_generation: int,
    ) -> None:
        now = utc_now()
        if (
            task.claimed_by != actor.id
            or task.claim_id != claim_id
            or task.claim_generation != claim_generation
            or task.claim_expires_at is None
            or as_utc(task.claim_expires_at) <= as_utc(now)
        ):
            raise AgentConflictError("Claim fence is missing, stale, expired, or owned by another actor")

    async def _idempotent_replay(
        self,
        actor: AgentActor,
        operation: str,
        target_type: str,
        target_id: int,
        idempotency_key: Optional[str],
        request_payload: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        if not idempotency_key or actor.id <= 0:
            return None
        result = await self.db.execute(
            select(AgentIdempotencyRecord).where(
                AgentIdempotencyRecord.actor_id == actor.id,
                AgentIdempotencyRecord.operation == operation,
                AgentIdempotencyRecord.target_type == target_type,
                AgentIdempotencyRecord.target_id == target_id,
                AgentIdempotencyRecord.idempotency_key == idempotency_key,
            )
        )
        record = result.scalar_one_or_none()
        if record is None:
            return None
        request_hash = self._request_hash(request_payload)
        if record.request_hash != request_hash:
            raise AgentConflictError("idempotency_mismatch")
        return _json_loads(record.response_payload, {})

    @staticmethod
    def _live_fence_receipt(response: AgentWorkBeginResponse) -> dict[str, Any]:
        """Store an exact live response without retaining the plaintext claim secret."""
        snapshot = response.model_dump(mode="json")
        claim_id = str(snapshot.pop("claim_id"))
        return {
            "response_without_claim_id": snapshot,
            "claim_sha256": hashlib.sha256(claim_id.encode("utf-8")).hexdigest(),
        }

    async def _replay_live_fence_receipt(
        self,
        actor: AgentActor,
        payload: dict[str, Any],
    ) -> AgentWorkBeginResponse:
        """Replay a fence receipt only while its original authority is still exact."""
        snapshot = payload.get("response_without_claim_id")
        claim_digest = payload.get("claim_sha256")
        if not isinstance(snapshot, dict) or not isinstance(claim_digest, str):
            raise AgentConflictError("Idempotent live-work receipt is unavailable")
        assignment_data = snapshot.get("assignment", {})
        task_data = snapshot.get("task", {})
        run_data = snapshot.get("run", {})
        try:
            assignment_id = int(assignment_data["id"])
            assignment_task_version = int(assignment_data["task_version"])
            task_id = int(task_data["id"])
            task_version = int(task_data["version"])
            run_id = int(run_data["id"])
            claim_generation = int(snapshot["claim_generation"])
            queue_revision = int(snapshot["queue_revision"])
            assignment = await self.db.get(
                AgentTaskAssignment, assignment_id
            )
            task = await self.task_service.get_by_id(task_id)
            run = await self.db.get(AgentRun, run_id)
            expected_expiry = as_utc(
                datetime.fromisoformat(str(snapshot["claim_expires_at"]))
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise AgentConflictError(
                "Idempotent live-work receipt is invalid"
            ) from exc
        current_claim = task.claim_id if task is not None else None
        live_exact = (
            assignment is not None
            and task is not None
            and run is not None
            and assignment.actor_id == actor.id
            and assignment.id == assignment_id
            and assignment.task_id == task.id
            and assignment.state == assignment_data.get("state") == "accepted"
            and assignment.task_version == assignment_task_version
            and task.version == task_version
            and task.claimed_by == actor.id
            and current_claim is not None
            and task.claim_generation == claim_generation
            and task.claim_expires_at is not None
            and as_utc(task.claim_expires_at) == expected_expiry
            and expected_expiry > as_utc(utc_now())
            and run.actor_id == actor.id
            and run.assignment_id == assignment.id
            and run.task_id == task.id
            and run.status == run_data.get("status") == "running"
            and run.claim_generation == task.claim_generation
            and actor.queue_revision == queue_revision
            and secrets.compare_digest(
                hashlib.sha256(current_claim.encode("utf-8")).hexdigest(),
                claim_digest,
            )
        )
        if not live_exact:
            raise AgentConflictError(
                "Idempotent live-work receipt is no longer authoritative; refetch work state"
            )
        replay = dict(snapshot)
        replay["claim_id"] = current_claim
        return AgentWorkBeginResponse.model_validate(replay)

    async def _record_idempotency(
        self,
        actor: AgentActor,
        operation: str,
        target_type: str,
        target_id: int,
        idempotency_key: Optional[str],
        request_payload: dict[str, Any],
        response_payload: dict[str, Any],
    ) -> None:
        if not idempotency_key or actor.id <= 0:
            return
        self.db.add(
            AgentIdempotencyRecord(
                actor_id=actor.id,
                operation=operation,
                target_type=target_type,
                target_id=target_id,
                idempotency_key=idempotency_key,
                request_hash=self._request_hash(request_payload),
                response_payload=json.dumps(response_payload, sort_keys=True),
            )
        )

    @staticmethod
    def _request_hash(payload: dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @staticmethod
    def _snapshot_revision(
        kind: str,
        records: list[dict[str, Any]],
        *,
        queue_revision: Optional[int],
    ) -> str:
        payload = json.dumps(
            {"kind": kind, "records": records},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        )
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
        prefix = f"q{queue_revision}" if queue_revision is not None else "snapshot"
        return f"{prefix}-{digest}"

    @staticmethod
    def _validate_page_limit(limit: int) -> None:
        if not 1 <= limit <= 200:
            raise ValueError("Pagination limit must be between 1 and 200")

    @staticmethod
    def _encode_page_cursor(
        *,
        kind: str,
        actor_id: int,
        queue_revision: Optional[int],
        snapshot_revision: str,
        positions: dict[str, Optional[list[Any]]],
    ) -> str:
        payload = {
            "v": 1,
            "kind": kind,
            "actor_id": actor_id,
            "queue_revision": queue_revision,
            "snapshot_revision": snapshot_revision,
            "positions": positions,
        }
        raw = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        encoded = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
        checksum = hashlib.sha256(b"agent-page-cursor/v1\0" + raw).hexdigest()[:16]
        return f"{encoded}.{checksum}"

    @staticmethod
    def _decode_page_cursor(
        cursor: Optional[str],
        *,
        kind: str,
        actor_id: int,
        queue_revision: Optional[int],
        snapshot_revision: str,
    ) -> dict[str, Optional[list[Any]]]:
        if cursor is None:
            return {}
        if len(cursor) > 4096 or "." not in cursor:
            raise ValueError("Invalid pagination cursor")
        encoded, checksum = cursor.rsplit(".", 1)
        try:
            raw = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
            expected_checksum = hashlib.sha256(
                b"agent-page-cursor/v1\0" + raw
            ).hexdigest()[:16]
            if not secrets.compare_digest(checksum, expected_checksum):
                raise ValueError("cursor checksum")
            payload = json.loads(raw)
        except (
            ValueError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            binascii.Error,
        ) as exc:
            raise ValueError("Invalid pagination cursor") from exc
        if (
            not isinstance(payload, dict)
            or payload.get("v") != 1
            or payload.get("kind") != kind
            or payload.get("actor_id") != actor_id
        ):
            raise ValueError("Invalid pagination cursor")
        if (
            payload.get("queue_revision") != queue_revision
            or payload.get("snapshot_revision") != snapshot_revision
        ):
            raise AgentConflictError("stale_cursor")
        positions = payload.get("positions")
        if not isinstance(positions, dict):
            raise ValueError("Invalid pagination cursor")
        for value in positions.values():
            if value is not None and not isinstance(value, list):
                raise ValueError("Invalid pagination cursor")
        return positions

    @staticmethod
    def _keyset_page(
        items: list[Any],
        *,
        last_key: Optional[list[Any]],
        limit: int,
        key: Callable[[Any], list[Any]],
    ) -> tuple[list[Any], bool, Optional[list[Any]]]:
        keys = [key(item) for item in items]
        start = 0
        if last_key is not None:
            try:
                start = keys.index(last_key) + 1
            except ValueError as exc:
                raise ValueError("Invalid pagination cursor position") from exc
        page = items[start : start + limit]
        has_more = start + len(page) < len(items)
        position = key(page[-1]) if page else last_key
        return page, has_more, position

    @staticmethod
    def _work_item_key(item: AgentWorkItem) -> list[Any]:
        return [*item.selection_key, item.assignment.id]

    @staticmethod
    def _recovery_item_key(item: AgentRecoveryItem) -> list[Any]:
        return [item.task.priority, item.task.id]

    @staticmethod
    def _work_snapshot_record(bucket: str, item: AgentWorkItem) -> dict[str, Any]:
        payload = item.model_dump(mode="json")
        claim = payload.get("claim")
        if isinstance(claim, dict):
            claim.pop("claim_id", None)
        return {"bucket": bucket, "item": payload}

    @staticmethod
    def _recovery_snapshot_record(item: AgentRecoveryItem) -> dict[str, Any]:
        payload = item.model_dump(mode="json")
        payload.pop("server_time", None)
        return payload

    def _paginate_work_collections(
        self,
        *,
        actor_id: int,
        queue_revision: int,
        ready: list[AgentWorkItem],
        blocked: list[AgentWorkItem],
        limit: int,
        cursor: Optional[str],
        extra_records: Optional[list[dict[str, Any]]] = None,
    ) -> tuple[
        list[AgentWorkItem],
        list[AgentWorkItem],
        AgentWorkPaginationMetadata,
    ]:
        records = [
            self._work_snapshot_record("queue", item) for item in ready
        ] + [self._work_snapshot_record("blocked_assigned", item) for item in blocked]
        records.extend(extra_records or [])
        snapshot_revision = self._snapshot_revision(
            "work",
            records,
            queue_revision=queue_revision,
        )
        positions = self._decode_page_cursor(
            cursor,
            kind="work",
            actor_id=actor_id,
            queue_revision=queue_revision,
            snapshot_revision=snapshot_revision,
        )
        ready_page, ready_more, ready_position = self._keyset_page(
            ready,
            last_key=positions.get("queue"),
            limit=limit,
            key=self._work_item_key,
        )
        blocked_page, blocked_more, blocked_position = self._keyset_page(
            blocked,
            last_key=positions.get("blocked_assigned"),
            limit=limit,
            key=self._work_item_key,
        )
        has_more = ready_more or blocked_more
        next_cursor = None
        if has_more:
            next_cursor = self._encode_page_cursor(
                kind="work",
                actor_id=actor_id,
                queue_revision=queue_revision,
                snapshot_revision=snapshot_revision,
                positions={
                    "queue": ready_position,
                    "blocked_assigned": blocked_position,
                },
            )
        pagination = AgentWorkPaginationMetadata(
            snapshot_revision=snapshot_revision,
            page_size=limit,
            returned=len(ready_page) + len(blocked_page),
            has_more=has_more,
            next_cursor=next_cursor,
            queue=AgentCollectionPageMetadata(
                returned=len(ready_page),
                has_more=ready_more,
            ),
            blocked_assigned=AgentCollectionPageMetadata(
                returned=len(blocked_page),
                has_more=blocked_more,
            ),
        )
        return ready_page, blocked_page, pagination

    def _paginate_single_collection(
        self,
        *,
        kind: str,
        actor_id: int,
        queue_revision: Optional[int],
        items: list[Any],
        records: list[dict[str, Any]],
        limit: int,
        cursor: Optional[str],
        key: Callable[[Any], list[Any]],
    ) -> tuple[list[Any], AgentPaginationMetadata]:
        snapshot_revision = self._snapshot_revision(
            kind,
            records,
            queue_revision=queue_revision,
        )
        positions = self._decode_page_cursor(
            cursor,
            kind=kind,
            actor_id=actor_id,
            queue_revision=queue_revision,
            snapshot_revision=snapshot_revision,
        )
        page, has_more, position = self._keyset_page(
            items,
            last_key=positions.get("items"),
            limit=limit,
            key=key,
        )
        next_cursor = None
        if has_more:
            next_cursor = self._encode_page_cursor(
                kind=kind,
                actor_id=actor_id,
                queue_revision=queue_revision,
                snapshot_revision=snapshot_revision,
                positions={"items": position},
            )
        return page, AgentPaginationMetadata(
            snapshot_revision=snapshot_revision,
            page_size=limit,
            returned=len(page),
            has_more=has_more,
            next_cursor=next_cursor,
        )

    async def _read_actor_queue_revision(self, actor_id: int) -> int:
        result = await self.db.execute(
            select(AgentActor.queue_revision).where(AgentActor.id == actor_id)
        )
        revision = result.scalar_one_or_none()
        if revision is None:
            raise AgentPermissionError("Agent actor is missing")
        return int(revision)

    @staticmethod
    def work_etag(
        decision: AgentWorkDecisionResponse,
        *,
        cursor: Optional[str],
        limit: int,
    ) -> str:
        """Build a weak validator for ownership-equivalent work representations."""
        actor_payload = decision.actor.model_dump(mode="json")
        actor_payload.pop("last_seen_at", None)
        payload = json.dumps(
            {
                "actor": actor_payload,
                "queue_revision": decision.queue_revision,
                "snapshot_revision": decision.pagination.snapshot_revision,
                "state": decision.state,
                "recovery_codes": decision.recovery_codes,
                "cursor": cursor,
                "limit": limit,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return f'W/"{digest}"'
