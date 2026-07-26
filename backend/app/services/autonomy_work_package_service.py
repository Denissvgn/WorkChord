"""Fenced, package-level autonomous verification lifecycle service."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.autonomy.canonical import sha256_hex
from app.models.agent import AgentActor
from app.models.autonomy import (
    AgentAutonomyTopology,
    AgentAutonomyTopologyMember,
    AgentVerificationEvent,
    AgentVerificationRequirement,
    AgentWorkPackage,
)
from app.schemas.autonomy import (
    AgentWorkPackageCreate,
    AgentWorkPackageResponse,
    ResolvedVerifierLease,
    VerificationBeginRequest,
    VerificationClaimRequest,
    VerificationRenewRequest,
    VerificationRequirementResponse,
    VerificationSubmitRequest,
    VerificationTransitionResponse,
)
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    actor_has_scope,
    validate_idempotency_key,
)
from app.utils.time import as_utc, utc_now


ZERO_DIGEST = "0" * 64


class AutonomyWorkPackageService:
    """Mirror external-journal decisions without letting Task.status accept work."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_package(
        self,
        controller: AgentActor,
        data: AgentWorkPackageCreate,
    ) -> AgentWorkPackageResponse:
        self._require_controller(controller)
        existing = await self.db.scalar(
            select(AgentWorkPackage)
            .options(selectinload(AgentWorkPackage.requirements))
            .where(
                AgentWorkPackage.package_key == data.package_key,
                AgentWorkPackage.package_version == data.package_version,
            )
        )
        if existing is not None:
            if existing.creation_request_digest != self._request_fingerprint(data):
                raise AgentConflictError("Package key/version already has different inputs")
            return self.package_response(existing)
        if data.predecessor_package_id is not None:
            predecessor = await self.db.get(AgentWorkPackage, data.predecessor_package_id)
            if predecessor is None or predecessor.state != "rework_required":
                raise AgentConflictError(
                    "Successor package requires a rework_required predecessor"
                )
            if predecessor.package_key != data.package_key:
                raise AgentConflictError("Successor package key differs from predecessor")
            if data.package_version != predecessor.package_version + 1:
                raise AgentConflictError("Successor package version must increment by one")
        package = AgentWorkPackage(
            package_key=data.package_key,
            package_version=data.package_version,
            execution_task_id=data.execution_task_id,
            predecessor_package_id=data.predecessor_package_id,
            state="planned",
            artifact_set_digest=data.artifact_set_digest,
            contract_manifest_digest=data.contract_manifest_digest,
            source_contract_digest=data.source_contract_digest,
            creation_request_digest=self._request_fingerprint(data),
            external_journal_revision=data.external_journal_revision,
            external_journal_head_digest=data.external_journal_head_digest,
        )
        self.db.add(package)
        await self.db.flush()
        for requirement in data.requirements:
            self.db.add(
                AgentVerificationRequirement(
                    package_id=package.id,
                    slot_key=requirement.slot_key,
                    verifier_logical_key=requirement.verifier_logical_key,
                    state="planned",
                    criterion_schema=requirement.criterion_schema,
                    artifact_set_digest=data.artifact_set_digest,
                    evaluator_version=requirement.evaluator_version,
                    executor_independence_group=requirement.executor_independence_group,
                    verifier_independence_group=requirement.verifier_independence_group,
                )
            )
        await self.db.commit()
        return self.package_response(await self._load_package(package.id))

    async def activate_requirements(
        self,
        controller: AgentActor,
        *,
        package_id: int,
        external_journal_revision: int,
        external_journal_head_digest: str,
        idempotency_key: str,
    ) -> AgentWorkPackageResponse:
        self._require_controller(controller)
        key = validate_idempotency_key(idempotency_key, required=True)
        assert key is not None
        package = await self._lock_package(package_id)
        payload = {
            "operation": "activate-requirements",
            "package_id": package_id,
            "external_journal_revision": external_journal_revision,
            "external_journal_head_digest": external_journal_head_digest,
        }
        payload_digest = sha256_hex(payload)
        requirements = await self._lock_requirements(package.id)
        replayed = await self._matching_event(requirements, key, payload_digest)
        if replayed:
            return self.package_response(await self._load_package(package.id))
        self._advance_journal(
            package,
            revision=external_journal_revision,
            head_digest=external_journal_head_digest,
        )
        if package.state != "planned" or any(item.state != "planned" for item in requirements):
            raise AgentConflictError("Only a fully planned package may become ready")
        for requirement in requirements:
            requirement.state = "ready"
            await self._append_event(
                requirement,
                event_type="verification.ready",
                actor_id=controller.id,
                payload_digest=payload_digest,
                idempotency_key=self._child_key(key, requirement.slot_key),
            )
        package.state = "evaluating"
        await self.db.commit()
        return self.package_response(await self._load_package(package.id))

    async def claim_requirement(
        self,
        actor: AgentActor,
        data: VerificationClaimRequest,
        *,
        resolved_lease: ResolvedVerifierLease,
        idempotency_key: str,
    ) -> VerificationTransitionResponse:
        self._require_verifier(actor)
        key = self._idempotency(idempotency_key)
        requirement = await self._lock_requirement(data.requirement_id)
        package = await self._lock_package(requirement.package_id)
        payload_digest = sha256_hex(
            {
                "operation": "claim",
                "request": data.model_dump(mode="json"),
                "lease": resolved_lease.model_dump(mode="json"),
            }
        )
        if await self._event_replay(requirement, key, payload_digest):
            return self.transition_response(requirement, package)
        self._validate_lease(
            actor,
            requirement,
            package,
            resolved_lease,
            expected_action="verification-claim",
        )
        await self._require_topology_member(actor, requirement, resolved_lease)
        if package.package_version != data.expected_package_version:
            raise AgentConflictError("Package version is stale")
        if package.artifact_set_digest != data.expected_artifact_set_digest:
            raise AgentConflictError("Package artifact set is stale")
        if requirement.state != "ready":
            raise AgentConflictError("Verification requirement is not ready")
        self._advance_journal(
            package,
            revision=data.external_journal_revision,
            head_digest=data.external_journal_head_digest,
        )
        requirement.assigned_verifier_actor_id = actor.id
        requirement.state = "claimed"
        self._adopt_lease(requirement, resolved_lease)
        await self._append_event(
            requirement,
            event_type="verification.claimed",
            actor_id=actor.id,
            payload_digest=payload_digest,
            idempotency_key=key,
        )
        await self.db.commit()
        return self.transition_response(
            await self._load_requirement(requirement.id),
            await self._load_package(package.id),
        )

    async def begin_requirement(
        self,
        actor: AgentActor,
        data: VerificationBeginRequest,
        *,
        resolved_lease: ResolvedVerifierLease,
        idempotency_key: str,
    ) -> VerificationTransitionResponse:
        return await self._lease_transition(
            actor,
            data=data,
            resolved_lease=resolved_lease,
            idempotency_key=idempotency_key,
            expected_state="claimed",
            next_state="running",
            expected_action="verification-begin",
            event_type="verification.began",
        )

    async def renew_requirement(
        self,
        actor: AgentActor,
        data: VerificationRenewRequest,
        *,
        resolved_lease: ResolvedVerifierLease,
        idempotency_key: str,
    ) -> VerificationTransitionResponse:
        return await self._lease_transition(
            actor,
            data=data,
            resolved_lease=resolved_lease,
            idempotency_key=idempotency_key,
            expected_state="running",
            next_state="running",
            expected_action="verification-renew",
            event_type="verification.renewed",
        )

    async def submit_requirement(
        self,
        actor: AgentActor,
        data: VerificationSubmitRequest,
        *,
        resolved_lease: ResolvedVerifierLease,
        idempotency_key: str,
    ) -> VerificationTransitionResponse:
        self._require_verifier(actor)
        key = self._idempotency(idempotency_key)
        requirement = await self._lock_requirement(data.requirement_id)
        package = await self._lock_package(requirement.package_id)
        payload = {
            "operation": "submit",
            "request": data.model_dump(mode="json"),
            "lease": resolved_lease.model_dump(mode="json"),
        }
        payload_digest = sha256_hex(payload)
        if await self._event_replay(requirement, key, payload_digest):
            verdict = "passed" if requirement.state == "passed" else "rejected"
            return self.transition_response(requirement, package, verdict=verdict)
        self._validate_owned_fence(actor, requirement, data)
        self._validate_lease(
            actor,
            requirement,
            package,
            resolved_lease,
            expected_action="verification-submit",
        )
        await self._require_topology_member(actor, requirement, resolved_lease)
        if requirement.state != "running":
            raise AgentConflictError("Verification requirement is not running")
        self._require_unexpired(requirement)
        if data.artifact_set_digest != requirement.artifact_set_digest:
            raise AgentConflictError("Verifier submitted another artifact set")
        self._advance_journal(
            package,
            revision=data.external_journal_revision,
            head_digest=data.external_journal_head_digest,
        )
        verdict = (
            "rejected"
            if any(item.outcome == "failed" for item in data.criterion_results)
            else "passed"
        )
        requirement.state = verdict
        self._adopt_lease(requirement, resolved_lease)
        requirement.heartbeat_at = utc_now()
        requirement.evidence_digest = sha256_hex(
            [item.evidence_object_digest for item in data.criterion_results]
        )
        requirement.verdict_digest = sha256_hex(
            {
                "artifact_set_digest": data.artifact_set_digest,
                "criterion_results": [
                    item.model_dump(mode="json") for item in data.criterion_results
                ],
                "evaluator_attestation_digest": data.evaluator_attestation_digest,
                "verdict": verdict,
            }
        )
        await self._append_event(
            requirement,
            event_type=f"verification.{verdict}",
            actor_id=actor.id,
            payload_digest=payload_digest,
            idempotency_key=key,
        )
        requirements = await self._lock_requirements(package.id)
        if verdict == "rejected":
            for sibling in requirements:
                if sibling.id == requirement.id or sibling.state in {
                    "rejected",
                    "expired",
                }:
                    continue
                sibling.state = "expired"
                await self._append_event(
                    sibling,
                    event_type="verification.sibling_invalidated",
                    actor_id=None,
                    payload_digest=payload_digest,
                    idempotency_key=self._child_key(
                        key, f"invalidate:{sibling.slot_key}"
                    ),
                )
            package.state = "rework_required"
        elif all(item.state == "passed" for item in requirements):
            package.state = "passed"
        else:
            package.state = "evaluating"
        await self.db.commit()
        return self.transition_response(
            await self._load_requirement(requirement.id),
            await self._load_package(package.id),
            verdict=verdict,
        )

    async def expire_leases(
        self,
        *,
        observed_at: datetime,
        external_journal_revision: int,
        external_journal_head_digest: str,
    ) -> tuple[int, ...]:
        """Expire every overdue live slot; caller first commits one journal event."""

        if observed_at.tzinfo is None or observed_at.utcoffset() is None:
            raise ValueError("Lease-expiry observation must be timezone-aware")
        result = await self.db.execute(
            select(AgentVerificationRequirement)
            .where(
                AgentVerificationRequirement.state.in_(("claimed", "running")),
                AgentVerificationRequirement.lease_expires_at <= observed_at,
            )
            .with_for_update()
        )
        requirements = list(result.scalars().all())
        package_ids = sorted({item.package_id for item in requirements})
        expired: list[int] = []
        for package_id in package_ids:
            package = await self._lock_package(package_id)
            self._advance_journal(
                package,
                revision=external_journal_revision,
                head_digest=external_journal_head_digest,
                allow_equal=True,
            )
            for requirement in [item for item in requirements if item.package_id == package_id]:
                requirement.state = "expired"
                payload_digest = sha256_hex(
                    {
                        "operation": "expire",
                        "requirement_id": requirement.id,
                        "observed_at": observed_at,
                    }
                )
                await self._append_event(
                    requirement,
                    event_type="verification.expired",
                    actor_id=None,
                    payload_digest=payload_digest,
                    idempotency_key=f"expiry:{external_journal_revision}:{requirement.id}",
                )
                expired.append(requirement.id)
            package.state = "rework_required"
        await self.db.commit()
        return tuple(expired)

    async def _lease_transition(
        self,
        actor: AgentActor,
        *,
        data: VerificationBeginRequest | VerificationRenewRequest,
        resolved_lease: ResolvedVerifierLease,
        idempotency_key: str,
        expected_state: str,
        next_state: str,
        expected_action: str,
        event_type: str,
    ) -> VerificationTransitionResponse:
        self._require_verifier(actor)
        key = self._idempotency(idempotency_key)
        requirement = await self._lock_requirement(data.requirement_id)
        package = await self._lock_package(requirement.package_id)
        payload_digest = sha256_hex(
            {
                "operation": expected_action,
                "request": data.model_dump(mode="json"),
                "lease": resolved_lease.model_dump(mode="json"),
            }
        )
        if await self._event_replay(requirement, key, payload_digest):
            return self.transition_response(requirement, package)
        self._validate_owned_fence(actor, requirement, data)
        self._validate_lease(
            actor,
            requirement,
            package,
            resolved_lease,
            expected_action=expected_action,
        )
        member = await self._require_topology_member(
            actor, requirement, resolved_lease
        )
        if isinstance(data, VerificationBeginRequest) and (
            member.runtime_attestation_digest != data.runtime_attestation_digest
        ):
            raise AgentConflictError("Verifier runtime attestation drifted")
        if requirement.state != expected_state:
            raise AgentConflictError(
                f"Verification requirement must be {expected_state}"
            )
        self._require_unexpired(requirement)
        self._advance_journal(
            package,
            revision=data.external_journal_revision,
            head_digest=data.external_journal_head_digest,
        )
        requirement.state = next_state
        self._adopt_lease(requirement, resolved_lease)
        requirement.heartbeat_at = utc_now()
        await self._append_event(
            requirement,
            event_type=event_type,
            actor_id=actor.id,
            payload_digest=payload_digest,
            idempotency_key=key,
        )
        await self.db.commit()
        return self.transition_response(
            await self._load_requirement(requirement.id),
            await self._load_package(package.id),
        )

    async def _require_topology_member(
        self,
        actor: AgentActor,
        requirement: AgentVerificationRequirement,
        lease: ResolvedVerifierLease,
    ) -> AgentAutonomyTopologyMember:
        result = await self.db.execute(
            select(AgentAutonomyTopologyMember)
            .join(
                AgentAutonomyTopology,
                AgentAutonomyTopology.id == AgentAutonomyTopologyMember.topology_id,
            )
            .where(
                AgentAutonomyTopologyMember.actor_id == actor.id,
                AgentAutonomyTopologyMember.logical_key
                == requirement.verifier_logical_key,
                AgentAutonomyTopologyMember.lifecycle_state == "runtime_ready",
                AgentAutonomyTopology.state == "active",
                AgentAutonomyTopology.revision == lease.topology_revision,
            )
        )
        member = result.scalar_one_or_none()
        if member is None:
            raise AgentPermissionError(
                "Verifier is not runtime-ready in the exact active topology revision"
            )
        if member.independence_group != requirement.verifier_independence_group:
            raise AgentPermissionError("Verifier independence group drifted")
        return member

    @staticmethod
    def _require_controller(actor: AgentActor) -> None:
        if (
            not actor.enabled
            or actor.name != "pg-program-controller"
            or actor.role != "pm"
            or not actor_has_scope(actor, "planning:write")
        ):
            raise AgentPermissionError("Only pg-program-controller may project packages")

    @staticmethod
    def _require_verifier(actor: AgentActor) -> None:
        if (
            not actor.enabled
            or actor.role != "verifier"
            or not actor_has_scope(actor, "verification:write")
        ):
            raise AgentPermissionError("A current verifier identity is required")

    @staticmethod
    def _idempotency(value: str) -> str:
        key = validate_idempotency_key(value, required=True)
        assert key is not None
        return key

    @staticmethod
    def _child_key(parent: str, suffix: str) -> str:
        candidate = f"{parent}:{suffix}"
        if len(candidate) <= 255:
            return candidate
        return f"derived:{sha256_hex(candidate)}"

    @staticmethod
    def _validate_owned_fence(actor: AgentActor, requirement, data) -> None:
        if requirement.assigned_verifier_actor_id != actor.id:
            raise AgentPermissionError("Verification slot belongs to another actor")
        if requirement.lease_generation != data.expected_lease_generation:
            raise AgentConflictError("Verification lease generation is stale")
        if requirement.lease_digest != data.expected_lease_digest:
            raise AgentConflictError("Verification lease digest is stale")

    @staticmethod
    def _validate_lease(
        actor: AgentActor,
        requirement: AgentVerificationRequirement,
        package: AgentWorkPackage,
        lease: ResolvedVerifierLease,
        *,
        expected_action: str,
    ) -> None:
        now = utc_now()
        if lease.expires_at <= now or lease.issued_at > now:
            raise AgentConflictError("Resolved verifier action lease is not current")
        if lease.action != expected_action:
            raise AgentConflictError("Resolved verifier action lease has another action")
        if lease.actor_id != actor.id:
            raise AgentPermissionError("Resolved verifier action lease has another actor")
        if lease.actor_logical_key != requirement.verifier_logical_key:
            raise AgentPermissionError("Resolved verifier action lease has another logical key")
        if lease.task_id != package.package_key or lease.stage_id != requirement.slot_key:
            raise AgentConflictError("Resolved verifier action lease has another package/slot")
        if (
            requirement.attempt_start_digest is not None
            and lease.attempt_start_digest != requirement.attempt_start_digest
        ):
            raise AgentConflictError("Resolved verifier lease has another attempt start")

    @staticmethod
    def _require_unexpired(requirement: AgentVerificationRequirement) -> None:
        if requirement.lease_expires_at is None or as_utc(
            requirement.lease_expires_at
        ) <= utc_now():
            raise AgentConflictError("Verification lease expired")

    @staticmethod
    def _adopt_lease(
        requirement: AgentVerificationRequirement,
        lease: ResolvedVerifierLease,
    ) -> None:
        if requirement.attempt_start_digest is None:
            requirement.attempt_start_digest = lease.attempt_start_digest
        elif requirement.attempt_start_digest != lease.attempt_start_digest:
            raise AgentConflictError("Verification attempt ancestry changed")
        requirement.lease_generation += 1
        requirement.lease_digest = lease.lease_digest
        requirement.lease_expires_at = lease.expires_at

    @staticmethod
    def _advance_journal(
        package: AgentWorkPackage,
        *,
        revision: int,
        head_digest: str,
        allow_equal: bool = False,
    ) -> None:
        if head_digest == ZERO_DIGEST:
            raise AgentConflictError("External journal head cannot be the zero digest")
        minimum = package.external_journal_revision if allow_equal else package.external_journal_revision + 1
        if revision < minimum:
            raise AgentConflictError("External journal projection is stale")
        if revision == package.external_journal_revision and head_digest != package.external_journal_head_digest:
            raise AgentConflictError("External journal revision has conflicting heads")
        package.external_journal_revision = revision
        package.external_journal_head_digest = head_digest

    async def _append_event(
        self,
        requirement: AgentVerificationRequirement,
        *,
        event_type: str,
        actor_id: int | None,
        payload_digest: str,
        idempotency_key: str,
    ) -> AgentVerificationEvent:
        events = list(
            (
                await self.db.execute(
                    select(AgentVerificationEvent)
                    .where(
                        AgentVerificationEvent.requirement_id == requirement.id
                    )
                    .order_by(AgentVerificationEvent.sequence)
                )
            ).scalars().all()
        )
        sequence = len(events) + 1
        previous_hash = events[-1].event_digest if events else ZERO_DIGEST
        created_at = utc_now()
        digest_values = {
            "requirement_id": requirement.id,
            "sequence": sequence,
            "event_type": event_type,
            "actor_id": actor_id,
            "lease_generation": requirement.lease_generation,
            "payload_digest": payload_digest,
            "previous_hash": previous_hash,
            "idempotency_key": idempotency_key,
            "created_at": created_at,
        }
        event = AgentVerificationEvent(
            **digest_values,
            event_digest=sha256_hex(digest_values),
        )
        self.db.add(event)
        await self.db.flush()
        return event

    async def _event_replay(
        self,
        requirement: AgentVerificationRequirement,
        idempotency_key: str,
        payload_digest: str,
    ) -> bool:
        event = await self.db.scalar(
            select(AgentVerificationEvent).where(
                AgentVerificationEvent.requirement_id == requirement.id,
                AgentVerificationEvent.idempotency_key == idempotency_key,
            )
        )
        if event is None:
            return False
        if event.payload_digest != payload_digest:
            raise AgentConflictError("Idempotency key was reused with another request")
        return True

    async def _matching_event(
        self,
        requirements: list[AgentVerificationRequirement],
        idempotency_key: str,
        payload_digest: str,
    ) -> bool:
        if not requirements:
            return False
        keys = [
            self._child_key(idempotency_key, item.slot_key)
            for item in requirements
        ]
        events = list(
            (
                await self.db.execute(
                    select(AgentVerificationEvent).where(
                        AgentVerificationEvent.requirement_id.in_(
                            [item.id for item in requirements]
                        ),
                        AgentVerificationEvent.idempotency_key.in_(keys),
                    )
                )
            ).scalars().all()
        )
        if not events:
            return False
        if len(events) != len(requirements) or any(
            item.payload_digest != payload_digest for item in events
        ):
            raise AgentConflictError("Package activation idempotency history is incomplete")
        return True

    async def _lock_package(self, package_id: int) -> AgentWorkPackage:
        package = await self.db.scalar(
            select(AgentWorkPackage)
            .where(AgentWorkPackage.id == package_id)
            .with_for_update()
        )
        if package is None:
            raise ValueError("Agent work package not found")
        return package

    async def _lock_requirement(self, requirement_id: int) -> AgentVerificationRequirement:
        requirement = await self.db.scalar(
            select(AgentVerificationRequirement)
            .where(AgentVerificationRequirement.id == requirement_id)
            .with_for_update()
        )
        if requirement is None:
            raise ValueError("Verification requirement not found")
        return requirement

    async def _lock_requirements(
        self, package_id: int
    ) -> list[AgentVerificationRequirement]:
        result = await self.db.execute(
            select(AgentVerificationRequirement)
            .where(AgentVerificationRequirement.package_id == package_id)
            .order_by(AgentVerificationRequirement.slot_key)
            .with_for_update()
        )
        return list(result.scalars().all())

    async def _load_package(self, package_id: int) -> AgentWorkPackage:
        package = await self.db.scalar(
            select(AgentWorkPackage)
            .options(selectinload(AgentWorkPackage.requirements))
            .where(AgentWorkPackage.id == package_id)
        )
        if package is None:
            raise ValueError("Agent work package not found")
        return package

    async def _load_requirement(self, requirement_id: int) -> AgentVerificationRequirement:
        requirement = await self.db.get(AgentVerificationRequirement, requirement_id)
        if requirement is None:
            raise ValueError("Verification requirement not found")
        return requirement

    @staticmethod
    def requirement_response(
        requirement: AgentVerificationRequirement,
    ) -> VerificationRequirementResponse:
        return VerificationRequirementResponse.model_validate(requirement)

    @classmethod
    def package_response(cls, package: AgentWorkPackage) -> AgentWorkPackageResponse:
        values = {
            column: getattr(package, column)
            for column in (
                "id",
                "package_key",
                "package_version",
                "execution_task_id",
                "predecessor_package_id",
                "state",
                "artifact_set_digest",
                "contract_manifest_digest",
                "source_contract_digest",
                "external_journal_revision",
                "external_journal_head_digest",
                "created_at",
                "updated_at",
            )
        }
        values["requirements"] = [
            cls.requirement_response(item) for item in package.requirements
        ]
        return AgentWorkPackageResponse(**values)

    @classmethod
    def transition_response(
        cls,
        requirement: AgentVerificationRequirement,
        package: AgentWorkPackage,
        *,
        verdict: str | None = None,
    ) -> VerificationTransitionResponse:
        return VerificationTransitionResponse(
            requirement=cls.requirement_response(requirement),
            package_state=package.state,
            verdict=verdict,
        )

    @staticmethod
    def _request_fingerprint(data: AgentWorkPackageCreate) -> str:
        return sha256_hex(data.model_dump(mode="json"))
