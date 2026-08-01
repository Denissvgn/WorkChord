"""Live topology, recovery, redaction, and compatibility qualification."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTeamApplyRun,
    AgentTeamTopology,
    AgentTaskAssignment,
)
from app.schemas.agent import (
    AgentRecoveryRequeue,
    AgentTaskAssignmentCreate,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_team_setup import (
    ROLE_SCOPE_PRESETS,
    AgentTeamApplyRequest,
    AgentTeamMaster,
    AgentTeamManifestRequest,
    AgentTeamPlanRequest,
    AgentTeamRuntimeAcknowledgement,
)
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.agent_service import AgentService, hash_api_key
from app.services.agent_team_setup_service import (
    AgentTeamSetupConflictError,
    AgentTeamSetupService,
)
from app.services.agent_work_service import AgentWorkService
from tests.test_agent_routing_wave6_qualification import (
    Candidate,
    ScenarioBase,
    _TASK_BRIEF,
    _assessment_command,
    _create_assessment_with_parity,
    _dispatch,
    _exclusion,
    _preview_with_parity,
)
from tests.test_agent_team_setup import (
    CapturingCredentialSink,
    example_payload,
    operator,
)


pytestmark = [
    pytest.mark.sqlite,
    pytest.mark.usefixtures("qualified_model_aware_routing_test_context"),
]

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FIXED_NOW = datetime(2026, 8, 1, 12, tzinfo=UTC)


@pytest.fixture(autouse=True)
def fixed_qualification_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep REST/MCP preview parity and readiness freshness deterministic."""

    for target in (
        "app.services.agent_routing_service.utc_now",
        "app.services.agent_work_service.utc_now",
        "app.services.agent_team_setup_service.utc_now",
    ):
        monkeypatch.setattr(target, lambda: FIXED_NOW)


def topology_payload(
    *,
    two_workers: bool = True,
    include_verifier: bool = True,
    prefix: str | None = None,
) -> dict[str, Any]:
    """Return a logical topology with routine and advanced execution actors."""

    payload = deepcopy(example_payload())
    payload["workers"][0].update(
        {
            "default_model_binding_key": "implementation-routine",
            "model_binding_keys": ["implementation-routine"],
        }
    )
    if two_workers:
        advanced = deepcopy(payload["workers"][0])
        advanced.update(
            {
                "actor_key": "operations-worker",
                "actor_name": "workchord-operations-worker",
                "display_name": "Advanced Operations Runtime",
                "profile_key": "release-ops-agent",
                "default_model_binding_key": "implementation-advanced",
                "model_binding_keys": ["implementation-advanced"],
                "runtime_ref": "runtime://operations-worker",
                "credential_ref": (
                    "agent-team-secure-sink/operations-worker"
                ),
            }
        )
        payload["workers"].append(advanced)
        payload["readiness_policy"]["minimum_execution_workers"] = 2
    if include_verifier:
        payload["verifiers"][0].update(
            {
                "default_model_binding_key": "verification-advanced",
                "model_binding_keys": ["verification-advanced"],
            }
        )
    else:
        payload["verifiers"] = []
    if prefix is not None:
        payload["topology_key"] = f"{prefix}-agent-team"
        for member in (
            payload["controller"],
            *payload["workers"],
            *payload["verifiers"],
        ):
            original_key = member["actor_key"]
            member["actor_key"] = f"{prefix}-{original_key}"
            member["actor_name"] = f"{prefix}-{member['actor_name']}"
            member["runtime_ref"] = (
                f"runtime://{prefix}/{member['actor_key']}"
            )
            member["credential_ref"] = (
                f"agent-team-secure-sink/{prefix}/{member['actor_key']}"
            )
    return payload


def topology_manifest(**kwargs: Any) -> AgentTeamMaster:
    return AgentTeamMaster.model_validate(topology_payload(**kwargs))


async def seed_model_catalog(
    db: AsyncSession,
    manifest: AgentTeamMaster,
) -> None:
    specifications = {
        "planning-default": (2, "medium", "medium"),
        "implementation-routine": (1, "small", "low"),
        "implementation-advanced": (3, "large", "high"),
        "verification-advanced": (3, "large", "high"),
    }
    existing = set(
        (
            await db.execute(
                select(AgentModelCatalogEntry.key).where(
                    AgentModelCatalogEntry.key.in_(
                        {
                            key
                            for member in manifest.all_members
                            for key in member.model_binding_keys
                        }
                    )
                )
            )
        )
        .scalars()
        .all()
    )
    for key in {
        key
        for member in manifest.all_members
        for key in member.model_binding_keys
    }:
        if key in existing:
            continue
        reasoning_tier, context_tier, cost_tier = specifications[key]
        db.add(
            AgentModelCatalogEntry(
                key=key,
                provider="qualification-provider",
                configured_model_alias=f"runtime-{key}",
                reasoning_tier=reasoning_tier,
                context_tier=context_tier,
                modality_tags=["text"],
                cost_tier=cost_tier,
                latency_tier="balanced",
                enabled=True,
                revision=1,
            )
        )
    await db.commit()


