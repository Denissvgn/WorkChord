"""Agent integration services."""
import hashlib
import json
import secrets
from datetime import datetime, timedelta
from typing import Any, Optional, Sequence

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.models.agent import (
    AgentActor,
    AgentIdempotencyRecord,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentRunEvent,
    AgentTaskAssignment,
    TaskEvent,
)
from app.models.label import Label, LabelGroup
from app.models.task import Task, TaskDependency, TaskStatus
from app.models.team_member import TeamMemberProfile
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.schemas.agent import (
    AgentActorCreate,
    AgentRunCreate,
    AgentRunEventCreate,
    AgentRunFinish,
    AgentTaskCreate,
    AgentTaskPatch,
    SUPPORTED_AGENT_SCOPES,
    TaskClaimRequest,
    TaskEventCreate,
)
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.agent_readiness import evaluate_agent_readiness
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.task_service import TaskService
from app.utils.time import as_utc, utc_now


ALL_AGENT_SCOPES = sorted(SUPPORTED_AGENT_SCOPES)
ALLOWED_ASSIGNED_RUN_EVENT_TYPES = {
    "agent.progress",
    "agent.checkpoint",
    "agent.blocker",
}


class AgentConflictError(Exception):
    """Raised when an agent operation conflicts with current task state."""


class AgentPermissionError(Exception):
    """Raised when an agent lacks a required scope."""


def hash_api_key(api_key: str) -> str:
    """Hash an agent API key for storage and lookup."""
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def actor_scopes(actor: AgentActor) -> list[str]:
    """Parse an actor scope list."""
    try:
        scopes = json.loads(actor.scopes) if actor.scopes else []
    except (json.JSONDecodeError, TypeError):
        scopes = []
    return scopes if isinstance(scopes, list) else []


def actor_has_scope(actor: AgentActor, scope: str) -> bool:
    """Return whether an actor has the requested scope."""
    scopes = actor_scopes(actor)
    return "admin" in scopes or scope in scopes


def require_scope(actor: AgentActor, scope: str) -> None:
    """Raise if actor does not have scope."""
    if not actor_has_scope(actor, scope):
        raise AgentPermissionError(f"Missing required scope: {scope}")


