"""Operator-owned model catalog, binding administration, and audit receipts."""

from __future__ import annotations

import hashlib
import json
import secrets
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal

from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.agent import (
    AgentActor,
    AgentIdempotencyRecord,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTaskAssignment,
    TaskEvent,
)
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_routing import (
    AgentModelBindingCreate,
    AgentModelBindingDisable,
    AgentModelBindingResponse,
    AgentModelBindingUpdate,
    AgentModelCatalogCreate,
    AgentModelCatalogDisable,
    AgentModelCatalogResponse,
    AgentModelCatalogUpdate,
    AgentModelMutationReceipt,
)
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    actor_has_scope,
    require_scope,
    validate_idempotency_key,
)


LIVE_ASSIGNMENT_STATES = ("queued", "accepted")
MODEL_CATALOG_READ_SCOPES = ("planning:read", "admin")


class AgentModelConflictError(AgentConflictError):
    """Stable model-control conflict shared by REST and MCP."""

    def __init__(self, code: str, message: str, **context: Any):
        self.code = code
        self.message = message
        self.context = context
        super().__init__(message)

    def detail(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            **self.context,
        }


@dataclass(frozen=True)
class _MutationResult:
    target_type: Literal["model_catalog", "model_binding"]
    target_id: int
    authoritative_revision: int
    result: dict[str, Any]
    invalidated_assignment_ids: tuple[int, ...] = ()
    audit_event_ids: tuple[int, ...] = ()


Mutation = Callable[[], Awaitable[_MutationResult]]