async def apply_manifest(
    service: AgentTeamSetupService,
    manifest: AgentTeamMaster,
    *,
    expected_revision: int,
    key: str,
    confirm_required: bool = False,
):
    plan = await service.plan(
        operator(),
        AgentTeamPlanRequest(
            manifest=manifest,
            expected_topology_revision=expected_revision,
        ),
    )
    actions = tuple(
        action
        for action in plan.actions
        if action.operation not in {"blocked", "unmanaged"}
    )
    request = AgentTeamApplyRequest(
        manifest=manifest,
        expected_topology_revision=expected_revision,
        plan_digest=plan.plan_digest,
        approved_action_ids=tuple(action.action_id for action in actions),
        confirmed_action_ids=tuple(
            action.action_id
            for action in actions
            if confirm_required and action.requires_explicit_confirmation
        ),
    )
    command = AgentPlanningCommandContext(
        idempotency_key=key,
        rationale="Qualify the exact reviewed topology reconciliation actions",
        correlation_id=f"{key}-correlation",
    )
    return plan, request, command, await service.apply(
        operator(),
        request,
        command=command,
    )


async def acknowledge_member(
    service: AgentTeamSetupService,
    *,
    topology_key: str,
    actor_key: str,
    api_key: str,
) -> None:
    status = await service.status(operator(), topology_key=topology_key)
    member = next(item for item in status.members if item.actor_key == actor_key)
    handoff = member.handoff
    assert handoff is not None
    response = await service.acknowledge_runtime(
        api_key,
        AgentTeamRuntimeAcknowledgement(
            topology_key=handoff.topology_key,
            topology_revision=handoff.topology_revision,
            actor_key=handoff.actor_key,
            role=handoff.role,
            skill_package=handoff.skill_package,
            profile_revision=handoff.profile_revision,
            model_binding_revisions=handoff.model_binding_revisions,
            server_features=handoff.required_server_features,
            supported_assignment_modes=handoff.supported_assignment_modes,
        ),
    )
    assert response.actor_key == actor_key


async def acknowledge_all(
    service: AgentTeamSetupService,
    manifest: AgentTeamMaster,
    keys: dict[str, str],
) -> None:
    for member in manifest.all_members:
        await acknowledge_member(
            service,
            topology_key=manifest.topology_key,
            actor_key=member.actor_key,
            api_key=keys[member.actor_key],
        )


async def topology_actors(
    db: AsyncSession,
    manifest: AgentTeamMaster,
) -> dict[str, AgentActor]:
    result = await db.execute(
        select(AgentActor)
        .options(
            selectinload(AgentActor.profile),
            selectinload(AgentActor.model_bindings).selectinload(
                AgentModelBinding.model_catalog
            ),
        )
        .where(
            AgentActor.name.in_(
                [member.actor_name for member in manifest.all_members]
            )
        )
    )
    by_name = {actor.name: actor for actor in result.scalars().all()}
    return {
        member.actor_key: by_name[member.actor_name]
        for member in manifest.all_members
    }


def default_candidate(actor: AgentActor) -> Candidate:
    binding = next(
        item
        for item in actor.model_bindings
        if item.is_default and item.enabled and item.model_catalog is not None
    )
    assert binding.model_catalog is not None
    return Candidate(
        actor=actor,
        binding=binding,
        catalog=binding.model_catalog,
    )


@dataclass(frozen=True)
class ReadyTopology:
    manifest: AgentTeamMaster
    sink: CapturingCredentialSink
    service: AgentTeamSetupService
    actors: dict[str, AgentActor]


async def provision_ready_topology(
    db: AsyncSession,
    *,
    two_workers: bool = True,
    prefix: str | None = None,
) -> ReadyTopology:
    manifest = topology_manifest(
        two_workers=two_workers,
        prefix=prefix,
    )
    await seed_model_catalog(db, manifest)
    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db, credential_sink=sink)
    await apply_manifest(
        service,
        manifest,
        expected_revision=0,
        key=f"setup-qa-provision-{prefix or 'primary'}",
    )
    await acknowledge_all(service, manifest, sink.keys)
    status = await service.status(operator(), topology_key=manifest.topology_key)
    assert status.runtime_ready is True
    return ReadyTopology(
        manifest=manifest,
        sink=sink,
        service=service,
        actors=await topology_actors(db, manifest),
    )


async def routing_base(
    db: AsyncSession,
    *,
    topology: ReadyTopology,
    actor_key: str,
    team_member_factory: Any,
    task_factory: Any,
    title: str,
    skill_key: str = "backend-python",
    iteration: Any = None,
) -> ScenarioBase:
    actor = topology.actors[actor_key]
    assert actor.profile is not None
    member = await team_member_factory(
        profile=actor.profile,
        iteration=iteration,
    )
    task = await task_factory(
        iteration=iteration,
        assignee=member,
        title=title,
        description=_TASK_BRIEF,
        tags=json.dumps(["agent", f"cap:{skill_key}"]),
        priority=2,
        effort_days=1,
        status="planned",
        start_date=date(2026, 7, 20),
        end_date=date(2026, 7, 24),
    )
    await db.commit()
    return ScenarioBase(
        pm=topology.actors[topology.manifest.controller.actor_key],
        task=task,
        profile=actor.profile,
        member=member,
    )


