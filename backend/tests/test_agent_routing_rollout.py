"""Focused qualification for model-aware routing rollout controls."""

from __future__ import annotations

from datetime import date
import json
from typing import Any

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.agent_contract import (
    MODEL_AWARE_ROUTING_FEATURE,
    agent_contract_features,
)
from app.config import Settings, get_settings
from app.main import app as main_app
from app.mcp_agent_tools import get_agent_capabilities as get_mcp_capabilities
from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTaskAssignment,
    TaskEvent,
)
from app.models.outbound_webhook import OutboundWebhookEvent
from app.routers.agent import get_agent_capabilities as get_rest_capabilities
from app.schemas.agent import (
    AgentReviewVerdict,
    AgentRoutingRolloutStatusResponse,
)
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.agent_routing_observability import (
    RoutingOperationalEvent,
    record_routing_operational_event,
)
from app.services.agent_routing_policy import canonical_routing_json_bytes
from app.services.agent_skill_bundle_service import AgentSkillBundleService
from app.services.agent_routing_rollout import (
    AgentRoutingRolloutError,
    AgentRoutingRolloutMode,
    AgentRoutingRolloutService,
    AgentRoutingTopologyReadiness,
    reset_agent_routing_topology_readiness,
    set_agent_routing_topology_readiness,
)
from app.services.agent_work_service import AgentWorkService
from app.utils.time import utc_now


_TASK_BRIEF = """## Goal
Complete the bounded rollout queue check.

## Context and sources
Use the repository contracts.

## Scope
Check the assigned task.

## Out of scope
Unrelated behavior.

## Acceptance criteria
The authoritative work decision is consistent with begin.

## Verification
Run the focused qualification.

## Open questions
None
"""


def _settings(mode: str) -> Settings:
    return Settings(
        _env_file=None,
        model_aware_routing_mode=mode,
    )


def _assert_secret_free(value: Any) -> None:
    forbidden = ("secret", "password", "token", "credential", "prompt")
    if isinstance(value, dict):
        for key, item in value.items():
            assert not any(marker in key.lower() for marker in forbidden)
            _assert_secret_free(item)
    elif isinstance(value, list):
        for item in value:
            _assert_secret_free(item)
    elif isinstance(value, str):
        assert not any(marker in value.lower() for marker in forbidden)


def test_rollout_configuration_defaults_off_and_rejects_unknown_modes() -> None:
    assert _settings("off").model_aware_routing_mode == "off"
    with pytest.raises(ValidationError):
        _settings("automatic")