class AgentModelCatalogService:
    """Expose secret-free reads and replay-safe admin model mutations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _require_read(actor: AgentActor) -> None:
        if not any(actor_has_scope(actor, scope) for scope in MODEL_CATALOG_READ_SCOPES):
            raise AgentPermissionError("Missing required scope: planning:read")

    @staticmethod
    def _request_hash(payload: dict[str, Any]) -> str:
        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def _audited_request(
        data: Any,
        command: AgentPlanningCommandContext,
    ) -> dict[str, Any]:
        return {
            "command": {
                "rationale": command.rationale,
                "correlation_id": command.correlation_id,
            },
            "payload": data.model_dump(
                mode="json",
                exclude_unset=True,
            ),
        }

    async def _replay(
        self,
        *,
        actor_id: int,
        operation: str,
        target_type: str,
        idempotency_target_id: int,
        idempotency_key: str,
        request_payload: dict[str, Any],
    ) -> AgentModelMutationReceipt | None:
        result = await self.db.execute(
            select(AgentIdempotencyRecord).where(
                AgentIdempotencyRecord.actor_id == actor_id,
                AgentIdempotencyRecord.operation == operation,
                AgentIdempotencyRecord.target_type == target_type,
                AgentIdempotencyRecord.target_id == idempotency_target_id,
                AgentIdempotencyRecord.idempotency_key == idempotency_key,
            )
        )
        record = result.scalar_one_or_none()
        if record is None:
            return None
        if not secrets.compare_digest(
            record.request_hash,
            self._request_hash(request_payload),
        ):
            raise AgentModelConflictError(
                "agent_model_idempotency_conflict",
                "Idempotency key was already used with a different model request",
            )
        try:
            payload = json.loads(record.response_payload)
            return AgentModelMutationReceipt.model_validate(payload["response"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise AgentModelConflictError(
                "agent_model_receipt_invalid",
                "Stored model mutation receipt is invalid",
            ) from exc

    async def _execute(
        self,
        *,
        actor: AgentActor,
        operation: str,
        target_type: str,
        idempotency_target_id: int,
        command: AgentPlanningCommandContext,
        request_payload: dict[str, Any],
        mutate: Mutation,
    ) -> AgentModelMutationReceipt:
        require_scope(actor, "admin")
        actor_id = actor.id
        if actor_id <= 0:
            raise AgentPermissionError(
                "Model mutations require a stored admin actor identity"
            )
        idempotency_key = validate_idempotency_key(
            command.idempotency_key,
            required=True,
        )
        assert idempotency_key is not None

        replay = await self._replay(
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            idempotency_target_id=idempotency_target_id,
            idempotency_key=idempotency_key,
            request_payload=request_payload,
        )
        if replay is not None:
            return replay

        try:
            mutation = await mutate()
            receipt = AgentModelMutationReceipt(
                operation=operation,
                actor_id=actor_id,
                target_type=mutation.target_type,
                target_id=mutation.target_id,
                idempotency_key=idempotency_key,
                rationale=command.rationale,
                correlation_id=command.correlation_id,
                authoritative_revision=mutation.authoritative_revision,
                invalidated_assignment_ids=list(
                    mutation.invalidated_assignment_ids
                ),
                audit_event_ids=list(mutation.audit_event_ids),
                result=mutation.result,
            )
            self.db.add(
                AgentIdempotencyRecord(
                    actor_id=actor_id,
                    operation=operation,
                    target_type=target_type,
                    target_id=idempotency_target_id,
                    idempotency_key=idempotency_key,
                    request_hash=self._request_hash(request_payload),
                    response_payload=json.dumps(
                        {"response": receipt.model_dump(mode="json")},
                        sort_keys=True,
                    ),
                )
            )
            await self.db.commit()
            return receipt
        except IntegrityError as exc:
            await self.db.rollback()
            replay = await self._replay(
                actor_id=actor_id,
                operation=operation,
                target_type=target_type,
                idempotency_target_id=idempotency_target_id,
                idempotency_key=idempotency_key,
                request_payload=request_payload,
            )
            if replay is not None:
                return replay
            raise AgentModelConflictError(
                "agent_model_uniqueness_conflict",
                "Model catalog or binding conflicts with current authoritative state",
            ) from exc
        except AgentModelConflictError:
            await self.db.rollback()
            replay = await self._replay(
                actor_id=actor_id,
                operation=operation,
                target_type=target_type,
                idempotency_target_id=idempotency_target_id,
                idempotency_key=idempotency_key,
                request_payload=request_payload,
            )
            if replay is not None:
                return replay
            raise
        except Exception:
            await self.db.rollback()
            raise

    async def _catalog_entry(
        self,
        *,
        catalog_id: int | None = None,
        catalog_key: str | None = None,
        for_update: bool = False,
    ) -> AgentModelCatalogEntry | None:
        query = select(AgentModelCatalogEntry).options(
            selectinload(AgentModelCatalogEntry.bindings)
        )
        if catalog_id is not None:
            query = query.where(AgentModelCatalogEntry.id == catalog_id)
        elif catalog_key is not None:
            query = query.where(AgentModelCatalogEntry.key == catalog_key)
        else:
            raise ValueError("Catalog lookup requires an id or key")
        if for_update:
            if self.db.get_bind().dialect.name == "sqlite":
                assert catalog_id is not None
                await self.db.execute(
                    text(
                        "UPDATE agent_model_catalog_entries SET id = id "
                        "WHERE id = :catalog_id"
                    ),
                    {"catalog_id": catalog_id},
                )
            query = query.with_for_update()
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _binding(
        self,
        binding_id: int,
        *,
        for_update: bool = False,
    ) -> AgentModelBinding | None:
        query = (
            select(AgentModelBinding)
            .options(selectinload(AgentModelBinding.model_catalog))
            .where(AgentModelBinding.id == binding_id)
        )
        if for_update:
            if self.db.get_bind().dialect.name == "sqlite":
                await self.db.execute(
                    text(
                        "UPDATE agent_model_bindings SET id = id "
                        "WHERE id = :binding_id"
                    ),
                    {"binding_id": binding_id},
                )
            query = query.with_for_update()
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _catalog_bindings(
        self,
        catalog_id: int,
        *,
        for_update: bool = False,
    ) -> list[AgentModelBinding]:
        query = (
            select(AgentModelBinding)
            .options(selectinload(AgentModelBinding.model_catalog))
            .where(AgentModelBinding.model_catalog_id == catalog_id)
            .order_by(AgentModelBinding.id)
        )
        if for_update:
            query = query.with_for_update()
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _locked_binding(
        self,
        binding_id: int,
    ) -> AgentModelBinding | None:
        hint_result = await self.db.execute(
            select(AgentModelBinding.model_catalog_id).where(
                AgentModelBinding.id == binding_id
            )
        )
        catalog_id = hint_result.scalar_one_or_none()
        if catalog_id is None:
            return None
        catalog = await self._catalog_entry(
            catalog_id=int(catalog_id),
            for_update=True,
        )
        if catalog is None:
            raise AgentModelConflictError(
                "agent_model_catalog_missing",
                "Model binding catalog entry is missing",
                binding_id=binding_id,
            )
        binding = await self._binding(binding_id, for_update=True)
        if binding is not None and binding.model_catalog_id != catalog.id:
            raise AgentModelConflictError(
                "agent_model_binding_changed",
                "Model binding changed while acquiring its catalog lock",
                binding_id=binding_id,
            )
        return binding

    @staticmethod
    def _catalog_response(
        catalog: AgentModelCatalogEntry,
    ) -> AgentModelCatalogResponse:
        return AgentModelCatalogResponse.model_validate(catalog)

    async def _binding_reference_counts(
        self,
        binding_ids: list[int],
    ) -> dict[int, tuple[int, int, int]]:
        if not binding_ids:
            return {}
        assignment_rows = (
            await self.db.execute(
                select(
                    AgentTaskAssignment.model_binding_id,
                    AgentTaskAssignment.state,
                    func.count(AgentTaskAssignment.id),
                )
                .where(AgentTaskAssignment.model_binding_id.in_(binding_ids))
                .group_by(
                    AgentTaskAssignment.model_binding_id,
                    AgentTaskAssignment.state,
                )
            )
        ).all()
        run_rows = (
            await self.db.execute(
                select(
                    AgentRun.model_binding_id,
                    func.count(AgentRun.id),
                )
                .where(AgentRun.model_binding_id.in_(binding_ids))
                .group_by(AgentRun.model_binding_id)
            )
        ).all()
        counts: dict[int, list[int]] = {
            binding_id: [0, 0, 0] for binding_id in binding_ids
        }
        for binding_id, state, count in assignment_rows:
            if binding_id is None:
                continue
            bucket = 0 if state in LIVE_ASSIGNMENT_STATES else 1
            counts[int(binding_id)][bucket] += int(count)
        for binding_id, count in run_rows:
            if binding_id is not None:
                counts[int(binding_id)][2] = int(count)
        return {
            binding_id: (values[0], values[1], values[2])
            for binding_id, values in counts.items()
        }

    def binding_response(
        self,
        binding: AgentModelBinding,
        *,
        reference_counts: tuple[int, int, int] = (0, 0, 0),
    ) -> AgentModelBindingResponse:
        catalog = (
            self._catalog_response(binding.model_catalog)
            if binding.model_catalog is not None
            else None
        )
        return AgentModelBindingResponse(
            id=binding.id,
            actor_id=binding.actor_id,
            model_catalog_id=binding.model_catalog_id,
            is_default=binding.is_default,
            enabled=binding.enabled,
            tool_tags=binding.tool_tags,
            data_policy_tags=binding.data_policy_tags,
            revision=binding.revision,
            model_catalog_key=catalog.key if catalog is not None else None,
            selectable=binding.selectable,
            model_catalog=catalog,
            live_assignment_count=reference_counts[0],
            historical_assignment_count=reference_counts[1],
            run_reference_count=reference_counts[2],
            created_at=binding.created_at,
            updated_at=binding.updated_at,
        )

    async def list_catalog(
        self,
        actor: AgentActor,
        *,
        include_disabled: bool = False,
    ) -> list[AgentModelCatalogResponse]:
        """List bounded provider-neutral model declarations."""

        self._require_read(actor)
        query = select(AgentModelCatalogEntry).order_by(
            AgentModelCatalogEntry.key,
            AgentModelCatalogEntry.id,
        )
        if not include_disabled:
            query = query.where(AgentModelCatalogEntry.enabled.is_(True))
        result = await self.db.execute(query.limit(MAX_BOUNDED_LIST_ITEMS + 1))
        entries = list(result.scalars().all())
        if len(entries) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "agent model catalog",
                MAX_BOUNDED_LIST_ITEMS,
            )
        return [self._catalog_response(entry) for entry in entries]

    async def get_catalog(
        self,
        actor: AgentActor,
        catalog_key: str,
    ) -> AgentModelCatalogResponse:
        """Read one secret-free catalog entry by stable key."""

        self._require_read(actor)
        entry = await self._catalog_entry(catalog_key=catalog_key)
        if entry is None:
            raise LookupError("Model catalog entry not found")
        return self._catalog_response(entry)

    async def list_bindings(
        self,
        actor: AgentActor,
        *,
        actor_id: int | None = None,
        include_disabled: bool = False,
    ) -> list[AgentModelBindingResponse]:
        """List bounded actor binding evidence, including audit-only rows on request."""

        self._require_read(actor)
        query = (
            select(AgentModelBinding)
            .options(selectinload(AgentModelBinding.model_catalog))
            .order_by(AgentModelBinding.actor_id, AgentModelBinding.id)
        )
        if actor_id is not None:
            query = query.where(AgentModelBinding.actor_id == actor_id)
        if not include_disabled:
            query = query.where(AgentModelBinding.enabled.is_(True))
        result = await self.db.execute(query.limit(MAX_BOUNDED_LIST_ITEMS + 1))
        bindings = list(result.scalars().all())
        if len(bindings) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "agent model bindings",
                MAX_BOUNDED_LIST_ITEMS,
            )
        counts = await self._binding_reference_counts(
            [binding.id for binding in bindings]
        )
        return [
            self.binding_response(
                binding,
                reference_counts=counts.get(binding.id, (0, 0, 0)),
            )
            for binding in bindings
        ]

    async def get_binding(
        self,
        actor: AgentActor,
        binding_id: int,
    ) -> AgentModelBindingResponse:
        """Read one binding, including disabled historical evidence."""

        self._require_read(actor)
        binding = await self._binding(binding_id)
        if binding is None:
            raise LookupError("Model binding not found")
        counts = await self._binding_reference_counts([binding.id])
        return self.binding_response(
            binding,
            reference_counts=counts.get(binding.id, (0, 0, 0)),
        )

    async def _live_assignments(
        self,
        binding_ids: list[int],
    ) -> tuple[list[AgentTaskAssignment], dict[int, AgentActor]]:
        if not binding_ids:
            return [], {}
        actor_hint_rows = (
            await self.db.execute(
                select(AgentTaskAssignment.actor_id)
                .where(
                    AgentTaskAssignment.model_binding_id.in_(binding_ids),
                    AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES),
                )
                .distinct()
                .order_by(AgentTaskAssignment.actor_id)
            )
        ).scalars().all()
        locked_actors: dict[int, AgentActor] = {}
        if actor_hint_rows:
            actor_result = await self.db.execute(
                select(AgentActor)
                .where(AgentActor.id.in_(actor_hint_rows))
                .order_by(AgentActor.id)
                .with_for_update()
            )
            locked_actors = {
                actor.id: actor for actor in actor_result.scalars().all()
            }
        result = await self.db.execute(
            select(AgentTaskAssignment)
            .where(
                AgentTaskAssignment.model_binding_id.in_(binding_ids),
                AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES),
            )
            .order_by(AgentTaskAssignment.id)
            .with_for_update()
        )
        assignments = list(result.scalars().all())
        missing_actor_ids = sorted(
            {
                assignment.actor_id
                for assignment in assignments
                if assignment.actor_id not in locked_actors
            }
        )
        if missing_actor_ids:
            raise AgentModelConflictError(
                "agent_model_live_assignments_changed",
                "Live assignments changed while acquiring model mutation locks",
                actor_ids=missing_actor_ids,
            )
        return assignments, locked_actors

    async def _invalidation_events(
        self,
        *,
        assignments: list[AgentTaskAssignment],
        principal: AgentActor,
        command: AgentPlanningCommandContext,
        reason_code: str,
        binding_revisions: dict[int, int],
        locked_actors: dict[int, AgentActor],
    ) -> list[TaskEvent]:
        events: list[TaskEvent] = []
        for assignment in assignments:
            binding_id = assignment.model_binding_id
            event = TaskEvent(
                task_id=assignment.task_id,
                actor_type="agent",
                actor_id=principal.id,
                event_type="agent.model_binding_invalidated",
                payload=json.dumps(
                    {
                        "assignment_id": assignment.id,
                        "binding_id": binding_id,
                        "assigned_binding_revision": (
                            assignment.model_binding_revision
                        ),
                        "current_binding_revision": (
                            binding_revisions.get(binding_id)
                            if binding_id is not None
                            else None
                        ),
                        "reason_code": reason_code,
                        "rationale": command.rationale,
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                correlation_id=command.correlation_id,
                idempotency_key=command.idempotency_key,
            )
            self.db.add(event)
            events.append(event)
        for actor_id in sorted({assignment.actor_id for assignment in assignments}):
            locked_actors[actor_id].queue_revision += 1
        return events

    async def _mutation_audit_event(
        self,
        *,
        principal: AgentActor,
        command: AgentPlanningCommandContext,
        operation: str,
        target_type: str,
        target_id: int,
        authoritative_revision: int,
        invalidated_assignment_ids: list[int],
    ) -> TaskEvent:
        event = TaskEvent(
            task_id=None,
            actor_type="agent",
            actor_id=principal.id,
            event_type="agent.model_configuration_changed",
            payload=json.dumps(
                {
                    "operation": operation,
                    "target_type": target_type,
                    "target_id": target_id,
                    "authoritative_revision": authoritative_revision,
                    "invalidated_assignment_ids": invalidated_assignment_ids,
                    "rationale": command.rationale,
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            correlation_id=command.correlation_id,
            idempotency_key=command.idempotency_key,
        )
        self.db.add(event)
        return event

    @staticmethod
    def _raise_revision_conflict(
        resource: str,
        resource_id: int,
        *,
        expected: int,
        current: int,
    ) -> None:
        raise AgentModelConflictError(
            "agent_model_revision_conflict",
            f"{resource} revision is stale",
            resource=resource,
            resource_id=resource_id,
            expected_revision=expected,
            current_revision=current,
        )

    @staticmethod
    def _require_reconciliation(
        assignments: list[AgentTaskAssignment],
        *,
        reconcile: bool,
    ) -> None:
        if assignments and not reconcile:
            raise AgentModelConflictError(
                "agent_model_live_assignments",
                "Model mutation would invalidate live assignments; reconcile or "
                "cancel them explicitly",
                live_assignment_ids=[
                    assignment.id for assignment in assignments
                ],
            )

    async def create_catalog(
        self,
        actor: AgentActor,
        data: AgentModelCatalogCreate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Create one stable model declaration with an exact durable receipt."""

        request_payload = self._audited_request(data, command)

        async def mutate() -> _MutationResult:
            existing = await self._catalog_entry(catalog_key=data.key)
            if existing is not None:
                raise AgentModelConflictError(
                    "agent_model_catalog_key_conflict",
                    "Model catalog key already exists",
                    catalog_key=data.key,
                )
            entry = AgentModelCatalogEntry(
                **data.model_dump(mode="python"),
            )
            self.db.add(entry)
            await self.db.flush()
            audit = await self._mutation_audit_event(
                principal=actor,
                command=command,
                operation="model_catalog.create",
                target_type="model_catalog",
                target_id=entry.id,
                authoritative_revision=entry.revision,
                invalidated_assignment_ids=[],
            )
            await self.db.flush()
            entry = await self._catalog_entry(catalog_id=entry.id)
            assert entry is not None
            return _MutationResult(
                target_type="model_catalog",
                target_id=entry.id,
                authoritative_revision=entry.revision,
                result=self._catalog_response(entry).model_dump(mode="json"),
                audit_event_ids=(audit.id,),
            )

        return await self._execute(
            actor=actor,
            operation="model_catalog.create",
            target_type="model_catalog",
            idempotency_target_id=0,
            command=command,
            request_payload=request_payload,
            mutate=mutate,
        )

    async def update_catalog(
        self,
        catalog_id: int,
        actor: AgentActor,
        data: AgentModelCatalogUpdate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Update one catalog entry and invalidate dependent live decisions."""

        request_payload = self._audited_request(data, command)

        async def mutate() -> _MutationResult:
            entry = await self._catalog_entry(
                catalog_id=catalog_id,
                for_update=True,
            )
            if entry is None:
                raise LookupError("Model catalog entry not found")
            if entry.revision != data.expected_revision:
                self._raise_revision_conflict(
                    "model_catalog",
                    entry.id,
                    expected=data.expected_revision,
                    current=entry.revision,
                )
            bindings = await self._catalog_bindings(
                entry.id,
                for_update=True,
            )
            assignments, locked_actors = await self._live_assignments(
                [binding.id for binding in bindings]
            )
            self._require_reconciliation(
                assignments,
                reconcile=data.reconcile_live_assignments,
            )

            updates = data.model_dump(
                mode="python",
                exclude_unset=True,
                exclude={
                    "expected_revision",
                    "reconcile_live_assignments",
                },
            )
            changed = any(getattr(entry, key) != value for key, value in updates.items())
            if not changed:
                raise AgentModelConflictError(
                    "agent_model_no_change",
                    "Catalog update does not change authoritative state",
                )
            for key, value in updates.items():
                setattr(entry, key, value)
            entry.revision += 1
            for binding in bindings:
                binding.revision += 1
            binding_revisions = {
                binding.id: binding.revision for binding in bindings
            }
            invalidation_events = await self._invalidation_events(
                assignments=assignments,
                principal=actor,
                command=command,
                reason_code="model_catalog_revised",
                binding_revisions=binding_revisions,
                locked_actors=locked_actors,
            )
            await self.db.flush()
            audit = await self._mutation_audit_event(
                principal=actor,
                command=command,
                operation="model_catalog.update",
                target_type="model_catalog",
                target_id=entry.id,
                authoritative_revision=entry.revision,
                invalidated_assignment_ids=[
                    assignment.id for assignment in assignments
                ],
            )
            await self.db.flush()
            entry = await self._catalog_entry(catalog_id=entry.id)
            assert entry is not None
            return _MutationResult(
                target_type="model_catalog",
                target_id=entry.id,
                authoritative_revision=entry.revision,
                result=self._catalog_response(entry).model_dump(mode="json"),
                invalidated_assignment_ids=tuple(
                    assignment.id for assignment in assignments
                ),
                audit_event_ids=tuple(
                    sorted(
                        [audit.id, *(event.id for event in invalidation_events)]
                    )
                ),
            )

        return await self._execute(
            actor=actor,
            operation="model_catalog.update",
            target_type="model_catalog",
            idempotency_target_id=catalog_id,
            command=command,
            request_payload=request_payload,
            mutate=mutate,
        )

    async def disable_catalog(
        self,
        catalog_id: int,
        actor: AgentActor,
        data: AgentModelCatalogDisable,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Soft-disable a catalog entry while preserving all audit references."""

        request_payload = self._audited_request(data, command)

        async def mutate() -> _MutationResult:
            entry = await self._catalog_entry(
                catalog_id=catalog_id,
                for_update=True,
            )
            if entry is None:
                raise LookupError("Model catalog entry not found")
            if entry.revision != data.expected_revision:
                self._raise_revision_conflict(
                    "model_catalog",
                    entry.id,
                    expected=data.expected_revision,
                    current=entry.revision,
                )
            if not entry.enabled:
                raise AgentModelConflictError(
                    "agent_model_already_disabled",
                    "Model catalog entry is already disabled",
                )
            bindings = await self._catalog_bindings(
                entry.id,
                for_update=True,
            )
            assignments, locked_actors = await self._live_assignments(
                [binding.id for binding in bindings]
            )
            self._require_reconciliation(
                assignments,
                reconcile=data.reconcile_live_assignments,
            )
            entry.enabled = False
            entry.revision += 1
            for binding in bindings:
                binding.revision += 1
            invalidation_events = await self._invalidation_events(
                assignments=assignments,
                principal=actor,
                command=command,
                reason_code="model_catalog_disabled",
                binding_revisions={
                    binding.id: binding.revision for binding in bindings
                },
                locked_actors=locked_actors,
            )
            await self.db.flush()
            audit = await self._mutation_audit_event(
                principal=actor,
                command=command,
                operation="model_catalog.disable",
                target_type="model_catalog",
                target_id=entry.id,
                authoritative_revision=entry.revision,
                invalidated_assignment_ids=[
                    assignment.id for assignment in assignments
                ],
            )
            await self.db.flush()
            entry = await self._catalog_entry(catalog_id=entry.id)
            assert entry is not None
            return _MutationResult(
                target_type="model_catalog",
                target_id=entry.id,
                authoritative_revision=entry.revision,
                result=self._catalog_response(entry).model_dump(mode="json"),
                invalidated_assignment_ids=tuple(
                    assignment.id for assignment in assignments
                ),
                audit_event_ids=tuple(
                    sorted(
                        [audit.id, *(event.id for event in invalidation_events)]
                    )
                ),
            )

        return await self._execute(
            actor=actor,
            operation="model_catalog.disable",
            target_type="model_catalog",
            idempotency_target_id=catalog_id,
            command=command,
            request_payload=request_payload,
            mutate=mutate,
        )

    async def create_binding(
        self,
        actor: AgentActor,
        data: AgentModelBindingCreate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Create one actor-owned runtime binding."""

        request_payload = self._audited_request(data, command)

        async def mutate() -> _MutationResult:
            target_actor = await self.db.get(AgentActor, data.actor_id)
            if target_actor is None:
                raise LookupError("Agent actor not found")
            catalog = await self._catalog_entry(
                catalog_id=data.model_catalog_id,
                for_update=True,
            )
            if catalog is None:
                raise LookupError("Model catalog entry not found")
            if data.enabled and not catalog.enabled:
                raise AgentModelConflictError(
                    "agent_model_catalog_disabled",
                    "Enabled bindings require an enabled model catalog entry",
                )
            existing_result = await self.db.execute(
                select(AgentModelBinding).where(
                    AgentModelBinding.actor_id == data.actor_id,
                    AgentModelBinding.model_catalog_id == data.model_catalog_id,
                )
            )
            if existing_result.scalar_one_or_none() is not None:
                raise AgentModelConflictError(
                    "agent_model_binding_conflict",
                    "Actor already has a binding for this model catalog entry",
                )
            if data.is_default:
                await self._require_default_slot(data.actor_id)
            binding = AgentModelBinding(
                **data.model_dump(mode="python"),
            )
            self.db.add(binding)
            await self.db.flush()
            audit = await self._mutation_audit_event(
                principal=actor,
                command=command,
                operation="model_binding.create",
                target_type="model_binding",
                target_id=binding.id,
                authoritative_revision=binding.revision,
                invalidated_assignment_ids=[],
            )
            await self.db.flush()
            binding = await self._binding(binding.id)
            assert binding is not None
            counts = await self._binding_reference_counts([binding.id])
            return _MutationResult(
                target_type="model_binding",
                target_id=binding.id,
                authoritative_revision=binding.revision,
                result=self.binding_response(
                    binding,
                    reference_counts=counts.get(binding.id, (0, 0, 0)),
                ).model_dump(mode="json"),
                audit_event_ids=(audit.id,),
            )

        return await self._execute(
            actor=actor,
            operation="model_binding.create",
            target_type="model_binding",
            idempotency_target_id=data.actor_id,
            command=command,
            request_payload=request_payload,
            mutate=mutate,
        )

    async def _require_default_slot(
        self,
        actor_id: int,
        *,
        exclude_binding_id: int | None = None,
    ) -> None:
        query = select(AgentModelBinding.id).where(
            AgentModelBinding.actor_id == actor_id,
            AgentModelBinding.enabled.is_(True),
            AgentModelBinding.is_default.is_(True),
        )
        if exclude_binding_id is not None:
            query = query.where(AgentModelBinding.id != exclude_binding_id)
        result = await self.db.execute(query.limit(1))
        if result.scalar_one_or_none() is not None:
            raise AgentModelConflictError(
                "agent_model_default_binding_conflict",
                "Actor already has an enabled default model binding",
                actor_id=actor_id,
            )

    async def update_binding(
        self,
        binding_id: int,
        actor: AgentActor,
        data: AgentModelBindingUpdate,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Update one binding behind an optimistic revision fence."""

        request_payload = self._audited_request(data, command)

        async def mutate() -> _MutationResult:
            binding = await self._locked_binding(binding_id)
            if binding is None:
                raise LookupError("Model binding not found")
            if binding.revision != data.expected_revision:
                self._raise_revision_conflict(
                    "model_binding",
                    binding.id,
                    expected=data.expected_revision,
                    current=binding.revision,
                )
            assignments, locked_actors = await self._live_assignments(
                [binding.id]
            )
            self._require_reconciliation(
                assignments,
                reconcile=data.reconcile_live_assignments,
            )
            updates = data.model_dump(
                mode="python",
                exclude_unset=True,
                exclude={
                    "expected_revision",
                    "reconcile_live_assignments",
                },
            )
            if updates.get("enabled") and (
                binding.model_catalog is None
                or not binding.model_catalog.enabled
            ):
                raise AgentModelConflictError(
                    "agent_model_catalog_disabled",
                    "Enabled bindings require an enabled model catalog entry",
                )
            candidate_enabled = updates.get("enabled", binding.enabled)
            candidate_default = updates.get("is_default", binding.is_default)
            if candidate_default and not candidate_enabled:
                raise ValueError("A default model binding must be enabled")
            if candidate_default and (
                not binding.is_default or not binding.enabled
            ):
                await self._require_default_slot(
                    binding.actor_id,
                    exclude_binding_id=binding.id,
                )
            changed = any(
                getattr(binding, key) != value for key, value in updates.items()
            )
            if not changed:
                raise AgentModelConflictError(
                    "agent_model_no_change",
                    "Binding update does not change authoritative state",
                )
            for key, value in updates.items():
                setattr(binding, key, value)
            binding.revision += 1
            invalidation_events = await self._invalidation_events(
                assignments=assignments,
                principal=actor,
                command=command,
                reason_code="model_binding_revised",
                binding_revisions={binding.id: binding.revision},
                locked_actors=locked_actors,
            )
            await self.db.flush()
            audit = await self._mutation_audit_event(
                principal=actor,
                command=command,
                operation="model_binding.update",
                target_type="model_binding",
                target_id=binding.id,
                authoritative_revision=binding.revision,
                invalidated_assignment_ids=[
                    assignment.id for assignment in assignments
                ],
            )
            await self.db.flush()
            binding = await self._binding(binding.id)
            assert binding is not None
            counts = await self._binding_reference_counts([binding.id])
            return _MutationResult(
                target_type="model_binding",
                target_id=binding.id,
                authoritative_revision=binding.revision,
                result=self.binding_response(
                    binding,
                    reference_counts=counts.get(binding.id, (0, 0, 0)),
                ).model_dump(mode="json"),
                invalidated_assignment_ids=tuple(
                    assignment.id for assignment in assignments
                ),
                audit_event_ids=tuple(
                    sorted(
                        [audit.id, *(event.id for event in invalidation_events)]
                    )
                ),
            )

        return await self._execute(
            actor=actor,
            operation="model_binding.update",
            target_type="model_binding",
            idempotency_target_id=binding_id,
            command=command,
            request_payload=request_payload,
            mutate=mutate,
        )

    async def disable_binding(
        self,
        binding_id: int,
        actor: AgentActor,
        data: AgentModelBindingDisable,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Soft-disable a binding only after explicit live-work reconciliation."""

        request_payload = self._audited_request(data, command)

        async def mutate() -> _MutationResult:
            binding = await self._locked_binding(binding_id)
            if binding is None:
                raise LookupError("Model binding not found")
            if binding.revision != data.expected_revision:
                self._raise_revision_conflict(
                    "model_binding",
                    binding.id,
                    expected=data.expected_revision,
                    current=binding.revision,
                )
            if not binding.enabled:
                raise AgentModelConflictError(
                    "agent_model_already_disabled",
                    "Model binding is already disabled",
                )
            assignments, locked_actors = await self._live_assignments(
                [binding.id]
            )
            self._require_reconciliation(
                assignments,
                reconcile=data.reconcile_live_assignments,
            )
            binding.enabled = False
            binding.is_default = False
            binding.revision += 1
            invalidation_events = await self._invalidation_events(
                assignments=assignments,
                principal=actor,
                command=command,
                reason_code="model_binding_disabled",
                binding_revisions={binding.id: binding.revision},
                locked_actors=locked_actors,
            )
            await self.db.flush()
            audit = await self._mutation_audit_event(
                principal=actor,
                command=command,
                operation="model_binding.disable",
                target_type="model_binding",
                target_id=binding.id,
                authoritative_revision=binding.revision,
                invalidated_assignment_ids=[
                    assignment.id for assignment in assignments
                ],
            )
            await self.db.flush()
            binding = await self._binding(binding.id)
            assert binding is not None
            counts = await self._binding_reference_counts([binding.id])
            return _MutationResult(
                target_type="model_binding",
                target_id=binding.id,
                authoritative_revision=binding.revision,
                result=self.binding_response(
                    binding,
                    reference_counts=counts.get(binding.id, (0, 0, 0)),
                ).model_dump(mode="json"),
                invalidated_assignment_ids=tuple(
                    assignment.id for assignment in assignments
                ),
                audit_event_ids=tuple(
                    sorted(
                        [audit.id, *(event.id for event in invalidation_events)]
                    )
                ),
            )

        return await self._execute(
            actor=actor,
            operation="model_binding.disable",
            target_type="model_binding",
            idempotency_target_id=binding_id,
            command=command,
            request_payload=request_payload,
            mutate=mutate,
        )