@pytest.mark.asyncio
async def test_setup_scenarios_01_02_fresh_multi_worker_and_noop_reapply(
    db_session: AsyncSession,
) -> None:
    manifest = topology_manifest()
    await seed_model_catalog(db_session, manifest)
    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)

    _, initial_request, initial_command, initial = await apply_manifest(
        service,
        manifest,
        expected_revision=0,
        key="setup-qa-fresh",
    )
    assert initial.status == "completed"
    assert initial.resulting_topology_revision == 1
    assert len(sink.keys) == 4
    await acknowledge_all(service, manifest, sink.keys)

    actors_before = await topology_actors(db_session, manifest)
    hashes_before = {
        key: actor.api_key_hash for key, actor in actors_before.items()
    }
    actor_count_before = await db_session.scalar(
        select(func.count(AgentActor.id))
    )
    binding_count_before = await db_session.scalar(
        select(func.count(AgentModelBinding.id))
    )

    _, noop_request, noop_command, noop = await apply_manifest(
        service,
        manifest,
        expected_revision=1,
        key="setup-qa-noop",
    )
    assert noop.status == "completed"
    assert noop.resulting_topology_revision == 1
    assert {receipt.operation for receipt in noop.receipts} == {"no_change"}
    replay = await service.apply(
        operator(),
        noop_request,
        command=noop_command,
    )
    assert replay.replayed is True
    assert replay.apply_id == noop.apply_id
    initial_replay = await service.apply(
        operator(),
        initial_request,
        command=initial_command,
    )
    assert initial_replay.replayed is True
    assert initial_replay.apply_id == initial.apply_id

    actors_after = await topology_actors(db_session, manifest)
    assert {
        key: actor.id for key, actor in actors_after.items()
    } == {
        key: actor.id for key, actor in actors_before.items()
    }
    assert {
        key: actor.api_key_hash for key, actor in actors_after.items()
    } == hashes_before
    assert await db_session.scalar(select(func.count(AgentActor.id))) == (
        actor_count_before
    )
    assert await db_session.scalar(
        select(func.count(AgentModelBinding.id))
    ) == binding_count_before

    report = await service.report(
        operator(),
        topology_key=manifest.topology_key,
    )
    assert report.runtime_ready is True
    assert report.counts.desired == 4
    assert report.counts.runtime_ready == 4
    assert report.counts.blocked == 0
    assert report.evidence.apply_runs == 2
    assert report.availability == "availability_unknown"


@pytest.mark.asyncio
async def test_setup_scenario_03_runtime_handoff_failure_resumes_in_place(
    db_session: AsyncSession,
) -> None:
    manifest = topology_manifest(two_workers=False)
    await seed_model_catalog(db_session, manifest)
    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)
    await apply_manifest(
        service,
        manifest,
        expected_revision=0,
        key="setup-qa-handoff",
    )
    worker = manifest.workers[0]
    status = await service.status(
        operator(),
        topology_key=manifest.topology_key,
    )
    worker_status = next(
        item for item in status.members if item.actor_key == worker.actor_key
    )
    handoff = worker_status.handoff
    assert handoff is not None
    actor_id = worker_status.actor_id
    actor_count = await db_session.scalar(select(func.count(AgentActor.id)))

    with pytest.raises(
        AgentTeamSetupConflictError,
        match="package identity",
    ) as conflict:
        await service.acknowledge_runtime(
            sink.keys[worker.actor_key],
            AgentTeamRuntimeAcknowledgement(
                topology_key=handoff.topology_key,
                topology_revision=handoff.topology_revision,
                actor_key=handoff.actor_key,
                role=handoff.role,
                skill_package=handoff.skill_package.model_copy(
                    update={"version": "9.9.9"}
                ),
                profile_revision=handoff.profile_revision,
                model_binding_revisions=handoff.model_binding_revisions,
                server_features=handoff.required_server_features,
                supported_assignment_modes=handoff.supported_assignment_modes,
            ),
        )
    assert conflict.value.code == "agent_team_ack_package_mismatch"
    blocked = await service.status(
        operator(),
        topology_key=manifest.topology_key,
    )
    assert next(
        item for item in blocked.members if item.actor_key == worker.actor_key
    ).runtime_ready is False

    await acknowledge_all(service, manifest, sink.keys)
    ready = await service.status(
        operator(),
        topology_key=manifest.topology_key,
    )
    resumed_worker = next(
        item for item in ready.members if item.actor_key == worker.actor_key
    )
    assert resumed_worker.actor_id == actor_id
    assert resumed_worker.runtime_ready is True
    assert await db_session.scalar(select(func.count(AgentActor.id))) == (
        actor_count
    )