def validate_idempotency_key(
    value: Optional[str], *, required: bool = False
) -> Optional[str]:
    """Validate one persistence-safe, log-safe idempotency key."""
    if value is None:
        if required:
            raise ValueError("Idempotency-Key is required")
        return None
    if (
        not value
        or value != value.strip()
        or len(value) > 255
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise ValueError(
            "Idempotency-Key must be 1-255 printable characters without outer whitespace"
        )
    return value


class AgentService:
    """Service for agent authentication, task control, and run tracing."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_service = TaskService(db)

    async def authenticate(self, api_key: str) -> Optional[AgentActor]:
        """Authenticate an API key against stored enabled agent actors."""
        key_hash = hash_api_key(api_key)
        result = await self.db.execute(
            select(AgentActor).where(
                AgentActor.api_key_hash == key_hash,
                AgentActor.enabled.is_(True),
            )
        )
        actor = result.scalar_one_or_none()

        if actor:
            settings = get_settings()
            now = utc_now()
            touch_due = (
                actor.last_seen_at is None
                or now - as_utc(actor.last_seen_at)
                >= timedelta(seconds=settings.agent_last_seen_interval_seconds)
            )
            # Authentication remains a pure read while the deployment write
            # fence is active. In normal operation, throttle this audit field
            # so 200 concurrent MCP clients do not turn every read into a write.
            if settings.maintenance_mode == "off" and touch_due:
                actor.last_seen_at = now
                await self.db.commit()
                await self.db.refresh(actor)

        return actor

    def authenticate_bootstrap_key(self, api_key: str) -> Optional[AgentActor]:
        """Return a transient provisioning actor for the bootstrap API key."""
        configured = get_settings().agent_bootstrap_api_key
        if not configured or not secrets.compare_digest(api_key, configured):
            return None
        return AgentActor(
            id=0,
            name="bootstrap-agent",
            display_name="Bootstrap Agent",
            api_key_hash="bootstrap",
            scopes=json.dumps(ALL_AGENT_SCOPES),
            enabled=True,
            created_at=utc_now(),
        )

    async def create_actor(
        self,
        data: AgentActorCreate,
        *,
        principal: AgentActor | None = None,
    ) -> tuple[AgentActor, str, AgentModelBinding | None]:
        """Create an actor and optional secret-free model binding atomically."""
        if data.profile_id is not None:
            profile = await self.db.get(TeamMemberProfile, data.profile_id)
            if profile is None:
                raise ValueError("Team member profile not found")
        catalog: AgentModelCatalogEntry | None = None
        if data.model_binding is not None:
            result = await self.db.execute(
                select(AgentModelCatalogEntry).where(
                    AgentModelCatalogEntry.key
                    == data.model_binding.model_catalog_key,
                    AgentModelCatalogEntry.enabled.is_(True),
                )
            )
            catalog = result.scalar_one_or_none()
            if catalog is None:
                raise ValueError(
                    "Enabled model catalog entry not found for "
                    f"{data.model_binding.model_catalog_key!r}"
                )
        api_key = f"pmag_{secrets.token_urlsafe(32)}"
        actor = AgentActor(
            name=data.name,
            display_name=data.display_name,
            api_key_hash=hash_api_key(api_key),
            scopes=json.dumps(data.scopes),
            enabled=data.enabled,
            role=data.role,
            profile_id=data.profile_id,
            work_policy=data.work_policy,
            max_parallel_work=data.max_parallel_work,
        )
        self.db.add(actor)
        binding: AgentModelBinding | None = None
        if data.model_binding is not None:
            assert catalog is not None
            await self.db.flush()
            binding = AgentModelBinding(
                actor_id=actor.id,
                model_catalog_id=catalog.id,
                is_default=data.model_binding.is_default,
                enabled=True,
                tool_tags=data.model_binding.tool_tags,
                data_policy_tags=data.model_binding.data_policy_tags,
                revision=1,
            )
            self.db.add(binding)
            await self.db.flush()
            self.db.add(
                TaskEvent(
                    task_id=None,
                    actor_type=(
                        "agent"
                        if principal is not None and principal.id > 0
                        else "bootstrap"
                    ),
                    actor_id=(
                        principal.id
                        if principal is not None and principal.id > 0
                        else None
                    ),
                    event_type="agent.model_configuration_changed",
                    payload=json.dumps(
                        {
                            "operation": "actor.model_binding.create",
                            "target_type": "model_binding",
                            "target_id": binding.id,
                            "actor_id": actor.id,
                            "model_catalog_key": (
                                data.model_binding.model_catalog_key
                            ),
                            "authoritative_revision": binding.revision,
                            "invalidated_assignment_ids": [],
                        },
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                )
            )
        await self.db.commit()
        await self.db.refresh(actor)
        if binding is not None:
            await self.db.refresh(binding)
        return actor, api_key, binding

    async def list_ready_tasks(
        self,
        actor: AgentActor,
        iteration_id: Optional[int] = None,
        tags: Optional[list[str]] = None,
        priority_min: Optional[int] = None,
        priority_max: Optional[int] = None,
        assignee_id: Optional[int] = None,
        capabilities: Optional[list[str]] = None,
        limit: int = 50,
    ) -> list[Task]:
        """Return claimable tasks with dependencies satisfied."""
        require_scope(actor, "tasks:read")
        now = utc_now()

        query = (
            select(Task)
            .options(
                selectinload(Task.dependencies).selectinload(TaskDependency.depends_on),
                selectinload(Task.assignee),
                selectinload(Task.claimed_agent),
                selectinload(Task.children),
            )
            .where(
                Task.status == TaskStatus.PLANNED.value,
                Task.is_deferred.is_(False),
            )
            .order_by(Task.priority, Task.sort_order, Task.id)
            .limit(limit * 3)
        )
        if iteration_id is not None:
            query = query.where(Task.iteration_id == iteration_id)
        if priority_min is not None:
            query = query.where(Task.priority >= priority_min)
        if priority_max is not None:
            query = query.where(Task.priority <= priority_max)
        if assignee_id is not None:
            query = query.where(Task.assignee_id == assignee_id)

        result = await self.db.execute(query)
        candidates = result.scalars().all()
        active_capability_slugs = await self._active_capability_slugs()

        ready: list[Task] = []
        required_tags = set(tags or [])
        required_capabilities = set(capabilities or [])
        for task in candidates:
            task_tags = self._parse_tags(task.tags)
            if required_tags and not required_tags.issubset(task_tags):
                continue
            if required_capabilities and not required_capabilities.intersection(task_tags):
                continue
            readiness = evaluate_agent_readiness(
                task,
                tags=task_tags,
                children=task.children,
                dependencies=task.dependencies,
                now=now,
                current_actor_id=actor.id,
                capability_slugs=active_capability_slugs,
            )
            if not readiness.is_ready:
                continue
            ready.append(task)
            if len(ready) >= limit:
                break

        return ready

    async def _active_capability_slugs(self) -> Optional[set[str]]:
        """Return active capability label slugs, falling back when taxonomy is absent."""
        group_result = await self.db.execute(
            select(LabelGroup).where(LabelGroup.key == "capability")
        )
        group = group_result.scalar_one_or_none()
        if group is None:
            return None
        if not group.is_active:
            return set()

        label_result = await self.db.execute(
            select(Label.slug).where(
                Label.group_id == group.id,
                Label.is_active.is_(True),
            )
        )
        return set(label_result.scalars().all())

    def _parse_tags(self, tags_value: Optional[str]) -> set[str]:
        try:
            tags = json.loads(tags_value) if tags_value else []
        except (json.JSONDecodeError, TypeError):
            tags = []
        return set(tags if isinstance(tags, list) else [])

    async def claim_task(
        self,
        task_id: int,
        actor: AgentActor,
        data: TaskClaimRequest,
        idempotency_key: Optional[str] = None,
    ) -> Optional[Task]:
        """Claim a task lease for an agent."""
        idempotency_key = validate_idempotency_key(idempotency_key)
        if "work:execute" in actor_scopes(actor):
            raise AgentPermissionError(
                "Assigned-work actors must use the atomic work begin command"
            )
        require_scope(actor, "tasks:write")
        existing = await self._task_from_idempotency(actor, "task_claimed", idempotency_key)
        if existing:
            return existing

        await self.db.execute(select(Task.id).where(Task.id == task_id).with_for_update())
        task = await self.task_service.get_by_id(task_id)
        if not task:
            return None

        now = utc_now()
        readiness = evaluate_agent_readiness(
            task,
            tags=self._parse_tags(task.tags),
            children=task.children,
            dependencies=task.dependencies,
            now=now,
            current_actor_id=actor.id,
            capability_slugs=await self._active_capability_slugs(),
        )
        if not readiness.start_ready:
            raise AgentConflictError(
                "Task is not ready to claim: " + ", ".join(readiness.blocker_codes)
            )
        assignment_result = await self.db.execute(
            select(AgentTaskAssignment).where(
                AgentTaskAssignment.task_id == task_id,
                AgentTaskAssignment.purpose == "execution",
                AgentTaskAssignment.state.in_(("queued", "accepted")),
            )
        )
        assignment = assignment_result.scalars().first()
        if assignment is not None and assignment.actor_id != actor.id:
            raise AgentConflictError("Task is assigned to another actor.")
        if task.claimed_by and task.claimed_by != actor.id:
            if task.claim_expires_at and as_utc(task.claim_expires_at) > now:
                raise AgentConflictError("Task is already claimed by another agent.")

        task.claimed_by = actor.id
        task.claimed_agent = actor
        task.claim_generation += 1
        task.claim_id = secrets.token_hex(24)
        claim_expires_at = now + timedelta(seconds=data.lease_seconds)
        task.claim_expires_at = claim_expires_at
        task.version += 1
        await self.task_service.record_task_event(
            task_id,
            "task_claimed",
            {
                "claim_expires_at": claim_expires_at.isoformat(),
                "claim_generation": task.claim_generation,
                "version": task.version,
            },
            actor_type="agent",
            actor_id=actor.id,
            trace_id=data.trace_id,
            span_id=data.span_id,
            correlation_id=data.correlation_id,
            idempotency_key=idempotency_key,
        )
        await emit_outbound_webhook_event(
            self.db,
            commit=False,
            event_type="task.claimed",
            entity_type="task",
            entity_id=task_id,
            data={
                "task_id": task_id,
                "actor_id": actor.id,
                "claim_expires_at": claim_expires_at.isoformat(),
                "version": task.version,
            },
        )
        await self.db.commit()
        return await self.task_service.get_by_id(task_id)

    async def renew_claim(
        self,
        task_id: int,
        actor: AgentActor,
        data: TaskClaimRequest,
        idempotency_key: Optional[str] = None,
    ) -> Optional[Task]:
        """Renew a task lease."""
        idempotency_key = validate_idempotency_key(idempotency_key)
        if "work:execute" in actor_scopes(actor):
            raise AgentPermissionError(
                "Assigned-work actors must use the atomic work renew command"
            )
        require_scope(actor, "tasks:write")
        existing = await self._task_from_idempotency(actor, "task_claim_renewed", idempotency_key)
        if existing:
            return existing

        task = await self.task_service.get_by_id(task_id)
        if not task:
            return None
        if task.claimed_by != actor.id and not actor_has_scope(actor, "admin"):
            raise AgentConflictError("Only the claiming agent can renew this task.")
        if data.claim_id is not None and task.claim_id != data.claim_id:
            raise AgentConflictError("Claim fence does not match the current claim.")
        if (
            data.claim_generation is not None
            and task.claim_generation != data.claim_generation
        ):
            raise AgentConflictError("Claim generation is stale.")

        task.claimed_by = actor.id
        task.claimed_agent = actor
        claim_expires_at = utc_now() + timedelta(seconds=data.lease_seconds)
        task.claim_expires_at = claim_expires_at
        task.version += 1
        await self.task_service.record_task_event(
            task_id,
            "task_claim_renewed",
            {"claim_expires_at": claim_expires_at.isoformat(), "version": task.version},
            actor_type="agent",
            actor_id=actor.id,
            trace_id=data.trace_id,
            span_id=data.span_id,
            correlation_id=data.correlation_id,
            idempotency_key=idempotency_key,
        )
        await emit_outbound_webhook_event(
            self.db,
            commit=False,
            event_type="agent.claim_renewed",
            entity_type="task",
            entity_id=task_id,
            data={
                "task_id": task_id,
                "actor_id": actor.id,
                "claim_expires_at": claim_expires_at.isoformat(),
                "version": task.version,
            },
        )
        await self.db.commit()
        return await self.task_service.get_by_id(task_id)

    async def release_claim(
        self,
        task_id: int,
        actor: AgentActor,
        idempotency_key: Optional[str] = None,
    ) -> Optional[Task]:
        """Release a task lease."""
        idempotency_key = validate_idempotency_key(idempotency_key)
        if "work:execute" in actor_scopes(actor):
            raise AgentPermissionError(
                "Assigned-work actors cannot use the legacy unfenced release command"
            )
        require_scope(actor, "tasks:write")
        existing = await self._task_from_idempotency(actor, "task_claim_released", idempotency_key)
        if existing:
            return existing

        task = await self.task_service.get_by_id(task_id)
        if not task:
            return None
        if task.claimed_by != actor.id and not actor_has_scope(actor, "admin"):
            raise AgentConflictError("Only the claiming agent can release this task.")

        task.claimed_by = None
        task.claim_expires_at = None
        task.claim_id = None
        task.version += 1
        await self.task_service.record_task_event(
            task_id,
            "task_claim_released",
            {"version": task.version},
            actor_type="agent",
            actor_id=actor.id,
            idempotency_key=idempotency_key,
        )
        await emit_outbound_webhook_event(
            self.db,
            commit=False,
            event_type="agent.claim_released",
            entity_type="task",
            entity_id=task_id,
            data={
                "task_id": task_id,
                "actor_id": actor.id,
                "version": task.version,
            },
        )
        await self.db.commit()
        return await self.task_service.get_by_id(task_id)

    async def create_task(
        self,
        iteration_id: int,
        actor: AgentActor,
        data: AgentTaskCreate,
        idempotency_key: Optional[str] = None,
    ) -> TaskResponse:
        """Create a task on behalf of an agent, honoring idempotency."""
        if not any(
            actor_has_scope(actor, scope) for scope in ("planning:write", "tasks:write")
        ):
            raise AgentPermissionError(
                "Missing required scope; expected one of: planning:write, tasks:write"
            )
        idempotency_key = validate_idempotency_key(idempotency_key)
        request_payload = {
            "iteration_id": iteration_id,
            "task": data.model_dump(mode="json"),
        }
        replay = await self._command_receipt_replay(
            actor,
            "task.create",
            "iteration",
            iteration_id,
            idempotency_key,
            request_payload,
        )
        if replay is not None:
            return TaskResponse.model_validate(replay["response"])
        task_create = TaskCreate(**data.model_dump())
        try:
            task = await self.task_service.create(
                iteration_id,
                task_create,
                actor_type="agent",
                actor_id=actor.id,
                idempotency_key=idempotency_key,
                commit=False,
            )
            loaded = await self.task_service.get_by_id(task.id)
            response = self.task_service.task_to_response(loaded or task)
            self._record_command_receipt(
                actor,
                "task.create",
                "iteration",
                iteration_id,
                idempotency_key,
                request_payload,
                {"response": response.model_dump(mode="json")},
            )
            await self.db.commit()
            return response
        except IntegrityError:
            await self.db.rollback()
            replay = await self._command_receipt_replay(
                actor,
                "task.create",
                "iteration",
                iteration_id,
                idempotency_key,
                request_payload,
            )
            if replay is not None:
                return TaskResponse.model_validate(replay["response"])
            raise
        except Exception:
            await self.db.rollback()
            raise

    async def patch_task(
        self,
        task_id: int,
        actor: AgentActor,
        data: AgentTaskPatch,
        idempotency_key: Optional[str] = None,
    ) -> Optional[TaskResponse]:
        """Patch a task with optimistic concurrency and audited status handling."""
        if "work:execute" in actor_scopes(actor):
            raise AgentPermissionError(
                "Assigned-work actors must use atomic begin, renew, submit, or fail; "
                "the legacy broad task patch is disabled."
            )
        if not any(
            actor_has_scope(actor, scope) for scope in ("planning:write", "tasks:write")
        ):
            raise AgentPermissionError(
                "Missing required scope; expected one of: planning:write, tasks:write"
            )
        idempotency_key = validate_idempotency_key(idempotency_key)
        request_payload = data.model_dump(mode="json", exclude_unset=True)
        replay = await self._command_receipt_replay(
            actor,
            "task.patch",
            "task",
            task_id,
            idempotency_key,
            request_payload,
        )
        if replay is not None:
            return TaskResponse.model_validate(replay["response"])

        task = await self.task_service.get_by_id(task_id)
        if not task:
            return None
        update_data = data.model_dump(exclude_unset=True)
        update_data.pop("expected_version", None)
        claim_id = update_data.pop("claim_id", None)
        claim_generation = update_data.pop("claim_generation", None)
        requested_status = update_data.pop("status", None)

        updated_task = task
        ordinary_change_reserved = False
        try:
            if update_data:
                task_update = TaskUpdate(
                    expected_version=data.expected_version,
                    **update_data,
                )
                updated_task = await self.task_service.update(
                    task_id,
                    task_update,
                    actor_type="agent",
                    actor_id=actor.id,
                    idempotency_key=idempotency_key,
                    commit=False,
                )
                ordinary_change_reserved = bool(
                    updated_task and updated_task.version != data.expected_version
                )

            if requested_status is not None:
                status_value = (
                    requested_status.value
                    if hasattr(requested_status, "value")
                    else requested_status
                )
                refreshed = await self.task_service.get_by_id(task_id)
                if refreshed and refreshed.status != status_value:
                    updated_task, _, _ = await self.task_service.change_status(
                        task_id,
                        requested_status,
                        actor_type="agent",
                        actor_id=actor.id,
                        idempotency_key=idempotency_key,
                        expected_version=(
                            updated_task.version if updated_task else data.expected_version
                        ),
                        commit=False,
                        reserve_version=not ordinary_change_reserved,
                    )
                    if updated_task is None:
                        raise ValueError(
                            f"Invalid task status transition: "
                            f"{refreshed.status} -> {status_value}"
                        )

            refreshed = await self.task_service.get_by_id(task_id)
            if refreshed is None:
                raise ValueError("Task disappeared during update")
            response = self.task_service.task_to_response(refreshed)
            self._record_command_receipt(
                actor,
                "task.patch",
                "task",
                task_id,
                idempotency_key,
                request_payload,
                {"response": response.model_dump(mode="json")},
            )
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        return response

    async def _command_receipt_replay(
        self,
        actor: AgentActor,
        operation: str,
        target_type: str,
        target_id: int,
        idempotency_key: Optional[str],
        request_payload: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """Return an exact durable command receipt or reject key reuse."""
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
        request_hash = self._command_request_hash(request_payload)
        if not secrets.compare_digest(record.request_hash, request_hash):
            raise AgentConflictError("idempotency_mismatch")
        try:
            payload = json.loads(record.response_payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise AgentConflictError("Idempotent command receipt is invalid") from exc
        if not isinstance(payload, dict):
            raise AgentConflictError("Idempotent command receipt is invalid")
        return payload

    def _record_command_receipt(
        self,
        actor: AgentActor,
        operation: str,
        target_type: str,
        target_id: int,
        idempotency_key: Optional[str],
        request_payload: dict[str, Any],
        response_payload: dict[str, Any],
    ) -> None:
        """Stage one durable response snapshot in the surrounding transaction."""
        if not idempotency_key or actor.id <= 0:
            return
        self.db.add(
            AgentIdempotencyRecord(
                actor_id=actor.id,
                operation=operation,
                target_type=target_type,
                target_id=target_id,
                idempotency_key=idempotency_key,
                request_hash=self._command_request_hash(request_payload),
                response_payload=json.dumps(response_payload, sort_keys=True),
            )
        )

    @staticmethod
    def _command_request_hash(payload: dict[str, Any]) -> str:
        canonical = json.dumps(
            payload, sort_keys=True, separators=(",", ":"), default=str
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    async def _task_from_idempotency(
        self,
        actor: AgentActor,
        event_type: str,
        idempotency_key: Optional[str],
    ) -> Optional[Task]:
        """Return an existing task for a prior idempotent task event."""
        event = await self._task_event_from_idempotency(actor, event_type, idempotency_key)
        return await self.task_service.get_by_id(event.task_id) if event and event.task_id else None

    async def _task_event_from_idempotency(
        self,
        actor: AgentActor,
        event_type: str,
        idempotency_key: Optional[str],
        *,
        task_id: Optional[int] = None,
    ) -> Optional[TaskEvent]:
        """Return a prior agent task event for an idempotent operation."""
        if not idempotency_key:
            return None
        query = select(TaskEvent).where(
            TaskEvent.actor_id == actor.id,
            TaskEvent.event_type == event_type,
            TaskEvent.idempotency_key == idempotency_key,
            TaskEvent.task_id.isnot(None),
        )
        if task_id is not None:
            query = query.where(TaskEvent.task_id == task_id)
        result = await self.db.execute(query.order_by(TaskEvent.created_at.desc(), TaskEvent.id.desc()))
        return result.scalars().first()

    async def append_task_event(
        self,
        task_id: int,
        actor: AgentActor,
        data: TaskEventCreate,
        idempotency_key: Optional[str] = None,
    ) -> Optional[TaskEvent]:
        """Append an agent-authored task event."""
        require_scope(actor, "events:write")
        assigned_worker = "work:execute" in actor_scopes(actor)
        idempotency_key = validate_idempotency_key(
            idempotency_key,
            required=assigned_worker,
        )
        request_payload = data.model_dump(mode="json")

        async def stable_replay() -> Optional[TaskEvent]:
            if not assigned_worker or idempotency_key is None:
                return None
            receipt = await self._command_receipt_replay(
                actor,
                "task.event.append",
                "task",
                task_id,
                idempotency_key,
                request_payload,
            )
            if receipt is None:
                return None
            event_id = receipt.get("event_id")
            event = (
                await self.db.get(TaskEvent, event_id)
                if isinstance(event_id, int)
                else None
            )
            if event is None:
                raise AgentConflictError(
                    "Idempotent task event receipt is invalid."
                )
            return event

        replay = await stable_replay()
        if replay is not None:
            return replay
        if not assigned_worker:
            existing = await self._task_event_from_idempotency(
                actor,
                data.event_type,
                idempotency_key,
                task_id=task_id,
            )
            if existing:
                if not self._task_event_matches(existing, data):
                    raise AgentConflictError(
                        "Task event idempotency key was reused with a different request."
                    )
                return existing

        if self.db.get_bind().dialect.name == "sqlite":
            await self.db.execute(
                text("UPDATE tasks SET id = id WHERE id = :task_id"),
                {"task_id": task_id},
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
        replay = await stable_replay()
        if replay is not None:
            return replay

        # A retry may arrive after the original command's claim expired or the
        # task was submitted.  Exact replays are therefore resolved before
        # validating mutable lease state; only a genuinely new append needs a
        # live fence.
        if assigned_worker:
            self._validate_task_fence(
                task,
                actor,
                data.claim_id,
                data.claim_generation,
            )

        event = await self.task_service.record_task_event(
            task_id,
            data.event_type,
            data.payload,
            actor_type="agent",
            actor_id=actor.id,
            trace_id=data.trace_id,
            span_id=data.span_id,
            correlation_id=data.correlation_id,
            idempotency_key=idempotency_key,
        )
        try:
            await self.db.flush()
        except IntegrityError:
            await self.db.rollback()
            existing = await self._task_event_from_idempotency(
                actor,
                data.event_type,
                idempotency_key,
                task_id=task_id,
            )
            if existing is None:
                raise
            if not self._task_event_matches(existing, data):
                raise AgentConflictError(
                    "Task event idempotency key was reused with a different request."
                )
            return existing
        if assigned_worker:
            self._record_command_receipt(
                actor,
                "task.event.append",
                "task",
                task_id,
                idempotency_key,
                request_payload,
                {"event_id": event.id},
            )
        await emit_outbound_webhook_event(
            self.db,
            commit=False,
            event_type="agent.task_event_created",
            entity_type="task",
            entity_id=task_id,
            data={
                "task_id": task_id,
                "task_event_id": event.id,
                "event_type": event.event_type,
                "actor_id": actor.id,
                "payload": self.event_to_payload(event.payload),
            },
        )
        await self.db.commit()
        await self.db.refresh(event)
        return event

    def _task_event_matches(
        self,
        event: TaskEvent,
        data: TaskEventCreate,
    ) -> bool:
        """Compare the persisted, non-secret task-event request fields."""
        return (
            event.event_type == data.event_type
            and self.event_to_payload(event.payload) == data.payload
            and event.trace_id == data.trace_id
            and event.span_id == data.span_id
            and event.correlation_id == data.correlation_id
        )

    async def start_run(
        self,
        actor: AgentActor,
        data: AgentRunCreate,
        idempotency_key: Optional[str] = None,
    ) -> AgentRun:
        """Start an agent run."""
        idempotency_key = validate_idempotency_key(idempotency_key)
        require_scope(actor, "runs:write")
        if "work:execute" in actor_scopes(actor):
            raise AgentPermissionError(
                "Assigned-work actors must use atomic begin; legacy run start is disabled."
            )
        if idempotency_key:
            result = await self.db.execute(
                select(AgentRun).where(
                    AgentRun.actor_id == actor.id,
                    AgentRun.idempotency_key == idempotency_key,
                )
            )
            existing = result.scalar_one_or_none()
            if existing:
                return existing

        if data.assignment_id is not None:
            assignment = await self.db.get(AgentTaskAssignment, data.assignment_id)
            if (
                assignment is None
                or assignment.actor_id != actor.id
                or assignment.state != "accepted"
                or assignment.task_id != data.task_id
            ):
                raise AgentConflictError("Run assignment is not accepted by this actor.")
            task = await self.task_service.get_by_id(assignment.task_id)
            if (
                task is None
                or task.claimed_by != actor.id
                or data.claim_generation != task.claim_generation
            ):
                raise AgentConflictError("Run claim generation is missing or stale.")

        run = AgentRun(
            task_id=data.task_id,
            actor_id=actor.id,
            assignment_id=data.assignment_id,
            claim_generation=data.claim_generation,
            status="running",
            trace_id=data.trace_id,
            model_trust_state=(
                "unverifiable" if (data.model or "").strip() else "unreported"
            ),
            model=data.model,
            tool_name=data.tool_name,
            run_metadata=json.dumps(data.metadata, ensure_ascii=False, default=str),
            artifact_links=json.dumps(data.artifact_links, ensure_ascii=False),
            commit_url=data.commit_url,
            pr_url=data.pr_url,
            idempotency_key=idempotency_key,
            heartbeat_at=utc_now(),
        )
        self.db.add(run)
        await self.db.flush()
        if data.task_id:
            await self.task_service.record_task_event(
                data.task_id,
                "agent_run_started",
                {"run_id": run.id, "model": data.model, "tool_name": data.tool_name},
                actor_type="agent",
                actor_id=actor.id,
                trace_id=data.trace_id,
                idempotency_key=idempotency_key,
            )
        await emit_outbound_webhook_event(
            self.db,
            commit=False,
            event_type="agent.run_created",
            entity_type="agent_run",
            entity_id=run.id,
            data={
                "run_id": run.id,
                "task_id": run.task_id,
                "actor_id": actor.id,
                "status": run.status,
                "model": run.model,
                "tool_name": run.tool_name,
                "trace_id": run.trace_id,
            },
        )
        await self.db.commit()
        await self.db.refresh(run)
        return run

    async def append_run_event(
        self,
        run_id: int,
        actor: AgentActor,
        data: AgentRunEventCreate,
    ) -> Optional[AgentRunEvent]:
        """Append an event to an agent run."""
        validate_idempotency_key(data.idempotency_key)
        require_scope(actor, "runs:write")
        request_payload = data.model_dump(mode="json")

        async def stable_replay() -> Optional[AgentRunEvent]:
            if data.idempotency_key is None:
                return None
            receipt = await self._command_receipt_replay(
                actor,
                "run.event.append",
                "run",
                run_id,
                data.idempotency_key,
                request_payload,
            )
            if receipt is None:
                return None
            event_id = receipt.get("event_id")
            event = (
                await self.db.get(AgentRunEvent, event_id)
                if isinstance(event_id, int)
                else None
            )
            if event is None:
                raise AgentConflictError("Idempotent run event receipt is invalid.")
            return event

        replay = await stable_replay()
        if replay is not None:
            return replay
        if self.db.get_bind().dialect.name == "sqlite":
            await self.db.execute(
                text("UPDATE agent_runs SET id = id WHERE id = :run_id"),
                {"run_id": run_id},
            )
        run_result = await self.db.execute(
            select(AgentRun)
            .where(AgentRun.id == run_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        run = run_result.scalar_one_or_none()
        if not run:
            return None
        if run.actor_id != actor.id and not actor_has_scope(actor, "admin"):
            raise AgentConflictError("Only the owning agent can append to this run.")
        assignment_bound = run.assignment_id is not None
        if assignment_bound:
            validate_idempotency_key(data.idempotency_key, required=True)
            if data.event_type not in ALLOWED_ASSIGNED_RUN_EVENT_TYPES:
                raise ValueError(
                    "Assignment-bound run events must use agent.progress, "
                    "agent.checkpoint, or agent.blocker"
                )
            if data.claim_generation != run.claim_generation:
                raise AgentConflictError("Run claim generation is missing or stale.")
            replay = await stable_replay()
            if replay is not None:
                return replay
        if data.idempotency_key:
            existing_result = await self.db.execute(
                select(AgentRunEvent).where(
                    AgentRunEvent.run_id == run_id,
                    AgentRunEvent.idempotency_key == data.idempotency_key,
                )
            )
            existing = existing_result.scalar_one_or_none()
            if existing is not None:
                if not self._run_event_matches(existing, run, data):
                    raise AgentConflictError(
                        "Run event idempotency key was reused with a different request."
                    )
                return existing

        # Resolve an exact retry before checking mutable run/claim state.  The
        # first append may have committed immediately before a terminal update
        # or lease expiry made the live fence invalid.
        if run.status != "running":
            raise AgentConflictError("Cannot append events to a terminal run.")
        await self._validate_run_fence(
            run,
            actor,
            claim_id=data.claim_id,
            claim_generation=data.claim_generation,
        )

        event = AgentRunEvent(
            run_id=run_id,
            event_type=data.event_type,
            message=data.message,
            payload=json.dumps(data.payload, ensure_ascii=False, default=str),
            trace_id=data.trace_id or run.trace_id,
            span_id=data.span_id,
            correlation_id=data.correlation_id,
            idempotency_key=data.idempotency_key,
        )
        run.heartbeat_at = utc_now()
        try:
            async with self.db.begin_nested():
                self.db.add(event)
                await self.db.flush()
        except IntegrityError:
            existing_result = await self.db.execute(
                select(AgentRunEvent).where(
                    AgentRunEvent.run_id == run_id,
                    AgentRunEvent.idempotency_key == data.idempotency_key,
                )
            )
            existing = existing_result.scalar_one_or_none()
            if existing is None or not self._run_event_matches(existing, run, data):
                raise AgentConflictError(
                    "Run event idempotency conflict."
                )
            return existing
        if assignment_bound:
            self._record_command_receipt(
                actor,
                "run.event.append",
                "run",
                run_id,
                data.idempotency_key,
                request_payload,
                {"event_id": event.id},
            )
        await emit_outbound_webhook_event(
            self.db,
            commit=False,
            event_type="agent.run_event_created",
            entity_type="agent_run",
            entity_id=run_id,
            data={
                "run_id": run_id,
                "run_event_id": event.id,
                "event_type": event.event_type,
                "message": event.message,
                "actor_id": actor.id,
                "payload": self.event_to_payload(event.payload),
                "trace_id": event.trace_id,
            },
        )
        await self.db.commit()
        await self.db.refresh(event)
        return event

    def _run_event_matches(
        self,
        event: AgentRunEvent,
        run: AgentRun,
        data: AgentRunEventCreate,
    ) -> bool:
        """Compare a replay request with the already persisted event payload."""
        return (
            event.event_type == data.event_type
            and event.message == data.message
            and self.event_to_payload(event.payload) == data.payload
            and event.trace_id == (data.trace_id or run.trace_id)
            and event.span_id == data.span_id
            and event.correlation_id == data.correlation_id
        )

    async def finish_run(
        self,
        run_id: int,
        actor: AgentActor,
        data: AgentRunFinish,
    ) -> Optional[AgentRun]:
        """Finish an agent run and attach final trace metadata."""
        if "work:execute" in actor_scopes(actor):
            raise AgentPermissionError(
                "Assigned-work actors must use atomic submit or fail; legacy run finish is disabled."
            )
        require_scope(actor, "runs:write")
        # Serialize the running -> terminal transition before inspecting mutable
        # state.  Row-locking databases honor ``FOR UPDATE``; SQLite ignores it,
        # so the no-op write acquires its database write reservation first.
        if self.db.get_bind().dialect.name == "sqlite":
            await self.db.execute(
                text("UPDATE agent_runs SET id = id WHERE id = :run_id"),
                {"run_id": run_id},
            )
        run_result = await self.db.execute(
            select(AgentRun)
            .where(AgentRun.id == run_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        run = run_result.scalar_one_or_none()
        if not run:
            return None
        if run.actor_id != actor.id and not actor_has_scope(actor, "admin"):
            raise AgentConflictError("Only the owning agent can finish this run.")
        if run.status != "running":
            if run.status == data.status:
                return run
            raise AgentConflictError(
                f"Run is already terminal with status {run.status}."
            )
        await self._validate_run_fence(run, actor)

        run.status = data.status
        run.ended_at = utc_now()
        run.summary = data.summary
        run.error = data.error
        if data.artifact_links:
            run.artifact_links = json.dumps(data.artifact_links, ensure_ascii=False)
        if data.commit_url is not None:
            run.commit_url = data.commit_url
        if data.pr_url is not None:
            run.pr_url = data.pr_url

        if run.task_id:
            await self.task_service.record_task_event(
                run.task_id,
                "agent_run_finished",
                {
                    "run_id": run.id,
                    "status": run.status,
                    "summary": run.summary,
                    "error": run.error,
                    "artifact_links": self._loads(run.artifact_links, []),
                    "commit_url": run.commit_url,
                    "pr_url": run.pr_url,
                },
                actor_type="agent",
                actor_id=actor.id,
                trace_id=run.trace_id,
            )

        await emit_outbound_webhook_event(
            self.db,
            commit=False,
            event_type="agent.run_finished",
            entity_type="agent_run",
            entity_id=run.id,
            data={
                "run_id": run.id,
                "task_id": run.task_id,
                "actor_id": actor.id,
                "status": run.status,
                "summary": run.summary,
                "error": run.error,
                "artifact_links": self._loads(run.artifact_links, []),
                "commit_url": run.commit_url,
                "pr_url": run.pr_url,
                "trace_id": run.trace_id,
            },
        )
        await self.db.commit()
        await self.db.refresh(run)
        return run

    @staticmethod
    def _validate_task_fence(
        task: Task,
        actor: AgentActor,
        claim_id: Optional[str],
        claim_generation: Optional[int],
    ) -> None:
        """Reject execution writes that do not own the current live fence."""
        if (
            not claim_id
            or claim_generation is None
            or task.claimed_by != actor.id
            or task.claim_id != claim_id
            or task.claim_generation != claim_generation
            or task.claim_expires_at is None
            or as_utc(task.claim_expires_at) <= as_utc(utc_now())
        ):
            raise AgentConflictError(
                "Claim fence is missing, stale, expired, or owned by another actor."
            )

    async def _validate_run_fence(
        self,
        run: AgentRun,
        actor: AgentActor,
        *,
        claim_id: Optional[str] = None,
        claim_generation: Optional[int] = None,
    ) -> None:
        """Validate the task fence for assignment-bound run writes."""
        if run.assignment_id is None:
            if "work:execute" in actor_scopes(actor):
                raise AgentPermissionError(
                    "Assigned-work actors cannot mutate legacy unbound runs."
                )
            return
        task = await self.task_service.get_by_id(run.task_id) if run.task_id else None
        if task is None:
            raise AgentConflictError("Assignment-bound run task is unavailable.")
        self._validate_task_fence(
            task,
            actor,
            claim_id,
            claim_generation,
        )

    async def get_run(self, run_id: int) -> Optional[AgentRun]:
        """Get an agent run by ID."""
        result = await self.db.execute(
            select(AgentRun).options(selectinload(AgentRun.events)).where(AgentRun.id == run_id)
        )
        return result.scalar_one_or_none()

    def event_to_payload(self, value: Optional[str]) -> dict[str, Any]:
        """Parse event payloads."""
        parsed = self._loads(value, {})
        return parsed if isinstance(parsed, dict) else {}

    def list_to_payload(self, value: Optional[str]) -> list[str]:
        """Parse JSON string lists."""
        parsed = self._loads(value, [])
        return parsed if isinstance(parsed, list) else []

    def _loads(self, value: Optional[str], fallback: Any) -> Any:
        try:
            return json.loads(value) if value else fallback
        except (json.JSONDecodeError, TypeError):
            return fallback

    async def get_task_timeline(self, task_id: int) -> list[dict[str, Any]]:
        """Return merged task event, status log, run, and run-event timeline items."""
        from app.models.task_status_log import TaskStatusLog

        task = await self.task_service.get_by_id(task_id)
        if not task:
            return []

        items: list[dict[str, Any]] = []

        events_result = await self.db.execute(
            select(TaskEvent).where(TaskEvent.task_id == task_id)
        )
        for event in events_result.scalars().all():
            items.append({
                "item_type": "task_event",
                "timestamp": event.created_at,
                "title": event.event_type,
                "payload": self.event_to_payload(event.payload),
                "actor_type": event.actor_type,
                "actor_id": event.actor_id,
                "trace_id": event.trace_id,
            })

        logs_result = await self.db.execute(
            select(TaskStatusLog).where(TaskStatusLog.task_id == task_id)
        )
        for log in logs_result.scalars().all():
            items.append({
                "item_type": "status_log",
                "timestamp": log.changed_at,
                "title": f"{log.from_status} -> {log.to_status}",
                "payload": {
                    "from_status": log.from_status,
                    "to_status": log.to_status,
                    "reason": log.reason,
                    "affected_task_ids": self._loads(log.affected_task_ids, []),
                },
                "actor_type": log.triggered_by,
                "actor_id": None,
                "trace_id": None,
            })

        runs_result = await self.db.execute(
            select(AgentRun).options(selectinload(AgentRun.events)).where(AgentRun.task_id == task_id)
        )
        for run in runs_result.scalars().all():
            items.append({
                "item_type": "agent_run",
                "timestamp": run.started_at,
                "title": f"agent_run_{run.status}",
                "payload": self._run_payload(run),
                "actor_type": "agent",
                "actor_id": run.actor_id,
                "trace_id": run.trace_id,
            })
            for event in run.events:
                items.append({
                    "item_type": "agent_run_event",
                    "timestamp": event.created_at,
                    "title": event.event_type,
                    "payload": {
                        "run_id": run.id,
                        "message": event.message,
                        **self.event_to_payload(event.payload),
                    },
                    "actor_type": "agent",
                    "actor_id": run.actor_id,
                    "trace_id": event.trace_id,
                })

        items.sort(key=lambda item: item["timestamp"])
        return items

    def _run_payload(self, run: AgentRun) -> dict[str, Any]:
        return {
            "run_id": run.id,
            "status": run.status,
            "model": run.model,
            "tool_name": run.tool_name,
            "metadata": self.event_to_payload(run.run_metadata),
            "artifact_links": self.list_to_payload(run.artifact_links),
            "commit_url": run.commit_url,
            "pr_url": run.pr_url,
            "summary": run.summary,
            "error": run.error,
            "ended_at": run.ended_at.isoformat() if run.ended_at else None,
        }

    async def get_pipeline(self) -> dict[str, list[TaskResponse]]:
        """Fetch and segment all tasks in the agent pipeline columns."""
        from app.models.task import Task, TaskDependency
        from sqlalchemy import and_, select
        from sqlalchemy.orm import selectinload

        now = utc_now()
        result = await self.db.execute(
            select(Task)
            .options(
                selectinload(Task.project),
                selectinload(Task.milestone),
                selectinload(Task.assignee),
                selectinload(Task.claimed_agent),
                selectinload(Task.external_links),
                selectinload(Task.request_source_links),
                selectinload(Task.children).selectinload(Task.project),
                selectinload(Task.children).selectinload(Task.milestone),
                selectinload(Task.children).selectinload(Task.assignee),
                selectinload(Task.children).selectinload(Task.claimed_agent),
                selectinload(Task.children).selectinload(Task.external_links),
                selectinload(Task.children).selectinload(Task.request_source_links),
                selectinload(Task.children).selectinload(Task.dependencies),
                selectinload(Task.children).selectinload(Task.dependencies).selectinload(TaskDependency.depends_on),
                selectinload(Task.dependencies).selectinload(TaskDependency.depends_on),
                selectinload(Task.parent),
            )
            .where(and_(Task.status != "closed", Task.is_deferred == False))
            .order_by(Task.priority.asc(), Task.id.asc())
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
        tasks = list(result.scalars().unique().all())
        if len(tasks) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "agent pipeline",
                MAX_BOUNDED_LIST_ITEMS,
            )

        needs_definition = []
        ready_for_agent = []
        definition_ready_unassigned = []
        assigned_waiting = []
        start_ready = []
        executing = []
        verification_required = []
        recovery_required = []

        # Query active/running agent runs
        task_ids = [task.id for task in tasks]
        runs_result = await self.db.execute(
            select(AgentRun).where(
                AgentRun.task_id.in_(task_ids),
                AgentRun.status == "running",
            )
        )
        all_runs = runs_result.scalars().all()
        running_run_task_ids = {
            run.task_id for run in all_runs if run.task_id and run.status == "running"
        }
        assignments_result = await self.db.execute(
            select(AgentTaskAssignment).where(
                AgentTaskAssignment.task_id.in_(task_ids),
                AgentTaskAssignment.purpose == "execution",
                AgentTaskAssignment.state.in_(("queued", "accepted")),
            )
        )
        all_assignments = assignments_result.scalars().all()
        assignments_by_task = {
            assignment.task_id: assignment
            for assignment in all_assignments
            if assignment.state in ("queued", "accepted")
        }
        from app.services.agent_work_service import AgentWorkService

        work_service = AgentWorkService(self.db)

        for task in tasks:
            task_resp = self.task_service.task_to_response(task)

            assignment = assignments_by_task.get(task.id)
            has_live_execution = (
                assignment is not None
                or task.id in running_run_task_ids
                or task.claimed_by is not None
            )

            # 1. Resolved tasks must have clean execution ownership before review.
            if task.status == "resolved":
                if has_live_execution:
                    recovery_required.append(task_resp)
                else:
                    verification_required.append(task_resp)
                continue

            if assignment is not None and assignment.state == "queued":
                blockers = await work_service._start_blockers(task, assignment, now)
                if not blockers:
                    start_ready.append(task_resp)
                else:
                    assigned_waiting.append(task_resp)
                continue

            # 2. Executing
            is_active_claim = (
                task.claimed_by is not None
                and task.claim_expires_at is not None
                and as_utc(task.claim_expires_at) > now
            )
            is_executing = (
                task.id in running_run_task_ids
                or is_active_claim
                or (assignment is not None and assignment.state == "accepted")
            )
            if is_executing:
                executing.append(task_resp)
                continue

            if task.status == TaskStatus.ACTIVE.value:
                if await work_service._has_pending_recovery_signal(task.id):
                    recovery_required.append(task_resp)
                continue

            # 3. Ready for Agent vs Needs Definition (Planned)
            if task_resp.agent_readiness.definition_ready:
                ready_for_agent.append(task_resp)
                definition_ready_unassigned.append(task_resp)
            else:
                needs_definition.append(task_resp)

        return {
            "needs_definition": needs_definition,
            "ready_for_agent": ready_for_agent,
            "definition_ready_unassigned": definition_ready_unassigned,
            "assigned_waiting": assigned_waiting,
            "start_ready": start_ready,
            "executing": executing,
            "verification_required": verification_required,
            "recovery_required": recovery_required,
        }