def test_unconfigured_runtime_context_is_off_and_unadvertised(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("MODEL_AWARE_ROUTING_MODE", raising=False)
    get_settings.cache_clear()
    try:
        status = AgentRoutingRolloutService().status()
    finally:
        get_settings.cache_clear()

    assert status.configured_mode == AgentRoutingRolloutMode.OFF
    assert status.effective_mode == AgentRoutingRolloutMode.OFF
    assert status.feature_advertised is False
    assert status.topology_readiness == (
        AgentRoutingTopologyReadiness.unavailable()
    )


def test_topology_readiness_contract_is_versioned_bounded_and_fail_closed() -> None:
    unavailable = AgentRoutingTopologyReadiness.unavailable()
    assert unavailable.as_dict() == {
        "schema_version": "model-aware-routing-topology-readiness-v1",
        "status": "unavailable",
        "source": "unavailable",
        "topology_id": None,
        "topology_revision": None,
        "blocker_codes": ["topology_readiness_unavailable"],
    }

    ready = AgentRoutingTopologyReadiness.ready(
        topology_id="primary-agent-team",
        topology_revision=7,
    )
    assert ready.as_dict()["source"] == "agent-team-master-v1"
    assert ready.as_dict()["status"] == "ready"

    with pytest.raises(ValueError, match="schema version"):
        AgentRoutingTopologyReadiness(
            schema_version="model-aware-routing-topology-readiness-v2"
        )
    with pytest.raises(ValueError, match="bounded stable identifier"):
        AgentRoutingTopologyReadiness.ready(
            topology_id="contains whitespace",
            topology_revision=1,
        )
    with pytest.raises(ValueError, match="requires blockers"):
        AgentRoutingTopologyReadiness.not_ready(
            topology_id="primary-agent-team",
            topology_revision=1,
            blocker_codes=(),
        )


@pytest.mark.parametrize("configured_mode", ("shadow", "enforced"))
def test_non_off_modes_fail_closed_without_ready_topology(
    configured_mode: str,
) -> None:
    service = AgentRoutingRolloutService(
        settings_override=_settings(configured_mode),
        topology_readiness=AgentRoutingTopologyReadiness.unavailable(),
    )

    status = service.status()

    assert status.configured_mode.value == configured_mode
    assert status.effective_mode == AgentRoutingRolloutMode.OFF
    assert status.feature_advertised is False
    assert "model_aware_routing_topology_not_ready" in status.blocker_codes
    assert MODEL_AWARE_ROUTING_FEATURE not in agent_contract_features(
        include_skill_bundles=False,
        model_aware_routing_mode=status.effective_mode.value,
    )
    with pytest.raises(AgentRoutingRolloutError) as preview:
        service.require_preview()
    assert preview.value.code == "model_aware_routing_preview_unavailable"


def test_ready_shadow_allows_preview_but_never_enforced_dispatch() -> None:
    service = AgentRoutingRolloutService(
        settings_override=_settings("shadow"),
        topology_readiness=AgentRoutingTopologyReadiness.ready(
            topology_id="primary-agent-team",
            topology_revision=7,
        ),
    )

    status = service.require_preview()

    assert status.effective_mode == AgentRoutingRolloutMode.SHADOW
    assert status.feature_advertised is True
    assert MODEL_AWARE_ROUTING_FEATURE in agent_contract_features(
        include_skill_bundles=False,
        model_aware_routing_mode=status.effective_mode.value,
    )
    with pytest.raises(AgentRoutingRolloutError) as enforced:
        service.require_enforced_dispatch()
    assert enforced.value.code == "model_aware_routing_shadow_only"


def test_ready_enforced_mode_allows_preview_and_enforced_dispatch() -> None:
    service = AgentRoutingRolloutService(
        settings_override=_settings("enforced"),
        topology_readiness=AgentRoutingTopologyReadiness.ready(
            topology_id="primary-agent-team",
            topology_revision=7,
        ),
    )

    assert service.require_preview() == service.require_enforced_dispatch()
    status = service.status()
    response = AgentRoutingRolloutStatusResponse.model_validate(status.as_dict())

    assert status.effective_mode == AgentRoutingRolloutMode.ENFORCED
    assert response.feature_advertised is True
    assert response.topology_readiness.topology_revision == 7
    _assert_secret_free(response.model_dump(mode="json"))


@pytest.mark.asyncio
async def test_rest_and_mcp_capabilities_share_fail_closed_rollout_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = AgentActor(
        id=1,
        name="routing-rollout-reader",
        display_name="Routing Rollout Reader",
        api_key_hash="routing-rollout-capabilities-hash",
        scopes=json.dumps(["assignments:read"]),
        enabled=True,
        role="pm",
        work_policy="assigned_only",
        max_parallel_work=1,
        queue_revision=1,
        created_at=utc_now(),
    )

    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "enforced")
    get_settings.cache_clear()
    readiness_token = set_agent_routing_topology_readiness(
        AgentRoutingTopologyReadiness.unavailable()
    )

    try:
        request = Request(
            {
                "type": "http",
                "method": "GET",
                "path": "/api/agent/capabilities",
                "headers": [],
                "app": main_app,
            }
        )
        rest_response = await get_rest_capabilities(
            request,
            actor,
            AgentWorkService(None),
            AgentSkillBundleService(),
        )
        rest = rest_response.model_dump(mode="json")
        mcp = await get_mcp_capabilities(None, actor)
    finally:
        reset_agent_routing_topology_readiness(readiness_token)
        get_settings.cache_clear()

    assert rest["model_aware_routing"] == mcp["model_aware_routing"]
    assert rest["features"] == mcp["features"]
    assert rest["model_aware_routing"] == {
        "configured_mode": "enforced",
        "effective_mode": "off",
        "feature_advertised": False,
        "blocker_codes": ["model_aware_routing_topology_not_ready"],
        "topology_readiness": {
            "schema_version": "model-aware-routing-topology-readiness-v1",
            "status": "unavailable",
            "source": "unavailable",
            "topology_id": None,
            "topology_revision": None,
            "blocker_codes": ["topology_readiness_unavailable"],
        },
    }
    assert MODEL_AWARE_ROUTING_FEATURE not in rest["features"]
    _assert_secret_free(rest["model_aware_routing"])