@pytest.mark.asyncio
async def test_setup_scenario_04_adopts_without_credential_rotation(
    db_session: AsyncSession,
) -> None:
    manifest = topology_manifest(two_workers=False)
    await seed_model_catalog(db_session, manifest)
    worker = manifest.workers[0]
    existing_key = "existing-worker-key"
    existing = AgentActor(
        name=worker.actor_name,
        display_name="Compatible existing worker",
        api_key_hash=hash_api_key(existing_key),
        scopes=json.dumps(
            list(ROLE_SCOPE_PRESETS["worker-v1"]),
            separators=(",", ":"),
        ),
        enabled=True,
        lifecycle_state="active",
        role="worker",
        queue_revision=3,
    )
    db_session.add(existing)
    await db_session.commit()
    original_hash = existing.api_key_hash
    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)

    plan = await service.plan(
        operator(),
        AgentTeamPlanRequest(
            manifest=manifest,
            expected_topology_revision=0,
        ),
    )
    adoption = next(
        action
        for action in plan.actions
        if action.actor_key == worker.actor_key
    )
    assert adoption.operation == "adopt_member"
    assert adoption.target_actor_id == existing.id
    assert adoption.requires_explicit_confirmation is True
    _, _, _, applied = await apply_manifest(
        service,
        manifest,
        expected_revision=0,
        key="setup-qa-adopt",
        confirm_required=True,
    )
    assert applied.status == "completed"
    assert worker.actor_key not in sink.keys
    await db_session.refresh(existing)
    assert existing.api_key_hash == original_hash

    keys = {**sink.keys, worker.actor_key: existing_key}
    await acknowledge_all(service, manifest, keys)
    actors = await topology_actors(db_session, manifest)
    assert actors[worker.actor_key].id == existing.id
    assert actors[worker.actor_key].api_key_hash == original_hash


@pytest.mark.asyncio
async def test_setup_scenarios_05_07_08_drift_readiness_and_redaction(
    db_session: AsyncSession,
) -> None:
    duplicate = topology_payload()
    duplicate["workers"][1]["actor_name"] = duplicate["workers"][0][
        "actor_name"
    ]
    with pytest.raises(ValidationError, match="actor_name"):
        AgentTeamMaster.model_validate(duplicate)
    no_workers = topology_payload(two_workers=False)
    no_workers["workers"] = []
    with pytest.raises(ValidationError):
        AgentTeamMaster.model_validate(no_workers)

    no_verifier = topology_manifest(
        two_workers=False,
        include_verifier=False,
    )
    await seed_model_catalog(db_session, no_verifier)
    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)
    await apply_manifest(
        service,
        no_verifier,
        expected_revision=0,
        key="setup-qa-no-verifier",
    )
    await acknowledge_all(service, no_verifier, sink.keys)
    missing_verifier = await service.status(
        operator(),
        topology_key=no_verifier.topology_key,
    )
    assert missing_verifier.runtime_ready is False
    assert "independent_verifier_not_runtime_ready" in (
        missing_verifier.blocker_codes
    )

    with pytest.raises(AgentTeamSetupConflictError) as stale:
        await service.plan(
            operator(),
            AgentTeamPlanRequest(
                manifest=no_verifier,
                expected_topology_revision=0,
            ),
        )
    assert stale.value.code == "agent_team_topology_revision_conflict"

    actors = await topology_actors(db_session, no_verifier)
    pm = actors[no_verifier.controller.actor_key]
    worker = actors[no_verifier.workers[0].actor_key]
    worker.scopes = "[]"
    assert worker.model_bindings[0].model_catalog is not None
    worker.model_bindings[0].model_catalog.enabled = False
    worker.model_bindings[0].model_catalog.revision += 1
    worker.queue_revision += 1
    outsider = AgentActor(
        name="unmanaged-qualification-worker",
        display_name="Unmanaged qualification worker",
        api_key_hash="unmanaged",
        scopes=json.dumps(list(ROLE_SCOPE_PRESETS["worker-v1"])),
        enabled=True,
        lifecycle_state="active",
        role="worker",
        profile_id=worker.profile_id,
    )
    db_session.add(outsider)
    await db_session.commit()

    drifted = await service.status(
        operator(),
        topology_key=no_verifier.topology_key,
    )
    drifted_worker = next(
        item
        for item in drifted.members
        if item.actor_key == no_verifier.workers[0].actor_key
    )
    assert {
        "actor_scope_mismatch",
        "model_binding_missing_or_disabled",
    }.issubset(drifted_worker.blocker_codes)
    boundary = await service.membership_boundary(pm.id)
    assert boundary is not None
    assert worker.id not in boundary.runtime_ready_actor_ids
    roster = await AgentWorkService(db_session).list_actor_roster(pm)
    roster_ids = {item.id for item in roster}
    assert worker.id not in roster_ids
    assert outsider.id not in roster_ids
    with pytest.raises(AgentTeamSetupConflictError) as dispatch_conflict:
        await service.require_dispatch_member(pm, worker.id)
    assert dispatch_conflict.value.code == "agent_team_actor_outside_topology"

    report = await service.report(
        operator(),
        topology_key=no_verifier.topology_key,
    )
    serialized = report.model_dump_json()
    assert report.counts.blocked >= 1
    assert report.dispatch_context.state == "availability_unknown"
    assert "pmag_" not in serialized
    assert "runtime://" not in serialized
    assert "credential_ref" not in serialized
    assert "raw_log" not in serialized


