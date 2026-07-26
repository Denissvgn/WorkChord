"""Focused fenced verifier lifecycle integration tests."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app import models as _models  # noqa: F401
from app.database import Base
from app.models.agent import AgentActor
from app.models.autonomy import AgentAutonomyTopology, AgentAutonomyTopologyMember
from app.schemas.autonomy import (
    AgentWorkPackageCreate,
    ResolvedVerifierLease,
    VerificationBeginRequest,
    VerificationClaimRequest,
    VerificationCriterionResult,
    VerificationRequirementCreate,
    VerificationSubmitRequest,
)
from app.services.agent_service import AgentConflictError, AgentPermissionError
from app.services.autonomy_work_package_service import AutonomyWorkPackageService


DIGESTS = tuple(char * 64 for char in "abcdef123456789")


def _actor(name: str, role: str, scopes: list[str]) -> AgentActor:
    return AgentActor(
        name=name,
        display_name=name,
        api_key_hash=f"{name}-hash",
        scopes=json.dumps(scopes),
        enabled=True,
        role=role,
    )


def _lease(
    *,
    action: str,
    actor: AgentActor,
    logical_key: str,
    slot: str,
    digest: str,
) -> ResolvedVerifierLease:
    now = datetime.now(UTC)
    return ResolvedVerifierLease(
        lease_digest=digest,
        task_id="AUT-ADV-001",
        stage_id=slot,
        action=action,
        actor_logical_key=logical_key,
        actor_id=actor.id,
        topology_revision=1,
        attempt_start_digest=DIGESTS[0],
        issued_at=now - timedelta(seconds=1),
        expires_at=now + timedelta(minutes=5),
    )


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_multi_slot_verification_is_fenced_and_rejection_invalidates_sibling(
    tmp_path,
) -> None:
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{tmp_path / 'workchord_autonomy_service.db'}"
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    sessions = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    try:
        async with sessions() as db:
            controller = _actor(
                "pg-program-controller",
                "pm",
                ["planning:write", "planning:read"],
            )
            verifier_a = _actor(
                "pg-adversarial-verifier-a",
                "verifier",
                ["verification:read", "verification:write"],
            )
            verifier_b = _actor(
                "pg-adversarial-verifier-b",
                "verifier",
                ["verification:read", "verification:write"],
            )
            outsider = _actor(
                "pg-outsider-verifier",
                "verifier",
                ["verification:read", "verification:write"],
            )
            db.add_all([controller, verifier_a, verifier_b, outsider])
            await db.flush()
            topology = AgentAutonomyTopology(
                topology_key="postgresql-autonomous-migration",
                revision=1,
                manifest_digest=DIGESTS[0],
                charter_digest=DIGESTS[1],
                primary_actor_id=controller.id,
                state="active",
                external_journal_revision=1,
                external_journal_head_digest=DIGESTS[0],
            )
            db.add(topology)
            await db.flush()
            db.add_all(
                [
                    AgentAutonomyTopologyMember(
                        topology_id=topology.id,
                        logical_key=verifier.name,
                        actor_id=verifier.id,
                        object_revision=1,
                        lifecycle_state="runtime_ready",
                        desired_member_digest=DIGESTS[index],
                        independence_group=f"verifier-{index}-group",
                        role_package_checksum=DIGESTS[2],
                        external_identity_binding_digest=DIGESTS[3],
                        runtime_attestation_digest=DIGESTS[4],
                        credential_delivery_receipt_digest=DIGESTS[5],
                        runtime_acknowledgement_digest=DIGESTS[6],
                    )
                    for index, verifier in enumerate((verifier_a, verifier_b), start=1)
                ]
            )
            await db.commit()

            service = AutonomyWorkPackageService(db)
            created = await service.create_package(
                controller,
                AgentWorkPackageCreate(
                    package_key="AUT-ADV-001",
                    package_version=1,
                    artifact_set_digest=DIGESTS[0],
                    contract_manifest_digest=DIGESTS[1],
                    source_contract_digest=DIGESTS[2],
                    external_journal_revision=1,
                    external_journal_head_digest=DIGESTS[0],
                    requirements=(
                        VerificationRequirementCreate(
                            slot_key="slot-a",
                            verifier_logical_key=verifier_a.name,
                            criterion_schema="autonomy-criteria-v1",
                            evaluator_version="evaluator-v1",
                            executor_independence_group="executor-group",
                            verifier_independence_group="verifier-1-group",
                        ),
                        VerificationRequirementCreate(
                            slot_key="slot-b",
                            verifier_logical_key=verifier_b.name,
                            criterion_schema="autonomy-criteria-v1",
                            evaluator_version="evaluator-v1",
                            executor_independence_group="executor-group",
                            verifier_independence_group="verifier-2-group",
                        ),
                    ),
                ),
            )
            activated = await service.activate_requirements(
                controller,
                package_id=created.id,
                external_journal_revision=2,
                external_journal_head_digest=DIGESTS[1],
                idempotency_key="activate-package-1",
            )
            by_slot = {item.slot_key: item for item in activated.requirements}
            assert {item.state for item in activated.requirements} == {"ready"}

            claim_a = VerificationClaimRequest(
                requirement_id=by_slot["slot-a"].id,
                expected_package_version=1,
                expected_artifact_set_digest=DIGESTS[0],
                external_journal_revision=3,
                external_journal_head_digest=DIGESTS[2],
            )
            with pytest.raises(AgentPermissionError, match="runtime-ready"):
                await service.claim_requirement(
                    outsider,
                    claim_a,
                    resolved_lease=_lease(
                        action="verification-claim",
                        actor=outsider,
                        logical_key=verifier_a.name,
                        slot="slot-a",
                        digest=DIGESTS[3],
                    ),
                    idempotency_key="outsider-claim",
                )
            claimed_a = await service.claim_requirement(
                verifier_a,
                claim_a,
                resolved_lease=_lease(
                    action="verification-claim",
                    actor=verifier_a,
                    logical_key=verifier_a.name,
                    slot="slot-a",
                    digest=DIGESTS[3],
                ),
                idempotency_key="claim-a",
            )
            assert claimed_a.requirement.attempt_start_digest == DIGESTS[0]
            with pytest.raises(AgentConflictError, match="attempt start"):
                await service.begin_requirement(
                    verifier_a,
                    VerificationBeginRequest(
                        requirement_id=claimed_a.requirement.id,
                        expected_lease_generation=claimed_a.requirement.lease_generation,
                        expected_lease_digest=claimed_a.requirement.lease_digest,
                        runtime_attestation_digest=DIGESTS[4],
                        external_journal_revision=4,
                        external_journal_head_digest=DIGESTS[3],
                    ),
                    resolved_lease=_lease(
                        action="verification-begin",
                        actor=verifier_a,
                        logical_key=verifier_a.name,
                        slot="slot-a",
                        digest=DIGESTS[4],
                    ).model_copy(update={"attempt_start_digest": DIGESTS[1]}),
                    idempotency_key="begin-a-wrong-attempt",
                )
            began_a = await service.begin_requirement(
                verifier_a,
                VerificationBeginRequest(
                    requirement_id=claimed_a.requirement.id,
                    expected_lease_generation=claimed_a.requirement.lease_generation,
                    expected_lease_digest=claimed_a.requirement.lease_digest,
                    runtime_attestation_digest=DIGESTS[4],
                    external_journal_revision=4,
                    external_journal_head_digest=DIGESTS[3],
                ),
                resolved_lease=_lease(
                    action="verification-begin",
                    actor=verifier_a,
                    logical_key=verifier_a.name,
                    slot="slot-a",
                    digest=DIGESTS[4],
                ),
                idempotency_key="begin-a",
            )
            passed_a = await service.submit_requirement(
                verifier_a,
                VerificationSubmitRequest(
                    requirement_id=began_a.requirement.id,
                    expected_lease_generation=began_a.requirement.lease_generation,
                    expected_lease_digest=began_a.requirement.lease_digest,
                    artifact_set_digest=DIGESTS[0],
                    criterion_results=(
                        VerificationCriterionResult(
                            criterion_id="criterion-a",
                            evidence_object_digest=DIGESTS[5],
                            evaluator_predicate_digest=DIGESTS[6],
                            outcome="passed",
                        ),
                    ),
                    evaluator_attestation_digest=DIGESTS[7],
                    external_journal_revision=5,
                    external_journal_head_digest=DIGESTS[4],
                ),
                resolved_lease=_lease(
                    action="verification-submit",
                    actor=verifier_a,
                    logical_key=verifier_a.name,
                    slot="slot-a",
                    digest=DIGESTS[5],
                ),
                idempotency_key="submit-a",
            )
            assert passed_a.verdict == "passed"
            assert passed_a.package_state == "evaluating"

            claim_b = await service.claim_requirement(
                verifier_b,
                VerificationClaimRequest(
                    requirement_id=by_slot["slot-b"].id,
                    expected_package_version=1,
                    expected_artifact_set_digest=DIGESTS[0],
                    external_journal_revision=6,
                    external_journal_head_digest=DIGESTS[5],
                ),
                resolved_lease=_lease(
                    action="verification-claim",
                    actor=verifier_b,
                    logical_key=verifier_b.name,
                    slot="slot-b",
                    digest=DIGESTS[6],
                ),
                idempotency_key="claim-b",
            )
            begin_b = await service.begin_requirement(
                verifier_b,
                VerificationBeginRequest(
                    requirement_id=claim_b.requirement.id,
                    expected_lease_generation=claim_b.requirement.lease_generation,
                    expected_lease_digest=claim_b.requirement.lease_digest,
                    runtime_attestation_digest=DIGESTS[4],
                    external_journal_revision=7,
                    external_journal_head_digest=DIGESTS[6],
                ),
                resolved_lease=_lease(
                    action="verification-begin",
                    actor=verifier_b,
                    logical_key=verifier_b.name,
                    slot="slot-b",
                    digest=DIGESTS[7],
                ),
                idempotency_key="begin-b",
            )
            rejected_b = await service.submit_requirement(
                verifier_b,
                VerificationSubmitRequest(
                    requirement_id=begin_b.requirement.id,
                    expected_lease_generation=begin_b.requirement.lease_generation,
                    expected_lease_digest=begin_b.requirement.lease_digest,
                    artifact_set_digest=DIGESTS[0],
                    criterion_results=(
                        VerificationCriterionResult(
                            criterion_id="criterion-b",
                            evidence_object_digest=DIGESTS[8],
                            evaluator_predicate_digest=DIGESTS[9],
                            outcome="failed",
                        ),
                    ),
                    evaluator_attestation_digest=DIGESTS[10],
                    external_journal_revision=8,
                    external_journal_head_digest=DIGESTS[7],
                ),
                resolved_lease=_lease(
                    action="verification-submit",
                    actor=verifier_b,
                    logical_key=verifier_b.name,
                    slot="slot-b",
                    digest=DIGESTS[8],
                ),
                idempotency_key="submit-b",
            )
            assert rejected_b.verdict == "rejected"
            assert rejected_b.package_state == "rework_required"
            package = await service._load_package(created.id)
            assert {item.slot_key: item.state for item in package.requirements} == {
                "slot-a": "expired",
                "slot-b": "rejected",
            }
    finally:
        await engine.dispose()