@pytest.mark.asyncio
async def test_rest_and_mcp_preserve_maximum_readiness_blocker_projection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = AgentActor(
        id=1,
        name="routing-readiness-reader",
        display_name="Routing Readiness Reader",
        api_key_hash="routing-readiness-capabilities-hash",
        scopes=json.dumps(["assignments:read"]),
        enabled=True,
        role="pm",
        work_policy="assigned_only",
        max_parallel_work=1,
        queue_revision=1,
        created_at=utc_now(),
    )
    blocker_codes = tuple(
        f"topology_blocker_{index:02d}" for index in range(20)
    )
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "enforced")
    get_settings.cache_clear()
    readiness_token = set_agent_routing_topology_readiness(
        AgentRoutingTopologyReadiness.not_ready(
            topology_id="primary-agent-team",
            topology_revision=7,
            blocker_codes=blocker_codes,
        )
    )

    try:
        request = Request(
            {
                "type": "http",
                "method": "GET",
                "path": "/api/agent/capabilities",
                "headers": [],
                "app": main_app,
            }
        )
        rest_response = await get_rest_capabilities(
            request,
            actor,
            AgentWorkService(None),
            AgentSkillBundleService(),
        )
        rest = rest_response.model_dump(mode="json")
        mcp = await get_mcp_capabilities(None, actor)
    finally:
        reset_agent_routing_topology_readiness(readiness_token)
        get_settings.cache_clear()

    assert rest["model_aware_routing"] == mcp["model_aware_routing"]
    status = rest["model_aware_routing"]
    assert status["blocker_codes"] == [
        "model_aware_routing_topology_not_ready"
    ]
    assert status["topology_readiness"]["blocker_codes"] == list(
        blocker_codes
    )
    AgentRoutingRolloutStatusResponse.model_validate(status)


