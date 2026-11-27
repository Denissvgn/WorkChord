"""The deployment's calibration contracts for performance-informed routing.

An operator submits a contract's complete terms and an operator approves
them as the contract's declared approver. Each command is replay-safe, carries a reason, adds
an append-only revision row and records an audit event. Routing consumes no
performance history: it only reports whether an approved contract exists.
"""

from __future__ import annotations

import json
from datetime import timedelta

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.authority import internal_authority
from app.models.agent import AgentActor, TaskEvent
from app.models.routing_calibration import (
    RoutingCalibrationContract,
    RoutingCalibrationContractRevision,
)
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_routing import AgentModelMutationReceipt
from app.schemas.routing_calibration import (
    CALIBRATION_CONTRACT_SCHEMA_VERSION,
    RoutingCalibrationContractApprove,
    RoutingCalibrationContractDetail,
    RoutingCalibrationContractListResponse,
    RoutingCalibrationContractResponse,
    RoutingCalibrationContractRevise,
    RoutingCalibrationContractRevisionResponse,
    RoutingCalibrationContractSubmit,
    RoutingCalibrationContractTerms,
)
from app.services.agent_model_catalog_service import (
    AgentModelCatalogService,
    AgentModelConflictError,
    _MutationResult,
)
from app.services.agent_routing_policy import RoutingTermsRefusedError
from app.services.agent_service import require_scope
from app.services.routing_qualification_key_service import require_known_qualification_keys
from app.utils.time import utc_now


TARGET_TYPE = "routing_calibration_contract"
# Clock skew tolerated between the bias reviewer's record and this server.
_REVIEW_CLOCK_SKEW = timedelta(minutes=5)


async def approved_calibration_contract_count(db: AsyncSession) -> int:
    """How many contracts are currently approved; routing reads nothing else from them."""

    return int(await db.scalar(
        select(func.count()).select_from(RoutingCalibrationContract).where(
            RoutingCalibrationContract.state == "approved"
        )
    ) or 0)