@pytest.mark.asyncio
async def test_setup_scenario_06_add_binding_change_and_explicit_disable(
    db_session: AsyncSession,
) -> None:
    initial_manifest = topology_manifest(two_workers=False)
    expanded_manifest = topology_manifest(two_workers=True)
    await seed_model_catalog(db_session, expanded_manifest)
    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db_session, credential_sink=sink)
    await apply_manifest(
        service,
        initial_manifest,
        expected_revision=0,
        key="setup-qa-change-initial",
    )
    await acknowledge_all(service, initial_manifest, sink.keys)

    _, _, _, added = await apply_manifest(
        service,
        expanded_manifest,
        expected_revision=1,
        key="setup-qa-add-worker",
    )
    assert added.resulting_topology_revision == 2
    assert any(
        receipt.actor_key == "operations-worker"
        and receipt.operation == "create_member"
        for receipt in added.receipts
    )
    await acknowledge_member(
        service,
        topology_key=expanded_manifest.topology_key,
        actor_key="operations-worker",
        api_key=sink.keys["operations-worker"],
    )

    changed_payload = topology_payload(two_workers=True)
    changed_payload["workers"][0].update(
        {
            "model_binding_keys": ["implementation-advanced"],
            "default_model_binding_key": "implementation-advanced",
        }
    )
    changed_manifest = AgentTeamMaster.model_validate(changed_payload)
    _, _, _, changed = await apply_manifest(
        service,
        changed_manifest,
        expected_revision=2,
        key="setup-qa-binding-change",
    )
    assert changed.resulting_topology_revision == 3
    await acknowledge_member(
        service,
        topology_key=changed_manifest.topology_key,
        actor_key=changed_manifest.workers[0].actor_key,
        api_key=sink.keys[changed_manifest.workers[0].actor_key],
    )
    actors = await topology_actors(db_session, changed_manifest)
    changed_actor = actors[changed_manifest.workers[0].actor_key]
    assert next(
        binding.model_catalog.key
        for binding in changed_actor.model_bindings
        if binding.is_default and binding.enabled
    ) == "implementation-advanced"

    remove_payload = changed_manifest.model_dump(mode="json")
    removed = remove_payload["workers"].pop(0)
    remove_payload["readiness_policy"]["minimum_execution_workers"] = 1
    reduced_manifest = AgentTeamMaster.model_validate(remove_payload)
    disable_plan = await service.plan(
        operator(),
        AgentTeamPlanRequest(
            manifest=reduced_manifest,
            expected_topology_revision=3,
        ),
    )
    disable_action = next(
        action
        for action in disable_plan.actions
        if action.actor_key == removed["actor_key"]
    )
    assert disable_action.operation == "disable_member"
    assert disable_action.requires_explicit_confirmation is True
    assert all(action.operation != "delete" for action in disable_plan.actions)

    _, _, _, disabled = await apply_manifest(
        service,
        reduced_manifest,
        expected_revision=3,
        key="setup-qa-explicit-disable",
        confirm_required=True,
    )
    assert disabled.resulting_topology_revision == 4
    await db_session.refresh(changed_actor)
    assert changed_actor.enabled is False
    assert changed_actor.lifecycle_state == "disabled"
    apply_runs = await db_session.scalar(
        select(func.count(AgentTeamApplyRun.id))
    )
    assert apply_runs == 4


