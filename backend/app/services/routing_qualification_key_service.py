"""The deployment's governed registry of qualification keys.

An operator declares, revises and retires keys here. Each change is one
replay-safe command with a reason, an append-only revision row and an audit
event. Catalog entries and task routing requirements may then name a declared
key beside the built-in routing skill keys, which stay fixed in code.
"""

from __future__ import annotations

import json
from collections.abc import Iterable

from sqlalchemy import String, bindparam, cast, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.authority import internal_authority
from app.models.agent import (
    AgentActor,
    AgentModelCatalogEntry,
    TaskEvent,
    TaskRoutingAssessment,
)
from app.models.routing_qualification import (
    RoutingQualificationKey,
    RoutingQualificationKeyRevision,
)
from app.models.task import Task
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_routing import AgentModelMutationReceipt
from app.schemas.routing_qualification import (
    MAX_QUALIFICATION_KEY_USAGE_ITEMS,
    QualificationKeyCatalogReference,
    RoutingQualificationKeyDeclare,
    RoutingQualificationKeyDetail,
    RoutingQualificationKeyRegistryResponse,
    RoutingQualificationKeyResponse,
    RoutingQualificationKeyRetire,
    RoutingQualificationKeyRevise,
    RoutingQualificationKeyRevisionResponse,
    RoutingQualificationKeyUsage,
)
from app.services.agent_model_catalog_service import (
    AgentModelCatalogService,
    AgentModelConflictError,
    _MutationResult,
)
from app.services.agent_service import require_scope
from app.services.agent_routing_policy import (
    ROUTING_POLICY_VERSION,
    ROUTING_SKILL_KEYS,
    require_known_routing_keys,
)
from app.utils.time import utc_now


TARGET_TYPE = "routing_qualification_key"


async def _lock_keys(db: AsyncSession, names: Iterable[str]) -> None:
    """Take SQLite's database write lock before reading the named keys.

    SQLite has no row locks, so a no-op write makes a concurrent writer wait
    until this transaction ends; the read that follows then sees settled rows.
    """

    names = sorted(set(names))
    if not names or db.get_bind().dialect.name != "sqlite":
        return
    # The statement carries no caller data and changes nothing, so it runs
    # outside the caller's project scope, which refuses unscoped text writes.
    with internal_authority(db.sync_session):
        await db.execute(
            text("UPDATE routing_qualification_keys SET id = id WHERE key IN :names").bindparams(
                bindparam("names", expanding=True)
            ),
            {"names": names},
        )


async def active_qualification_keys(
    db: AsyncSession,
    keys: Iterable[str] | None = None,
    *,
    lock: bool = False,
) -> frozenset[str]:
    """Return active declared keys, optionally only those named and share-locked.

    The lock keeps a concurrent retire from removing a key that the caller is
    about to reference.
    """

    query = select(RoutingQualificationKey.id, RoutingQualificationKey.key).where(
        RoutingQualificationKey.state == "active"
    )
    if keys is not None:
        names = sorted({str(key).strip().lower() for key in keys})
        if not names:
            return frozenset()
        query = query.where(RoutingQualificationKey.key.in_(names))
        if lock:
            await _lock_keys(db, names)
    if lock and db.get_bind().dialect.name != "sqlite":
        query = query.with_for_update(read=True)
    rows = (await db.execute(query)).all()
    return frozenset(row.key for row in rows)


async def require_known_qualification_keys(
    db: AsyncSession,
    keys: Iterable[str],
    *,
    lock: bool = True,
) -> tuple[str, ...]:
    """Refuse a key that is neither built in nor declared and active.

    The refusal is the same ``Unknown routing skill key`` error routing has
    always given for a key outside its vocabulary.
    """

    names = tuple(sorted({str(key).strip().lower() for key in keys}))
    candidates = [key for key in names if key not in ROUTING_SKILL_KEYS]
    declared = (
        await active_qualification_keys(db, candidates, lock=lock)
        if candidates
        else frozenset()
    )
    return require_known_routing_keys(names, declared)