@pytest.mark.asyncio
async def test_feature_off_rollback_preserves_representative_routing_history(
    db_session: AsyncSession,
    actor_factory,
    task_factory,
) -> None:
    worker = await actor_factory()
    task = await task_factory()
    catalog = AgentModelCatalogEntry(
        key="rollback-routine",
        provider="test-provider",
        configured_model_alias="runtime-rollback-routine",
        reasoning_tier=1,
        context_tier="small",
        modality_tags=["text"],
        cost_tier="low",
        latency_tier="fast",
        enabled=True,
        revision=2,
    )
    db_session.add(catalog)
    await db_session.flush()
    binding = AgentModelBinding(
        actor_id=worker.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=[],
        data_policy_tags=[],
        revision=3,
    )
    db_session.add(binding)
    await db_session.flush()
    snapshot = {
        "schema_version": "routing-decision-snapshot-v1",
        "policy_version": "model-aware-routing-v1",
        "task_id": task.id,
        "task_version": task.version,
        "actor_id": worker.id,
        "model_binding_id": binding.id,
        "model_binding_revision": binding.revision,
        "model_catalog_id": catalog.id,
        "model_catalog_revision": catalog.revision,
        "routing_preview_id": "rollback-preview",
        "routing_preview_digest": "a" * 64,
    }
    assignment = AgentTaskAssignment(
        task_id=task.id,
        actor_id=worker.id,
        purpose="execution",
        queue_class="normal",
        state="fulfilled",
        queue_rank=1000,
        task_version=task.version,
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        routing_snapshot=canonical_routing_json_bytes(snapshot).decode("utf-8"),
    )
    db_session.add(assignment)
    await db_session.flush()
    run = AgentRun(
        task_id=task.id,
        actor_id=worker.id,
        assignment_id=assignment.id,
        status="succeeded",
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        configured_model_alias=catalog.configured_model_alias,
        resolved_model_id=catalog.key,
        model_trust_state="matched",
        model_match_basis="catalog_key",
        model=catalog.configured_model_alias,
    )
    db_session.add(run)
    await db_session.flush()
    task_event_id = await record_routing_operational_event(
        db_session,
        event=RoutingOperationalEvent.ASSIGNMENT_SELECTED,
        task_id=task.id,
        actor_id=worker.id,
        values={
            "task_version": task.version,
            "policy_version": "model-aware-routing-v1",
            "rollout_mode": "enforced",
            "assessment_id": 1,
            "assessment_task_version": task.version,
            "assignment_id": assignment.id,
            "actor_id": worker.id,
            "model_binding_id": binding.id,
            "model_binding_revision": binding.revision,
            "model_catalog_id": catalog.id,
            "model_catalog_revision": catalog.revision,
            "routing_preview_id": "rollback-preview",
            "routing_preview_digest": "a" * 64,
            "purpose": "execution",
            "review_mode": "none",
            "reason_codes": ["eligible"],
        },
    )
    await db_session.commit()

    preserved_ids = {
        "task": task.id,
        "assignment": assignment.id,
        "run": run.id,
        "event": task_event_id,
    }
    enforced = AgentRoutingRolloutService(
        settings_override=_settings("enforced"),
        topology_readiness=AgentRoutingTopologyReadiness.ready(
            topology_id="primary-agent-team",
            topology_revision=7,
        ),
    )
    assert enforced.status().feature_advertised is True

    rolled_back = AgentRoutingRolloutService(
        settings_override=_settings("off"),
        topology_readiness=AgentRoutingTopologyReadiness.ready(
            topology_id="primary-agent-team",
            topology_revision=7,
        ),
    )
    rollback_status = rolled_back.status()
    assert rollback_status.effective_mode == AgentRoutingRolloutMode.OFF
    assert rollback_status.feature_advertised is False
    assert MODEL_AWARE_ROUTING_FEATURE not in agent_contract_features(
        include_skill_bundles=False,
        model_aware_routing_mode=rollback_status.effective_mode.value,
    )
    assert (
        AgentWorkService(
            None,
            rollout_service=rolled_back,
        )._require_supervised_routing()
        == rollback_status
    )

    db_session.expire_all()
    preserved_assignment = await db_session.get(
        AgentTaskAssignment,
        preserved_ids["assignment"],
    )
    preserved_run = await db_session.get(AgentRun, preserved_ids["run"])
    preserved_event = await db_session.get(TaskEvent, preserved_ids["event"])
    preserved_webhook = (
        await db_session.execute(
            select(OutboundWebhookEvent).where(
                OutboundWebhookEvent.event_type
                == "agent.routing.assignment_selected",
                OutboundWebhookEvent.entity_id == preserved_ids["task"],
            )
        )
    ).scalar_one()

    assert json.loads(preserved_assignment.routing_snapshot) == snapshot
    assert preserved_assignment.model_binding_revision == 3
    assert preserved_run.model_binding_revision == 3
    assert preserved_run.model_trust_state == "matched"
    assert json.loads(preserved_event.payload) == preserved_webhook.payload_json