class RoutingCalibrationContractService:
    """Read contracts and run their deployment-operator commands.

    Writes use the model catalog's gate: the operator's admin key, or an agent
    key whose actor holds the ``admin`` scope where the workspace's authority
    mode lets an agent change deployment settings.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        # Shares the model catalog's operator command path: admin authority,
        # idempotency, replay-safe receipts and rollback on refusal.
        self._commands = AgentModelCatalogService(db)

    @staticmethod
    def _response(row: RoutingCalibrationContract) -> RoutingCalibrationContractResponse:
        return RoutingCalibrationContractResponse.from_record(row)

    async def _contract(self, key: str, *, for_update: bool = False) -> RoutingCalibrationContract | None:
        name = key.strip().lower()
        query = select(RoutingCalibrationContract).where(RoutingCalibrationContract.key == name)
        if for_update:
            if self.db.get_bind().dialect.name == "sqlite":
                # SQLite has no row locks; a no-op write takes the database
                # write lock so a concurrent command waits for this one. It
                # carries no caller data and runs outside the caller's scope,
                # which refuses unscoped text writes.
                with internal_authority(self.db.sync_session):
                    await self.db.execute(
                        text("UPDATE routing_calibration_contracts SET id = id WHERE key = :key"),
                        {"key": name},
                    )
            else:
                query = query.with_for_update()
            query = query.execution_options(populate_existing=True)
        return (await self.db.execute(query)).scalar_one_or_none()

    async def list_contracts(self, actor: AgentActor) -> RoutingCalibrationContractListResponse:
        """List every contract and state whether any is approved."""

        self._commands._require_read(actor)
        rows = list((await self.db.execute(
            select(RoutingCalibrationContract)
            .order_by(RoutingCalibrationContract.key)
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )).scalars())
        if len(rows) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError("routing calibration contracts", MAX_BOUNDED_LIST_ITEMS)
        return RoutingCalibrationContractListResponse(
            approved_contract_exists=await approved_calibration_contract_count(self.db) > 0,
            contracts=[self._response(row) for row in rows],
        )

    async def get_contract(self, actor: AgentActor, key: str) -> RoutingCalibrationContractDetail:
        """Read one contract with every revision it has had."""

        self._commands._require_read(actor)
        # Revisions are deployment history, not the caller's data; reading them
        # inside the caller's scope would filter them by the actor that wrote them.
        with internal_authority(self.db.sync_session):
            row = (await self.db.execute(
                select(RoutingCalibrationContract)
                .options(selectinload(RoutingCalibrationContract.revisions))
                .where(RoutingCalibrationContract.key == key.strip().lower())
            )).scalar_one_or_none()
        if row is None:
            raise LookupError("Calibration contract not found")
        return RoutingCalibrationContractDetail(
            **self._response(row).model_dump(),
            revisions=[
                RoutingCalibrationContractRevisionResponse.model_validate(revision)
                for revision in row.revisions
            ],
        )

    async def _validated_terms(self, data: RoutingCalibrationContractTerms) -> RoutingCalibrationContractTerms:
        """Refuse unknown or retired keys and a bias review dated in the future."""

        terms = RoutingCalibrationContractTerms.model_validate(
            data.model_dump(include=set(RoutingCalibrationContractTerms.model_fields))
        )
        await require_known_qualification_keys(self.db, terms.qualification_keys)
        if terms.bias_review.reviewed_at > utc_now() + _REVIEW_CLOCK_SKEW:
            raise RoutingTermsRefusedError("bias_review.reviewed_at must not be in the future")
        return terms

    def _record(
        self,
        row: RoutingCalibrationContract,
        *,
        action: str,
        principal: AgentActor,
        command: AgentPlanningCommandContext,
        operation: str,
    ) -> TaskEvent:
        audit_actor = self._commands._audit_actor(principal)
        self.db.add(
            RoutingCalibrationContractRevision(
                contract=row,
                revision=row.revision,
                action=action,
                state=row.state,
                terms=row.terms,
                terms_digest=row.terms_digest,
                reason=command.rationale,
                approved_as=row.approved_as if action == "approve" else None,
                correlation_id=command.correlation_id,
                **audit_actor,
            )
        )
        event = TaskEvent(
            task_id=None,
            **audit_actor,
            event_type="agent.routing_calibration_contract_changed",
            payload=json.dumps(
                {
                    "operation": operation,
                    "target_type": TARGET_TYPE,
                    "key": row.key,
                    "action": action,
                    "state": row.state,
                    "authoritative_revision": row.revision,
                    "terms_digest": row.terms_digest,
                    "approved_as": row.approved_as,
                    "qualification_keys": row.terms.get("qualification_keys", []),
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

    async def _result(self, row: RoutingCalibrationContract, event: TaskEvent) -> _MutationResult:
        await self.db.flush()
        return _MutationResult(
            target_type=TARGET_TYPE,
            target_id=row.id,
            authoritative_revision=row.revision,
            result=self._response(row).model_dump(mode="json"),
            audit_event_ids=(event.id,),
        )

    @staticmethod
    def _require_revision(row: RoutingCalibrationContract, expected: int) -> None:
        if row.revision != expected:
            raise AgentModelConflictError(
                "routing_calibration_contract_revision_conflict",
                "Calibration contract revision is stale",
                key=row.key,
                expected_revision=expected,
                current_revision=row.revision,
            )

    @staticmethod
    def _concurrent_revision(key: str) -> AgentModelConflictError:
        return AgentModelConflictError(
            "routing_calibration_contract_revision_conflict",
            "Calibration contract was changed by a concurrent command",
            key=key.strip().lower(),
        )

    def _submitted_by(self, row: RoutingCalibrationContract, principal: AgentActor) -> None:
        audit_actor = self._commands._audit_actor(principal)
        row.submitted_by_actor_type = audit_actor["actor_type"]
        row.submitted_by_actor_id = audit_actor["actor_id"]
        row.submitted_at = utc_now()

    async def _target_id(self, key: str) -> int:
        row = await self._contract(key)
        if row is None:
            raise LookupError("Calibration contract not found")
        return row.id

    async def submit(
        self,
        actor: AgentActor,
        data: RoutingCalibrationContractSubmit,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Submit a new contract; it stays unapproved until another principal approves it."""

        require_scope(actor, "admin")
        operation = "routing_calibration_contract.submit"

        async def mutate() -> _MutationResult:
            terms = await self._validated_terms(data)
            existing = await self._contract(data.key, for_update=True)
            if existing is not None:
                raise AgentModelConflictError(
                    "routing_calibration_contract_exists",
                    "Calibration contract already exists; submit a revision with its current revision",
                    key=data.key,
                    current_revision=existing.revision,
                )
            row = RoutingCalibrationContract(
                key=data.key,
                schema_version=CALIBRATION_CONTRACT_SCHEMA_VERSION,
                state="submitted",
                revision=1,
                terms=terms.stored(),
                terms_digest=terms.digest(),
            )
            self._submitted_by(row, actor)
            self.db.add(row)
            await self.db.flush()
            event = self._record(row, action="submit", principal=actor, command=command, operation=operation)
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
                "routing_calibration_contract_exists",
                "Calibration contract was submitted by a concurrent command",
                key=data.key,
            ),
        )

    async def revise(
        self,
        key: str,
        actor: AgentActor,
        data: RoutingCalibrationContractRevise,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Submit complete new terms as the next revision; an earlier approval lapses."""

        require_scope(actor, "admin")
        operation = "routing_calibration_contract.revise"
        target_id = await self._target_id(key)

        async def mutate() -> _MutationResult:
            terms = await self._validated_terms(data)
            row = await self._contract(key, for_update=True)
            if row is None:
                raise LookupError("Calibration contract not found")
            self._require_revision(row, data.expected_revision)
            digest = terms.digest()
            if digest == row.terms_digest and row.state == "submitted":
                raise AgentModelConflictError(
                    "routing_calibration_contract_no_change",
                    "Calibration contract revision does not change its submitted terms",
                    key=row.key,
                )
            row.terms = terms.stored()
            row.terms_digest = digest
            row.state = "submitted"
            row.approved_by_actor_type = None
            row.approved_by_actor_id = None
            row.approved_at = None
            row.approval_reason = None
            row.approved_as = None
            self._submitted_by(row, actor)
            row.revision += 1
            event = self._record(row, action="submit", principal=actor, command=command, operation=operation)
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

    async def approve(
        self,
        key: str,
        actor: AgentActor,
        data: RoutingCalibrationContractApprove,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentModelMutationReceipt:
        """Approve the submitted terms as their declared approver, recording who authenticated."""

        require_scope(actor, "admin")
        operation = "routing_calibration_contract.approve"
        target_id = await self._target_id(key)

        async def mutate() -> _MutationResult:
            row = await self._contract(key, for_update=True)
            if row is None:
                raise LookupError("Calibration contract not found")
            self._require_revision(row, data.expected_revision)
            if row.state == "approved":
                raise AgentModelConflictError(
                    "routing_calibration_contract_already_approved",
                    "Calibration contract revision is already approved",
                    key=row.key,
                    current_revision=row.revision,
                )
            if row.terms_digest != data.expected_terms_digest:
                raise AgentModelConflictError(
                    "routing_calibration_contract_terms_mismatch",
                    "The approval names terms other than the submitted ones",
                    key=row.key,
                    current_terms_digest=row.terms_digest,
                )
            declared = row.terms.get("approver")
            if data.approved_as != declared:
                raise AgentModelConflictError(
                    "routing_calibration_contract_approver_mismatch",
                    "The approval must be given as the contract's declared approver",
                    key=row.key,
                    approver=declared,
                )
            audit_actor = self._commands._audit_actor(actor)
            # Keys retired since submission would make the terms unenforceable.
            await require_known_qualification_keys(self.db, row.terms.get("qualification_keys", []))
            row.state = "approved"
            row.approved_by_actor_type = audit_actor["actor_type"]
            row.approved_by_actor_id = audit_actor["actor_id"]
            row.approved_at = utc_now()
            row.approval_reason = command.rationale
            row.approved_as = data.approved_as
            row.revision += 1
            event = self._record(row, action="approve", principal=actor, command=command, operation=operation)
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
