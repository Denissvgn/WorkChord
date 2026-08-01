"""Contract and service coverage for portable agent-team setup."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import httpx
import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import mcp_agent_tools
from app.database import get_db
from app.main import app as main_app
from app.mcp_server import mcp
from app.models.agent import (
    AgentActor,
    AgentModelCatalogEntry,
    AgentTeamTopologyMember,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_team_setup import (
    MAX_AGENT_TEAM_MANIFEST_BYTES,
    AgentTeamApplyRequest,
    AgentTeamCurrentMember,
    AgentTeamCurrentSnapshot,
    AgentTeamManifestRequest,
    AgentTeamMaster,
    AgentTeamPlanRequest,
    AgentTeamReconciliationClass,
    AgentTeamRuntimeAcknowledgement,
    parse_agent_team_master,
    reconcile_agent_team_master,
)
from app.services.agent_service import AgentService
from app.services.agent_team_setup_service import (
    AgentTeamSetupConflictError,
    AgentTeamSetupService,
)
from app.utils.time import utc_now


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_PATH = REPOSITORY_ROOT / "config" / "examples" / "agent-team-master.json"


def example_payload() -> dict[str, Any]:
    return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))


def operator() -> AgentActor:
    return AgentActor(
        id=0,
        name="admin-api-key",
        display_name="Admin API Key",
        api_key_hash="admin",
        scopes='["admin"]',
        enabled=True,
        lifecycle_state="active",
        role="pm",
        created_at=utc_now(),
    )


class CapturingCredentialSink:
    reference = "agent-team-secure-sink"
    available = True

    def __init__(self) -> None:
        self.keys: dict[str, str] = {}

    async def deliver(
        self,
        *,
        credential_ref: str,
        actor_key: str,
        actor_name: str,
        api_key: str,
    ) -> str:
        assert credential_ref.startswith(f"{self.reference}/")
        assert actor_name
        self.keys[actor_key] = api_key
        return ("a" * 63) + str(len(self.keys))


class FailingOnceCredentialSink(CapturingCredentialSink):
    def __init__(self) -> None:
        super().__init__()
        self.failed = False
        self.failed_actor_key: str | None = None

    async def deliver(
        self,
        *,
        credential_ref: str,
        actor_key: str,
        actor_name: str,
        api_key: str,
    ) -> str:
        if not self.failed:
            self.failed = True
            self.failed_actor_key = actor_key
            raise RuntimeError("simulated uncertain sink delivery")
        return await super().deliver(
            credential_ref=credential_ref,
            actor_key=actor_key,
            actor_name=actor_name,
            api_key=api_key,
        )


@pytest.mark.contract
def test_master_is_canonical_secret_free_and_forward_versioned() -> None:
    payload = example_payload()
    master = parse_agent_team_master(payload)
    assert master.schema_version == "agent-team-master-v1"
    assert master.canonical_bytes() == AgentTeamMaster.model_validate(
        deepcopy(payload)
    ).canonical_bytes()
    assert len(master.digest()) == 64

    secret_payload = deepcopy(payload)
    secret_payload["controller"]["api_key"] = "forbidden"
    with pytest.raises(ValidationError, match="Extra inputs"):
        AgentTeamMaster.model_validate(secret_payload)

    secret_reference = deepcopy(payload)
    secret_reference["controller"]["runtime_ref"] = (
        "https://runtime.invalid?access_token=forbidden"
    )
    with pytest.raises(ValidationError, match="secret-like"):
        AgentTeamMaster.model_validate(secret_reference)

    unsupported = deepcopy(payload)
    unsupported["schema_version"] = "agent-team-master-v2"
    with pytest.raises(ValueError, match="Unsupported"):
        parse_agent_team_master(unsupported)

    no_workers = deepcopy(payload)
    no_workers["workers"] = []
    with pytest.raises(ValidationError):
        AgentTeamMaster.model_validate(no_workers)


@pytest.mark.contract
def test_master_rejects_role_identity_binding_and_size_mutations() -> None:
    base = example_payload()
    invalid: list[dict[str, Any]] = []

    duplicate_key = deepcopy(base)
    duplicate_key["workers"][0]["actor_key"] = (
        duplicate_key["controller"]["actor_key"]
    )
    invalid.append(duplicate_key)

    pm_worker_scopes = deepcopy(base)
    pm_worker_scopes["controller"]["scope_preset"] = "worker-v1"
    invalid.append(pm_worker_scopes)

    worker_without_execution = deepcopy(base)
    worker_without_execution["workers"][0]["assignment_modes"] = [
        "design_handoff"
    ]
    invalid.append(worker_without_execution)

    missing_default = deepcopy(base)
    missing_default["workers"][0]["default_model_binding_key"] = (
        "undeclared-model"
    )
    invalid.append(missing_default)

    incompatible_package = deepcopy(base)
    incompatible_package["workers"][0]["skill_package"]["name"] = (
        "workchord-pm"
    )
    invalid.append(incompatible_package)

    unknown_scope = deepcopy(base)
    unknown_scope["workers"][0]["scope_preset"] = "worker-v2"
    invalid.append(unknown_scope)

    credential_value = deepcopy(base)
    credential_value["workers"][0]["display_name"] = (
        f"pmag_{'a' * 24}"
    )
    invalid.append(credential_value)

    for payload in invalid:
        with pytest.raises(ValidationError):
            AgentTeamMaster.model_validate(payload)

    oversized = deepcopy(base)
    worker_template = oversized["workers"][0]
    oversized["workers"] = []
    for index in range(64):
        worker = deepcopy(worker_template)
        worker["actor_key"] = f"worker-{index}"
        worker["actor_name"] = f"workchord-worker-{index}"
        worker["runtime_ref"] = (
            f"runtime://worker-{index}/" + ("r" * 900)
        )
        worker["credential_ref"] = (
            f"agent-team-secure-sink/worker-{index}/" + ("c" * 900)
        )
        oversized["workers"].append(worker)
    assert len(json.dumps(oversized).encode("utf-8")) > (
        MAX_AGENT_TEAM_MANIFEST_BYTES
    )
    with pytest.raises(ValidationError, match="manifest exceeds"):
        AgentTeamMaster.model_validate(oversized)


@pytest.mark.contract
def test_reconciliation_is_stable_and_never_hard_deletes() -> None:
    master = AgentTeamMaster.model_validate(example_payload())
    empty = AgentTeamCurrentSnapshot(
        topology_key=master.topology_key,
        revision=0,
    )
    create_plan = reconcile_agent_team_master(master, empty)
    assert {
        action.reconciliation_class for action in create_plan.actions
    } == {AgentTeamReconciliationClass.CREATE}
    assert create_plan == reconcile_agent_team_master(master, empty)

    controller = master.controller
    current = AgentTeamCurrentSnapshot(
        topology_key=master.topology_key,
        revision=4,
        manifest_digest=master.digest(),
        members=(
            AgentTeamCurrentMember(
                actor_key=controller.actor_key,
                actor_id=7,
                actor_name=controller.actor_name,
                topology_key=master.topology_key,
                object_revision=2,
                lifecycle_state="runtime_ready",
                desired_spec=controller,
            ),
            AgentTeamCurrentMember(
                actor_key="retired-worker",
                actor_id=8,
                actor_name="retired-worker",
                topology_key=master.topology_key,
                object_revision=3,
                lifecycle_state="runtime_ready",
                desired_spec=master.workers[0].model_copy(
                    update={
                        "actor_key": "retired-worker",
                        "actor_name": "retired-worker",
                        "credential_ref": (
                            "agent-team-secure-sink/retired-worker"
                        ),
                        "runtime_ref": "runtime://retired-worker",
                    }
                ),
            ),
        ),
    )
    plan = reconcile_agent_team_master(master, current)
    by_actor = {action.actor_key: action for action in plan.actions}
    assert by_actor[controller.actor_key].reconciliation_class == "no_change"
    retired = by_actor["retired-worker"]
    assert retired.reconciliation_class == "propose_disable"
    assert retired.operation == "disable_member"
    assert retired.requires_explicit_confirmation is True
    assert all(action.operation != "delete" for action in plan.actions)


@pytest.mark.asyncio
async def test_fresh_apply_replay_onboarding_and_runtime_readiness(
    db_session: AsyncSession,
) -> None:
    payload = example_payload()
    manifest = AgentTeamMaster.model_validate(payload)
    for key in {
        member.default_model_binding_key for member in manifest.all_members
    }:
        db_session.add(
            AgentModelCatalogEntry(
                key=key,
                provider="configured-provider",
                configured_model_alias=key,
                reasoning_tier=2,
                context_tier="medium",
                modality_tags=["text"],
                cost_tier="medium",
                latency_tier="balanced",
                enabled=True,
                revision=1,
            )
        )
    await db_session.commit()

    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)
    admin = operator()
    validation = await service.validate(
        admin,
        AgentTeamManifestRequest(manifest=manifest),
    )
    assert validation.valid is True
    plan = await service.plan(
        admin,
        AgentTeamPlanRequest(
            manifest=manifest,
            expected_topology_revision=0,
        ),
    )
    request = AgentTeamApplyRequest(
        manifest=manifest,
        expected_topology_revision=0,
        plan_digest=plan.plan_digest,
        approved_action_ids=tuple(
            action.action_id for action in plan.actions
        ),
    )
    command = AgentPlanningCommandContext(
        idempotency_key="agent-team-fresh-setup",
        rationale="Establish the approved logical topology",
        correlation_id="agent-team-fresh-setup-correlation",
    )
    applied = await service.apply(admin, request, command=command)
    assert applied.status == "completed"
    assert applied.resulting_topology_revision == 1
    assert set(sink.keys) == {
        member.actor_key for member in manifest.all_members
    }
    assert "pmag_" not in applied.model_dump_json()

    replay = await service.apply(admin, request, command=command)
    assert replay.replayed is True
    assert replay.apply_id == applied.apply_id

    status = await service.status(admin, topology_key=manifest.topology_key)
    assert status.topology_state == "blocked"
    assert status.runtime_ready is False
    assert all(member.handoff is not None for member in status.members)
    assert all(
        member.availability == "availability_unknown"
        for member in status.members
    )
    assert all(
        (
            member.queued_assignments,
            member.accepted_assignments,
            member.running_runs,
        )
        == (0, 0, 0)
        for member in status.members
    )
    onboarding_report = await service.report(
        admin,
        topology_key=manifest.topology_key,
    )
    assert onboarding_report.schema_version == "agent-team-setup-report-v1"
    assert onboarding_report.counts.desired == len(manifest.all_members)
    assert onboarding_report.counts.configured == len(manifest.all_members)
    assert onboarding_report.counts.credential_delivered == len(
        manifest.all_members
    )
    assert onboarding_report.counts.onboarding == len(manifest.all_members)
    assert onboarding_report.counts.connected == 0
    assert onboarding_report.counts.runtime_ready == 0
    assert onboarding_report.counts.blocked == len(manifest.all_members)
    assert onboarding_report.dispatch_context.state == "availability_unknown"
    assert onboarding_report.dispatch_context.dispatch_eligible is None
    assert onboarding_report.evidence.apply_runs == 1
    assert onboarding_report.evidence.action_receipts == len(
        manifest.all_members
    )
    serialized_report = onboarding_report.model_dump_json()
    assert "pmag_" not in serialized_report
    assert "runtime://" not in serialized_report
    assert "credential_ref" not in serialized_report

    actor_service = AgentService(db_session)
    for member_status in status.members:
        handoff = member_status.handoff
        assert handoff is not None
        api_key = sink.keys[member_status.actor_key]
        assert await actor_service.authenticate(api_key) is None
        acknowledgement = AgentTeamRuntimeAcknowledgement(
            topology_key=handoff.topology_key,
            topology_revision=handoff.topology_revision,
            actor_key=handoff.actor_key,
            role=handoff.role,
            skill_package=handoff.skill_package,
            profile_revision=handoff.profile_revision,
            model_binding_revisions=handoff.model_binding_revisions,
            server_features=handoff.required_server_features,
            supported_assignment_modes=handoff.supported_assignment_modes,
        )
        receipt = await service.acknowledge_runtime(
            api_key,
            acknowledgement,
        )
        assert receipt.actor_key == handoff.actor_key
        assert await actor_service.authenticate(api_key) is not None

    ready = await service.status(admin, topology_key=manifest.topology_key)
    assert ready.topology_state == "runtime_ready"
    assert ready.runtime_ready is True
    assert ready.blocker_codes == ()
    assert all(member.runtime_ready for member in ready.members)
    ready_report = await service.report(
        admin,
        topology_key=manifest.topology_key,
    )
    assert ready_report.runtime_ready is True
    assert ready_report.counts.runtime_ready == len(manifest.all_members)
    assert ready_report.counts.connected == len(manifest.all_members)
    assert ready_report.counts.blocked == 0

    controller_key = sink.keys[manifest.controller.actor_key]
    controller = await actor_service.authenticate(controller_key)
    assert controller is not None
    outsider = AgentActor(
        name="unmanaged-worker",
        display_name="Unmanaged Worker",
        api_key_hash="unmanaged",
        scopes='["work:execute"]',
        enabled=True,
        lifecycle_state="active",
        role="worker",
    )
    db_session.add(outsider)
    await db_session.commit()
    with pytest.raises(
        AgentTeamSetupConflictError,
        match="not runtime-ready",
    ):
        await service.require_dispatch_member(controller, outsider.id)

    async def override_db():
        yield db_session

    main_app.dependency_overrides[get_db] = override_db
    client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=main_app),
        base_url="http://workchord.test",
    )
    try:
        rest = await client.get(
            "/api/agent/team-setup/status",
            headers={"X-Agent-API-Key": controller_key},
        )
        assert rest.status_code == 200
        assert rest.json() == await mcp_agent_tools.get_agent_team_setup_status(
            db_session,
            controller,
        )
        assert rest.json()["can_mutate"] is False

        report = await client.get(
            "/api/agent/team-setup/report",
            headers={"X-Agent-API-Key": controller_key},
        )
        assert report.status_code == 200
        assert report.headers["cache-control"] == "private, no-store"
        assert report.json()["runtime_ready"] is True
        assert report.json()["counts"]["runtime_ready"] == len(
            manifest.all_members
        )
        assert "pmag_" not in report.text
        assert "runtime://" not in report.text

        denied = await client.post(
            "/api/agent/team-setup/validate",
            headers={"X-Agent-API-Key": controller_key},
            json={"manifest": payload},
        )
        assert denied.status_code == 403
        assert denied.json()["detail"]["code"] == "agent_permission_denied"
    finally:
        await client.aclose()
        main_app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_confirmed_identity_replacement_disables_old_actor(
    db_session: AsyncSession,
) -> None:
    manifest = AgentTeamMaster.model_validate(example_payload())
    for key in {
        member.default_model_binding_key for member in manifest.all_members
    }:
        db_session.add(
            AgentModelCatalogEntry(
                key=key,
                provider="configured-provider",
                configured_model_alias=key,
                reasoning_tier=2,
                context_tier="medium",
                modality_tags=["text"],
                cost_tier="medium",
                latency_tier="balanced",
                enabled=True,
                revision=1,
            )
        )
    await db_session.commit()

    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)
    admin = operator()
    initial_plan = await service.plan(
        admin,
        AgentTeamPlanRequest(
            manifest=manifest,
            expected_topology_revision=0,
        ),
    )
    initial = await service.apply(
        admin,
        AgentTeamApplyRequest(
            manifest=manifest,
            expected_topology_revision=0,
            plan_digest=initial_plan.plan_digest,
            approved_action_ids=tuple(
                action.action_id for action in initial_plan.actions
            ),
        ),
        command=AgentPlanningCommandContext(
            idempotency_key="agent-team-before-replacement",
            rationale="Create the topology before replacing one worker",
            correlation_id="agent-team-before-replacement-correlation",
        ),
    )
    assert initial.status == "completed"

    worker = manifest.workers[0]
    old_key = sink.keys[worker.actor_key]
    old_record = (
        await db_session.execute(
            select(AgentTeamTopologyMember).where(
                AgentTeamTopologyMember.actor_key == worker.actor_key
            )
        )
    ).scalar_one()
    assert old_record.actor_id is not None
    old_actor_id = old_record.actor_id

    replacement_payload = example_payload()
    replacement_payload["workers"][0].update(
        {
            "actor_name": "workchord-backend-worker-v2",
            "runtime_ref": "runtime://backend-worker-v2",
            "credential_ref": (
                "agent-team-secure-sink/backend-worker-v2"
            ),
        }
    )
    replacement_manifest = AgentTeamMaster.model_validate(
        replacement_payload
    )
    replacement_plan = await service.plan(
        admin,
        AgentTeamPlanRequest(
            manifest=replacement_manifest,
            expected_topology_revision=1,
        ),
    )
    replacement_action = next(
        action
        for action in replacement_plan.actions
        if action.actor_key == worker.actor_key
    )
    assert replacement_action.operation == "replace_member"
    assert replacement_action.requires_explicit_confirmation is True

    replaced = await service.apply(
        admin,
        AgentTeamApplyRequest(
            manifest=replacement_manifest,
            expected_topology_revision=1,
            plan_digest=replacement_plan.plan_digest,
            approved_action_ids=(replacement_action.action_id,),
            confirmed_action_ids=(replacement_action.action_id,),
        ),
        command=AgentPlanningCommandContext(
            idempotency_key="agent-team-replace-worker",
            rationale="Replace the reviewed stable worker identity",
            correlation_id="agent-team-replace-worker-correlation",
        ),
    )
    assert replaced.status == "completed"
    assert replaced.resulting_topology_revision == 2
    assert replaced.receipts[0].status == "applied"

    current_record = (
        await db_session.execute(
            select(AgentTeamTopologyMember).where(
                AgentTeamTopologyMember.actor_key == worker.actor_key
            )
        )
    ).scalar_one()
    assert current_record.actor_id is not None
    assert current_record.actor_id != old_actor_id
    old_actor = await db_session.get(AgentActor, old_actor_id)
    new_actor = await db_session.get(AgentActor, current_record.actor_id)
    assert old_actor is not None
    assert old_actor.enabled is False
    assert old_actor.lifecycle_state == "disabled"
    assert new_actor is not None
    assert new_actor.enabled is False
    assert new_actor.lifecycle_state == "onboarding"
    assert sink.keys[worker.actor_key] != old_key
    assert await AgentService(db_session).authenticate(old_key) is None


@pytest.mark.asyncio
async def test_uncertain_delivery_requires_explicit_new_reference_recovery(
    db_session: AsyncSession,
) -> None:
    manifest = AgentTeamMaster.model_validate(example_payload())
    for key in {
        member.default_model_binding_key for member in manifest.all_members
    }:
        db_session.add(
            AgentModelCatalogEntry(
                key=key,
                provider="configured-provider",
                configured_model_alias=key,
                reasoning_tier=2,
                context_tier="medium",
                modality_tags=["text"],
                cost_tier="medium",
                latency_tier="balanced",
                enabled=True,
                revision=1,
            )
        )
    await db_session.commit()

    sink = FailingOnceCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)
    admin = operator()
    plan = await service.plan(
        admin,
        AgentTeamPlanRequest(
            manifest=manifest,
            expected_topology_revision=0,
        ),
    )
    first_apply = await service.apply(
        admin,
        AgentTeamApplyRequest(
            manifest=manifest,
            expected_topology_revision=0,
            plan_digest=plan.plan_digest,
            approved_action_ids=tuple(
                action.action_id for action in plan.actions
            ),
        ),
        command=AgentPlanningCommandContext(
            idempotency_key="agent-team-uncertain-delivery",
            rationale="Exercise fail-closed credential delivery",
            correlation_id="agent-team-uncertain-delivery-correlation",
        ),
    )
    assert first_apply.status == "blocked"
    assert sink.failed_actor_key is not None
    failed_actor_key = sink.failed_actor_key
    failed_record = (
        await db_session.execute(
            select(AgentTeamTopologyMember).where(
                AgentTeamTopologyMember.actor_key == failed_actor_key
            )
        )
    ).scalar_one()
    assert failed_record.actor_id is not None
    assert failed_record.credential_delivery_state == "uncertain"
    failed_actor = await db_session.get(AgentActor, failed_record.actor_id)
    assert failed_actor is not None
    assert failed_actor.enabled is False
    assert failed_actor.lifecycle_state == "disabled"
    original_hash = failed_actor.api_key_hash

    recovery_payload = example_payload()
    recovery_members = [
        recovery_payload["controller"],
        *recovery_payload["workers"],
        *recovery_payload["verifiers"],
    ]
    recovery_member = next(
        member
        for member in recovery_members
        if member["actor_key"] == failed_actor_key
    )
    recovery_member["credential_ref"] = (
        f"agent-team-secure-sink/{failed_actor_key}-recovery"
    )
    recovery_manifest = AgentTeamMaster.model_validate(recovery_payload)
    recovery_plan = await service.plan(
        admin,
        AgentTeamPlanRequest(
            manifest=recovery_manifest,
            expected_topology_revision=1,
        ),
    )
    recovery_action = next(
        action
        for action in recovery_plan.actions
        if action.actor_key == failed_actor_key
    )
    assert recovery_action.operation == "replace_member"
    assert recovery_action.blocker_code == "credential_delivery_uncertain"
    recovered = await service.apply(
        admin,
        AgentTeamApplyRequest(
            manifest=recovery_manifest,
            expected_topology_revision=1,
            plan_digest=recovery_plan.plan_digest,
            approved_action_ids=(recovery_action.action_id,),
            confirmed_action_ids=(recovery_action.action_id,),
        ),
        command=AgentPlanningCommandContext(
            idempotency_key="agent-team-recover-delivery",
            rationale="Rotate the uncertain credential to a new sink reference",
            correlation_id="agent-team-recover-delivery-correlation",
        ),
    )
    assert recovered.status == "completed"
    assert recovered.receipts[0].status == "applied"

    await db_session.refresh(failed_record)
    await db_session.refresh(failed_actor)
    assert failed_record.actor_id == failed_actor.id
    assert failed_record.credential_ref == recovery_member["credential_ref"]
    assert failed_record.credential_delivery_state == "delivered"
    assert failed_actor.api_key_hash != original_hash
    assert failed_actor.enabled is False
    assert failed_actor.lifecycle_state == "onboarding"
    assert failed_actor_key in sink.keys


@pytest.mark.asyncio
async def test_mcp_registers_secret_free_setup_status_read_only() -> None:
    tools = {tool.name: tool for tool in await mcp.list_tools()}

    assert "agent_get_team_setup_status" in tools
    assert "agent_apply_team_setup" not in tools
    assert "agent_validate_team_setup" not in tools


@pytest.mark.asyncio
async def test_topologies_share_catalog_and_profile_references_not_identities(
    db_session: AsyncSession,
) -> None:
    first_payload = example_payload()
    first = AgentTeamMaster.model_validate(first_payload)
    for key in {
        member.default_model_binding_key for member in first.all_members
    }:
        db_session.add(
            AgentModelCatalogEntry(
                key=key,
                provider="configured-provider",
                configured_model_alias=key,
                reasoning_tier=2,
                context_tier="medium",
                modality_tags=["text"],
                cost_tier="medium",
                latency_tier="balanced",
                enabled=True,
                revision=1,
            )
        )
    await db_session.commit()

    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)
    admin = operator()

    async def apply_manifest(
        manifest: AgentTeamMaster,
        command_key: str,
    ):
        plan = await service.plan(
            admin,
            AgentTeamPlanRequest(
                manifest=manifest,
                expected_topology_revision=0,
            ),
        )
        return await service.apply(
            admin,
            AgentTeamApplyRequest(
                manifest=manifest,
                expected_topology_revision=0,
                plan_digest=plan.plan_digest,
                approved_action_ids=tuple(
                    action.action_id for action in plan.actions
                ),
            ),
            command=AgentPlanningCommandContext(
                idempotency_key=command_key,
                rationale="Apply an isolated topology",
                correlation_id=f"{command_key}-correlation",
            ),
        )

    assert (await apply_manifest(first, "first-topology")).status == "completed"

    second_payload = deepcopy(first_payload)
    second_payload["topology_key"] = "second-agent-team"
    for member in (
        second_payload["controller"],
        *second_payload["workers"],
        *second_payload["verifiers"],
    ):
        member["actor_key"] = f"second-{member['actor_key']}"
        member["actor_name"] = f"second-{member['actor_name']}"
        member["runtime_ref"] = f"runtime://second/{member['actor_key']}"
        member["credential_ref"] = (
            f"agent-team-secure-sink/second/{member['actor_key']}"
        )
    second = AgentTeamMaster.model_validate(second_payload)
    second_receipt = await apply_manifest(second, "second-topology")
    assert second_receipt.status == "completed"

    collision_payload = deepcopy(second_payload)
    collision_payload["topology_key"] = "third-agent-team"
    collision_payload["controller"]["actor_key"] = "third-primary-pm"
    collision_payload["controller"]["actor_name"] = "third-primary-pm"
    collision_payload["controller"]["credential_ref"] = (
        "agent-team-secure-sink/third-primary-pm"
    )
    collision_payload["controller"]["runtime_ref"] = (
        first.controller.runtime_ref
    )
    collision = AgentTeamMaster.model_validate(collision_payload)
    collision_plan = await service.plan(
        admin,
        AgentTeamPlanRequest(
            manifest=collision,
            expected_topology_revision=0,
        ),
    )
    controller_action = next(
        action
        for action in collision_plan.actions
        if action.actor_key == collision.controller.actor_key
    )
    assert controller_action.blocker_code == (
        "cross_topology_runtime_reference"
    )