@pytest.mark.asyncio
async def test_rollback_blocks_queued_model_aware_work_until_enforced(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    profile = await profile_factory(assignment_modes=["execution"])
    member = await team_member_factory(profile=profile)
    worker = await actor_factory(
        profile=profile,
        scopes=json.dumps(["work:execute", "assignments:read", "tasks:read"]),
    )
    task = await task_factory(
        assignee=member,
        description=_TASK_BRIEF,
        tags=json.dumps(["agent", "cap:backend-python"]),
        start_date=date(2026, 7, 20),
        end_date=date(2026, 7, 24),
    )
    catalog = AgentModelCatalogEntry(
        key="rollback-queued",
        provider="test-provider",
        configured_model_alias="runtime-rollback-queued",
        reasoning_tier=1,
        context_tier="small",
        modality_tags=["text"],
        cost_tier="low",
        latency_tier="fast",
        enabled=True,
        revision=1,
    )
    db_session.add(catalog)
    await db_session.flush()
    binding = AgentModelBinding(
        actor_id=worker.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=[],
        data_policy_tags=[],
        revision=1,
    )
    db_session.add(binding)
    await db_session.flush()
    assignment = AgentTaskAssignment(
        task_id=task.id,
        actor_id=worker.id,
        team_member_id=member.id,
        purpose="execution",
        queue_class="normal",
        state="queued",
        queue_rank=1000,
        task_version=task.version,
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        routing_snapshot=canonical_routing_json_bytes(
            {
                "schema_version": "routing-decision-snapshot-v1",
                "selection_pending": False,
                "policy_version": "model-aware-routing-v1",
            }
        ).decode("utf-8"),
    )
    db_session.add(assignment)
    await db_session.commit()

    readiness = AgentRoutingTopologyReadiness.ready(
        topology_id="primary-agent-team",
        topology_revision=7,
    )
    for mode in ("off", "shadow"):
        service = AgentWorkService(
            db_session,
            rollout_service=AgentRoutingRolloutService(
                settings_override=_settings(mode),
                topology_readiness=readiness,
            ),
        )
        decision = await service.get_work(worker)
        assert decision.state == "wait"
        assert decision.next is not None
        assert (
            "model_aware_assignment_inactive"
            in decision.next.blocker_codes
        )

    enforced_service = AgentWorkService(
        db_session,
        rollout_service=AgentRoutingRolloutService(
            settings_override=_settings("enforced"),
            topology_readiness=readiness,
        ),
    )
    enforced_decision = await enforced_service.get_work(worker)
    assert enforced_decision.state == "start_assigned"
    assert enforced_decision.next is not None
    assert (
        "model_aware_assignment_inactive"
        not in enforced_decision.next.blocker_codes
    )


@pytest.mark.parametrize("mode", ("off", "shadow"))
@pytest.mark.asyncio
async def test_inactive_rollout_blocks_queued_model_aware_verification_review(
    mode: str,
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    task_factory,
) -> None:
    verifier_profile = await profile_factory(
        assignment_modes=["verification"]
    )
    verifier = await actor_factory(
        profile=verifier_profile,
        role="verifier",
        scopes=json.dumps(["verification:read", "verification:write"]),
    )
    task = await task_factory(status="resolved")
    assignment = AgentTaskAssignment(
        task_id=task.id,
        actor_id=verifier.id,
        purpose="verification",
        queue_class="normal",
        state="queued",
        queue_rank=1000,
        task_version=task.version,
        routing_snapshot=canonical_routing_json_bytes(
            {
                "schema_version": "routing-decision-snapshot-v1",
                "selection_pending": False,
                "policy_version": "model-aware-routing-v1",
            }
        ).decode("utf-8"),
    )
    db_session.add(assignment)
    await db_session.commit()
    service = AgentWorkService(
        db_session,
        rollout_service=AgentRoutingRolloutService(
            settings_override=_settings(mode),
            topology_readiness=AgentRoutingTopologyReadiness.ready(
                topology_id="primary-agent-team",
                topology_revision=7,
            ),
        ),
    )

    with pytest.raises(AgentRoutingConflictError) as conflict:
        await service.review(
            verifier,
            AgentReviewVerdict(
                assignment_id=assignment.id,
                verdict="pass",
                expected_task_version=task.version,
                evidence={"result": "verified"},
            ),
            idempotency_key=f"inactive-review-{mode}",
            rationale="Do not action queued model-aware review while inactive.",
            correlation_id=f"corr-inactive-review-{mode}",
        )

    assert conflict.value.code == "model_aware_assignment_inactive"
    await db_session.refresh(task)
    await db_session.refresh(assignment)
    assert task.status == "resolved"
    assert assignment.state == "queued"