@pytest.mark.asyncio
async def test_setup_scenario_09_live_roster_and_routing_matrix_is_topology_bound(
    db_session: AsyncSession,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    topology = await provision_ready_topology(db_session)
    routine_actor = topology.actors["backend-worker"]
    advanced_actor = topology.actors["operations-worker"]
    verifier_actor = topology.actors["independent-verifier"]
    routine = default_candidate(routine_actor)
    advanced = default_candidate(advanced_actor)
    verifier = default_candidate(verifier_actor)

    assert advanced_actor.profile is not None
    outsider = await actor_factory(
        profile=advanced_actor.profile,
        name="unmanaged-perfect-candidate",
        display_name="Unmanaged perfect candidate",
        role="worker",
        lifecycle_state="active",
        scopes=json.dumps(list(ROLE_SCOPE_PRESETS["worker-v1"])),
    )
    outsider_binding = AgentModelBinding(
        actor_id=outsider.id,
        model_catalog_id=advanced.catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=[],
        data_policy_tags=[],
        revision=1,
    )
    db_session.add(outsider_binding)
    await db_session.commit()

    routine_base = await routing_base(
        db_session,
        topology=topology,
        actor_key="backend-worker",
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Routine topology-bound backend change",
    )
    iteration = routine_base.task.iteration
    advanced_base = await routing_base(
        db_session,
        topology=topology,
        actor_key="operations-worker",
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Advanced topology-bound security change",
        skill_key="security-review",
        iteration=iteration,
    )
    assert verifier_actor.profile is not None
    await team_member_factory(
        profile=verifier_actor.profile,
        iteration=iteration,
    )
    await db_session.commit()

    roster = await AgentWorkService(db_session).list_actor_roster(
        routine_base.pm
    )
    roster_ids = {item.id for item in roster}
    assert {
        routine_actor.id,
        advanced_actor.id,
        verifier_actor.id,
    }.issubset(roster_ids)
    assert outsider.id not in roster_ids

    routine_assessment = await _create_assessment_with_parity(
        db_session,
        base=routine_base,
        data=_assessment_command(
            task_version=routine_base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="setup-qa-routine-assessment",
    )
    routine_preview = await _preview_with_parity(
        db_session,
        base=routine_base,
        assessment=routine_assessment,
    )
    assert routine_preview.topology_key == topology.manifest.topology_key
    assert routine_preview.topology_revision == 1
    assert routine_preview.recommended_candidate is not None
    assert routine_preview.recommended_candidate.actor_id == routine_actor.id

    advanced_assessment = await _create_assessment_with_parity(
        db_session,
        base=advanced_base,
        data=_assessment_command(
            task_version=advanced_base.task.version,
            required_skill_levels={"security-review": 3},
            minimum_reasoning_tier=3,
            minimum_context_tier="large",
            axes={
                "reasoning": 3,
                "ambiguity": 2,
                "context_breadth": 2,
                "risk": 3,
                "verification_burden": 3,
            },
            reason_codes=(
                "security",
                "specialist-verification",
            ),
        ),
        key="setup-qa-advanced-assessment",
    )
    advanced_preview = await _preview_with_parity(
        db_session,
        base=advanced_base,
        assessment=advanced_assessment,
    )
    assert advanced_preview.recommended_candidate is not None
    assert advanced_preview.recommended_candidate.actor_id == advanced_actor.id
    outsider_exclusion = _exclusion(
        advanced_preview,
        actor_id=outsider.id,
        binding_id=outsider_binding.id,
    )
    assert "actor_topology_incompatible" in (
        outsider_exclusion.hard_blocker_codes
    )

    no_candidate_task = await task_factory(
        iteration=iteration,
        assignee=routine_base.member,
        title="Backend task above the routine model envelope",
        description=_TASK_BRIEF,
        tags=json.dumps(["agent", "cap:backend-python"]),
        priority=2,
        effort_days=1,
        status="planned",
        start_date=date(2026, 7, 20),
        end_date=date(2026, 7, 24),
    )
    await db_session.commit()
    no_candidate_base = ScenarioBase(
        pm=routine_base.pm,
        task=no_candidate_task,
        profile=routine_base.profile,
        member=routine_base.member,
    )
    no_candidate_assessment = await _create_assessment_with_parity(
        db_session,
        base=no_candidate_base,
        data=_assessment_command(
            task_version=no_candidate_task.version,
            required_skill_levels={"backend-python": 3},
            minimum_reasoning_tier=3,
            minimum_context_tier="large",
            axes={
                "reasoning": 3,
                "ambiguity": 2,
                "context_breadth": 2,
                "risk": 2,
                "verification_burden": 2,
            },
        ),
        key="setup-qa-no-candidate-assessment",
    )
    no_candidate_preview = await _preview_with_parity(
        db_session,
        base=no_candidate_base,
        assessment=no_candidate_assessment,
    )
    assert no_candidate_preview.recommended_candidate is None
    assert no_candidate_preview.eligible_candidates == []
    assert no_candidate_preview.hard_blocker_codes == [
        "no_eligible_candidate"
    ]

    advanced_preview = await _preview_with_parity(
        db_session,
        base=advanced_base,
        assessment=advanced_assessment,
    )
    execution = await _dispatch(
        db_session,
        base=advanced_base,
        assessment=advanced_assessment,
        preview=advanced_preview,
        candidate=advanced,
        key="setup-qa-advanced-dispatch",
    )
    execution_record = await db_session.get(
        AgentTaskAssignment,
        execution.id,
    )
    assert execution_record is not None
    execution_record.state = "fulfilled"
    advanced_base.task.status = "resolved"
    await db_session.commit()

    verification_preview = await _preview_with_parity(
        db_session,
        base=advanced_base,
        assessment=advanced_assessment,
        purpose="verification",
        reviewer_profile_id=verifier_actor.profile_id,
    )
    assert verification_preview.recommended_candidate is not None
    assert verification_preview.recommended_candidate.actor_id == (
        verifier_actor.id
    )
    implementer_exclusion = _exclusion(
        verification_preview,
        actor_id=advanced_actor.id,
        binding_id=advanced.binding.id,
    )
    assert "verification_actor_not_independent" in (
        implementer_exclusion.hard_blocker_codes
    )
    verification = await _dispatch(
        db_session,
        base=advanced_base,
        assessment=advanced_assessment,
        preview=verification_preview,
        candidate=verifier,
        key="setup-qa-verification-dispatch",
        purpose="verification",
        reviewer_profile_id=verifier_actor.profile_id,
    )
    assert verification.actor_id == verifier_actor.id
    assert verification.routing_snapshot["topology_key"] == (
        topology.manifest.topology_key
    )


@pytest.mark.asyncio
async def test_setup_scenario_10_feature_off_preserves_setup_and_work_evidence(
    db_session: AsyncSession,
    team_member_factory,
    task_factory,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    topology = await provision_ready_topology(
        db_session,
        two_workers=False,
    )
    base = await routing_base(
        db_session,
        topology=topology,
        actor_key="backend-worker",
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="First rollback evidence task",
    )
    iteration = base.task.iteration
    candidate = default_candidate(topology.actors["backend-worker"])
    first_assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="setup-qa-rollback-first-assessment",
    )
    first_preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=first_assessment,
    )
    first_assignment = await _dispatch(
        db_session,
        base=base,
        assessment=first_assessment,
        preview=first_preview,
        candidate=candidate,
        key="setup-qa-rollback-first-dispatch",
    )
    db_session.add(
        AgentRun(
            task_id=base.task.id,
            actor_id=candidate.actor.id,
            assignment_id=first_assignment.id,
            status="succeeded",
            model_binding_id=candidate.binding.id,
            model_binding_revision=candidate.binding.revision,
            configured_model_alias=candidate.catalog.configured_model_alias,
            model_trust_state="unreported",
            run_metadata="{}",
            artifact_links="[]",
        )
    )

    second_task = await task_factory(
        iteration=iteration,
        assignee=base.member,
        title="Second rollback evidence task",
        description=_TASK_BRIEF,
        tags=json.dumps(["agent", "cap:backend-python"]),
        priority=2,
        effort_days=1,
        status="planned",
        start_date=date(2026, 7, 20),
        end_date=date(2026, 7, 24),
    )
    await db_session.commit()
    second_base = ScenarioBase(
        pm=base.pm,
        task=second_task,
        profile=base.profile,
        member=base.member,
    )
    second_assessment = await _create_assessment_with_parity(
        db_session,
        base=second_base,
        data=_assessment_command(
            task_version=second_task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="setup-qa-rollback-second-assessment",
    )
    second_preview = await _preview_with_parity(
        db_session,
        base=second_base,
        assessment=second_assessment,
    )
    counts_before = {
        "topologies": await db_session.scalar(
            select(func.count(AgentTeamTopology.id))
        ),
        "apply_runs": await db_session.scalar(
            select(func.count(AgentTeamApplyRun.id))
        ),
        "assignments": await db_session.scalar(
            select(func.count(AgentTaskAssignment.id))
        ),
        "runs": await db_session.scalar(select(func.count(AgentRun.id))),
    }

    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "off")
    get_settings.cache_clear()
    with pytest.raises(AgentRoutingConflictError) as inactive:
        await _dispatch(
            db_session,
            base=second_base,
            assessment=second_assessment,
            preview=second_preview,
            candidate=candidate,
            key="setup-qa-rollback-blocked-dispatch",
        )
    assert inactive.value.code == "model_aware_routing_enforcement_unavailable"
    counts_after = {
        "topologies": await db_session.scalar(
            select(func.count(AgentTeamTopology.id))
        ),
        "apply_runs": await db_session.scalar(
            select(func.count(AgentTeamApplyRun.id))
        ),
        "assignments": await db_session.scalar(
            select(func.count(AgentTaskAssignment.id))
        ),
        "runs": await db_session.scalar(select(func.count(AgentRun.id))),
    }
    assert counts_after == counts_before
    report = await topology.service.report(
        operator(),
        topology_key=topology.manifest.topology_key,
    )
    assert report.topology_revision == 1
    assert report.evidence.apply_runs == 1
    assert report.runtime_ready is True


@pytest.mark.asyncio
async def test_setup_scenario_11_compatibility_preflight_is_non_mutating(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = topology_manifest(two_workers=False)
    await seed_model_catalog(db_session, manifest)
    service = AgentTeamSetupService(
        db_session,
        credential_sink=CapturingCredentialSink(),
    )
    monkeypatch.setattr(
        AgentTeamSetupService,
        "_supported_features",
        staticmethod(lambda: frozenset({"actor-roster-v1"})),
    )

    validation = await service.validate(
        operator(),
        AgentTeamManifestRequest(manifest=manifest),
    )
    assert validation.valid is False
    assert validation.blocker_codes == ("required_server_feature_missing",)
    plan = await service.plan(
        operator(),
        AgentTeamPlanRequest(
            manifest=manifest,
            expected_topology_revision=0,
        ),
    )
    assert "required_server_feature_missing" in plan.blocker_codes
    assert {action.operation for action in plan.actions} == {"blocked"}
    assert {
        action.blocker_code for action in plan.actions
    } == {"required_server_feature_missing"}
    assert await db_session.scalar(
        select(func.count(AgentTeamTopology.id))
    ) == 0
    assert await db_session.scalar(select(func.count(AgentActor.id))) == 0


@pytest.mark.asyncio
async def test_setup_scenario_12_revision_and_cross_topology_paths_fail_closed(
    db_session: AsyncSession,
    actor_factory,
    team_member_factory,
    task_factory,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    primary = await provision_ready_topology(
        db_session,
        two_workers=False,
    )
    base = await routing_base(
        db_session,
        topology=primary,
        actor_key="backend-worker",
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Membership revision qualification task",
    )
    candidate = default_candidate(primary.actors["backend-worker"])
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="setup-qa-revision-assessment",
    )
    stale_preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )
    assert stale_preview.topology_revision == 1

    changed_payload = primary.manifest.model_dump(mode="json")
    changed_payload["workers"][0]["display_name"] = (
        "Backend Runtime After Membership Revision"
    )
    changed_manifest = AgentTeamMaster.model_validate(changed_payload)
    _, _, _, changed = await apply_manifest(
        primary.service,
        changed_manifest,
        expected_revision=1,
        key="setup-qa-membership-revision",
    )
    assert changed.resulting_topology_revision == 2
    await acknowledge_member(
        primary.service,
        topology_key=changed_manifest.topology_key,
        actor_key=changed_manifest.workers[0].actor_key,
        api_key=primary.sink.keys[changed_manifest.workers[0].actor_key],
    )
    with pytest.raises(AgentRoutingConflictError) as stale:
        await _dispatch(
            db_session,
            base=base,
            assessment=assessment,
            preview=stale_preview,
            candidate=candidate,
            key="setup-qa-stale-preview-dispatch",
        )
    assert stale.value.code == "routing_preview_stale"
    assert await db_session.scalar(
        select(func.count(AgentTaskAssignment.id))
    ) == 0

    secondary = await provision_ready_topology(
        db_session,
        two_workers=False,
        prefix="other",
    )
    secondary_worker_key = secondary.manifest.workers[0].actor_key
    secondary_worker = secondary.actors[secondary_worker_key]
    assert candidate.actor.profile is not None
    unbound = await actor_factory(
        profile=candidate.actor.profile,
        name="unbound-backend-worker",
        display_name="Unbound backend worker",
        role="worker",
        lifecycle_state="active",
        scopes=json.dumps(list(ROLE_SCOPE_PRESETS["worker-v1"])),
    )
    unbound_binding = AgentModelBinding(
        actor_id=unbound.id,
        model_catalog_id=candidate.catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=[],
        data_policy_tags=[],
        revision=1,
    )
    db_session.add(unbound_binding)
    await db_session.commit()

    refreshed_preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )
    for actor_id, binding_id in (
        (
            secondary_worker.id,
            default_candidate(secondary_worker).binding.id,
        ),
        (unbound.id, unbound_binding.id),
    ):
        exclusion = _exclusion(
            refreshed_preview,
            actor_id=actor_id,
            binding_id=binding_id,
        )
        assert "actor_topology_incompatible" in (
            exclusion.hard_blocker_codes
        )

    work_service = AgentWorkService(db_session)
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "off")
    get_settings.cache_clear()
    for target in (secondary_worker, unbound):
        with pytest.raises(AgentTeamSetupConflictError) as legacy:
            await work_service.create_assignment(
                base.pm,
                AgentTaskAssignmentCreate(
                    task_id=base.task.id,
                    actor_id=target.id,
                    team_member_id=base.member.id,
                    purpose="execution",
                    queue_class="normal",
                    reason="Attempt an out-of-topology legacy dispatch",
                    expected_task_version=base.task.version,
                ),
                idempotency_key=f"setup-qa-legacy-{target.id}",
                rationale="Prove legacy dispatch cannot bypass membership",
                correlation_id=f"setup-qa-legacy-{target.id}-correlation",
            )
        assert legacy.value.code == "agent_team_actor_outside_topology"

    base.task.status = "active"
    await db_session.commit()
    with pytest.raises(AgentTeamSetupConflictError) as recovery:
        await work_service.requeue_recovery(
            base.pm,
            base.task.id,
            AgentRecoveryRequeue(
                actor_id=secondary_worker.id,
                expected_task_version=base.task.version,
                expected_live_assignment_ids=[],
                expected_running_run_ids=[],
                expected_claim_generation=0,
                reason="Attempt cross-topology recovery",
            ),
            idempotency_key="setup-qa-cross-topology-recovery",
            rationale="Prove recovery cannot bypass topology membership",
            correlation_id="setup-qa-cross-topology-recovery-correlation",
        )
    assert recovery.value.code == "agent_team_actor_outside_topology"