class RoutingQualificationKeyService:
    """Read the registry and run its deployment-operator commands.

    Writes use the same gate as the model catalog: the operator's admin key,
    or an agent key whose actor holds the ``admin`` scope where the workspace's
    authority mode lets an agent change deployment settings.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        # Shares the model catalog's operator command path: admin authority,
        # idempotency, replay-safe receipts and rollback on refusal.
        self._commands = AgentModelCatalogService(db)

    @staticmethod
    def _response(row: RoutingQualificationKey) -> RoutingQualificationKeyResponse:
        return RoutingQualificationKeyResponse.model_validate(row)

    async def _key(
        self,
        key: str,
        *,
        for_update: bool = False,
    ) -> RoutingQualificationKey | None:
        name = key.strip().lower()
        query = select(RoutingQualificationKey).where(RoutingQualificationKey.key == name)
        if for_update:
            await _lock_keys(self.db, [name])
            if self.db.get_bind().dialect.name != "sqlite":
                query = query.with_for_update()
            # Refresh an already loaded row with the locked values.
            query = query.execution_options(populate_existing=True)
        return (await self.db.execute(query)).scalar_one_or_none()

    async def list_registry(
        self,
        actor: AgentActor,
        *,
        include_retired: bool = False,
    ) -> RoutingQualificationKeyRegistryResponse:
        """List the built-in keys and the declared keys, active ones by default."""

        self._commands._require_read(actor)
        query = select(RoutingQualificationKey).order_by(RoutingQualificationKey.key)
        if not include_retired:
            query = query.where(RoutingQualificationKey.state == "active")
        rows = list((await self.db.execute(query.limit(MAX_BOUNDED_LIST_ITEMS + 1))).scalars())
        if len(rows) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError("routing qualification keys", MAX_BOUNDED_LIST_ITEMS)
        return RoutingQualificationKeyRegistryResponse(
            builtin_keys=sorted(ROUTING_SKILL_KEYS),
            keys=[self._response(row) for row in rows],
        )

    async def get_key(self, actor: AgentActor, key: str) -> RoutingQualificationKeyDetail:
        """Read one declared key with its revisions and what currently names it."""

        self._commands._require_read(actor)
        # Revisions are registry history, not the caller's data; reading them
        # inside the caller's scope would filter them by the actor that wrote them.
        with internal_authority(self.db.sync_session):
            row = (await self.db.execute(
                select(RoutingQualificationKey)
                .options(selectinload(RoutingQualificationKey.revisions))
                .where(RoutingQualificationKey.key == key.strip().lower())
            )).scalar_one_or_none()
        if row is None:
            raise LookupError("Qualification key not found")
        return RoutingQualificationKeyDetail(
            **self._response(row).model_dump(),
            revisions=[
                RoutingQualificationKeyRevisionResponse.model_validate(revision)
                for revision in row.revisions
            ],
            usage=await self.usage(row.key),
        )

    async def usage(self, key: str) -> RoutingQualificationKeyUsage:
        """Catalog entries holding the key and open tasks requiring it, as visible to the caller.

        Tasks outside the caller's project scope are not listed or counted.
        """

        return self._bounded_usage(*await self._references(key))

    async def _references(self, key: str) -> tuple[list[AgentModelCatalogEntry], list[int]]:
        name = key.strip().lower()
        entries = [
            entry
            for entry in (await self.db.execute(
                select(AgentModelCatalogEntry).order_by(AgentModelCatalogEntry.key)
            )).scalars()
            if name in (entry.qualification_keys or [])
        ]
        # The JSON text match narrows the scan; the decoded field decides.
        assessments = (await self.db.execute(
            select(TaskRoutingAssessment.task_id, TaskRoutingAssessment.required_model)
            .join(Task, Task.id == TaskRoutingAssessment.task_id)
            .where(
                TaskRoutingAssessment.task_version == Task.version,
                TaskRoutingAssessment.policy_version == ROUTING_POLICY_VERSION,
                Task.status != "closed",
                cast(TaskRoutingAssessment.required_model, String).like(f'%"{name}"%'),
            )
            .order_by(TaskRoutingAssessment.task_id)
        )).all()
        task_ids = sorted({
            row.task_id
            for row in assessments
            if name in ((row.required_model or {}).get("qualification_keys") or [])
        })
        return entries, task_ids

    @staticmethod
    def _bounded_usage(
        entries: list[AgentModelCatalogEntry],
        task_ids: list[int],
        *,
        total_entries: int | None = None,
        total_tasks: int | None = None,
    ) -> RoutingQualificationKeyUsage:
        limit = MAX_QUALIFICATION_KEY_USAGE_ITEMS
        total_entries = len(entries) if total_entries is None else total_entries
        total_tasks = len(task_ids) if total_tasks is None else total_tasks
        return RoutingQualificationKeyUsage(
            catalog_entries=[
                QualificationKeyCatalogReference(id=entry.id, key=entry.key, enabled=entry.enabled)
                for entry in entries[:limit]
            ],
            task_ids=task_ids[:limit],
            catalog_entries_omitted=max(total_entries - min(len(entries), limit), 0),
            task_ids_omitted=max(total_tasks - min(len(task_ids), limit), 0),
        )

    async def _retire_usage(self, key: str) -> RoutingQualificationKeyUsage:
        """Usage that decides a retire: every reference counts, but only visible tasks are named."""

        with internal_authority(self.db.sync_session):
            all_entries, all_tasks = await self._references(key)
        _, visible_tasks = await self._references(key)
        return self._bounded_usage(
            all_entries,
            [task_id for task_id in visible_tasks if task_id in set(all_tasks)],
            total_tasks=len(all_tasks),
        )

    def _record(
        self,
        row: RoutingQualificationKey,
        *,
        action: str,
        principal: AgentActor,
        command: AgentPlanningCommandContext,
        operation: str,
    ) -> TaskEvent:
        audit_actor = self._commands._audit_actor(principal)
        self.db.add(
            RoutingQualificationKeyRevision(
                qualification_key=row,
                revision=row.revision,
                action=action,
                state=row.state,
                label=row.label,
                description=row.description,
                reason=command.rationale,
                correlation_id=command.correlation_id,
                **audit_actor,
            )
        )
        event = TaskEvent(
            task_id=None,
            **audit_actor,
            event_type="agent.routing_qualification_key_changed",
            payload=json.dumps(
                {
                    "operation": operation,
                    "target_type": TARGET_TYPE,
                    "key": row.key,
                    "action": action,
                    "state": row.state,
                    "authoritative_revision": row.revision,
                    "label": row.label,
                    "description": row.description,
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

    async def _result(self, row: RoutingQualificationKey, event: TaskEvent) -> _MutationResult:
        await self.db.flush()
        return _MutationResult(
            target_type=TARGET_TYPE,
            target_id=row.id,
            authoritative_revision=row.revision,
            result=self._response(row).model_dump(mode="json"),
            audit_event_ids=(event.id,),
        )

    @staticmethod
    def _require_revision(row: RoutingQualificationKey, expected: int) -> None:
        if row.revision != expected:
            raise AgentModelConflictError(
                "routing_qualification_key_revision_conflict",
                "Qualification key revision is stale",
                key=row.key,
                expected_revision=expected,
                current_revision=row.revision,
            )

    async def declare(
        self,
        actor: AgentActor,
        data: RoutingQualificationKeyDeclare,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Declare a key, or bring back a retired one as its next revision."""

        require_scope(actor, "admin")
        operation = "routing_qualification_key.declare"

        async def mutate() -> _MutationResult:
            if data.key in ROUTING_SKILL_KEYS:
                raise AgentModelConflictError(
                    "routing_qualification_key_builtin",
                    "A built-in routing skill key cannot be declared",
                    key=data.key,
                )
            row = await self._key(data.key, for_update=True)
            if row is not None and row.state == "active":
                raise AgentModelConflictError(
                    "routing_qualification_key_exists",
                    "Qualification key is already declared",
                    key=data.key,
                    current_revision=row.revision,
                )
            if row is None:
                row = RoutingQualificationKey(
                    key=data.key,
                    label=data.label,
                    description=data.description,
                    state="active",
                    revision=1,
                )
                self.db.add(row)
            else:
                row.label = data.label
                row.description = data.description
                row.state = "active"
                row.retired_at = None
                row.revision += 1
            await self.db.flush()
            event = self._record(row, action="declare", principal=actor, command=command, operation=operation)
            return await self._result(row, event)

        return await self._commands._execute(
            actor=actor,
            operation=operation,
            target_type=TARGET_TYPE,
            idempotency_target_id=0,
            command=command,
            request_payload=self._commands._audited_request(data, command),
            mutate=mutate,
            integrity_conflict=lambda: AgentModelConflictError(
                "routing_qualification_key_exists",
                "Qualification key was declared by a concurrent command",
                key=data.key,
            ),
        )

    @staticmethod
    def _concurrent_revision(key: str) -> AgentModelConflictError:
        return AgentModelConflictError(
            "routing_qualification_key_revision_conflict",
            "Qualification key was changed by a concurrent command",
            key=key.strip().lower(),
        )

    async def _target_id(self, key: str) -> int:
        row = await self._key(key)
        if row is None:
            raise LookupError("Qualification key not found")
        return row.id

    async def revise(
        self,
        key: str,
        actor: AgentActor,
        data: RoutingQualificationKeyRevise,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Change an active key's label or description as its next revision."""

        require_scope(actor, "admin")
        operation = "routing_qualification_key.revise"
        target_id = await self._target_id(key)

        async def mutate() -> _MutationResult:
            row = await self._key(key, for_update=True)
            if row is None:
                raise LookupError("Qualification key not found")
            self._require_revision(row, data.expected_revision)
            if row.state != "active":
                raise AgentModelConflictError(
                    "routing_qualification_key_retired",
                    "A retired qualification key cannot be revised; declare it again",
                    key=row.key,
                )
            updates = data.model_dump(exclude_unset=True, exclude={"expected_revision"})
            if all(getattr(row, field) == value for field, value in updates.items()):
                raise AgentModelConflictError(
                    "routing_qualification_key_no_change",
                    "Qualification key revision does not change its label or description",
                    key=row.key,
                )
            for field, value in updates.items():
                setattr(row, field, value)
            row.revision += 1
            event = self._record(row, action="revise", principal=actor, command=command, operation=operation)
            return await self._result(row, event)

        return await self._commands._execute(
            actor=actor,
            operation=operation,
            target_type=TARGET_TYPE,
            idempotency_target_id=target_id,
            command=command,
            request_payload=self._commands._audited_request(data, command),
            mutate=mutate,
            integrity_conflict=lambda: self._concurrent_revision(key),
        )

    async def retire(
        self,
        key: str,
        actor: AgentActor,
        data: RoutingQualificationKeyRetire,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Retire a key that no catalog entry or open task requirement names."""

        require_scope(actor, "admin")
        operation = "routing_qualification_key.retire"
        target_id = await self._target_id(key)

        async def mutate() -> _MutationResult:
            row = await self._key(key, for_update=True)
            if row is None:
                raise LookupError("Qualification key not found")
            self._require_revision(row, data.expected_revision)
            if row.state != "active":
                raise AgentModelConflictError(
                    "routing_qualification_key_retired",
                    "Qualification key is already retired",
                    key=row.key,
                )
            usage = await self._retire_usage(row.key)
            if usage.in_use:
                raise AgentModelConflictError(
                    "routing_qualification_key_in_use",
                    "Qualification key is held by catalog entries or required by open tasks; "
                    "remove it from them first",
                    key=row.key,
                    **usage.model_dump(mode="json"),
                )
            row.state = "retired"
            row.retired_at = utc_now()
            row.revision += 1
            event = self._record(row, action="retire", principal=actor, command=command, operation=operation)
            return await self._result(row, event)

        return await self._commands._execute(
            actor=actor,
            operation=operation,
            target_type=TARGET_TYPE,
            idempotency_target_id=target_id,
            command=command,
            request_payload=self._commands._audited_request(data, command),
            mutate=mutate,
            integrity_conflict=lambda: self._concurrent_revision(key),
        )
