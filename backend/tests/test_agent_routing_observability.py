"""Security and persistence coverage for bounded routing telemetry."""

from __future__ import annotations

import json

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import TaskEvent
from app.models.outbound_webhook import OutboundWebhookEvent
from app.runtime_telemetry import metrics
from app.services.agent_routing_observability import (
    MAX_ROUTING_OPERATIONAL_CODES,
    MAX_ROUTING_OPERATIONAL_EVENT_BYTES,
    MAX_ROUTING_OPERATIONAL_EXCLUSION_CODES,
    MAX_ROUTING_OPERATIONAL_EXCLUSIONS,
    RoutingOperationalEvent,
    build_routing_operational_payload,
    record_routing_operational_event,
    routing_exclusion_projection,
)
from app.services.agent_routing_policy import canonical_routing_json_bytes
from app.services.outbound_webhook_service import KNOWN_WEBHOOK_EVENT_TYPES


_DIGEST_A = "a" * 64
_DIGEST_B = "b" * 64
_COMMON = {
    "task_version": 3,
    "policy_version": "model-aware-routing-v1",
}
_VALID_VALUES = {
    RoutingOperationalEvent.ASSESSMENT_CREATED: {
        **_COMMON,
        "assessment_id": 11,
        "assessment_task_version": 3,
        "band": "advanced",
        "review_mode": "independent",
        "reason_codes": ["migration"],
    },
    RoutingOperationalEvent.PREVIEW_RECORDED: {
        **_COMMON,
        "rollout_mode": "shadow",
        "assessment_id": 11,
        "assessment_task_version": 3,
        "purpose": "execution",
        "routing_preview_id": "preview-safe-1",
        "routing_preview_digest": _DIGEST_A,
        "input_digest": _DIGEST_B,
        "recommended_actor_id": 17,
        "recommended_model_binding_id": 19,
        "recommended_model_binding_revision": 2,
        "recommended_model_catalog_id": 37,
        "recommended_model_catalog_revision": 4,
        "hard_blocker_codes": [],
        "excluded_candidates": [
            {
                "actor_id": 23,
                "model_binding_id": 29,
                "hard_blocker_codes": ["reasoning_tier_insufficient"],
            }
        ],
    },
    RoutingOperationalEvent.NO_ELIGIBLE_CANDIDATE: {
        **_COMMON,
        "rollout_mode": "shadow",
        "assessment_id": 11,
        "assessment_task_version": 3,
        "purpose": "execution",
        "routing_preview_id": "preview-safe-2",
        "routing_preview_digest": _DIGEST_A,
        "input_digest": _DIGEST_B,
        "hard_blocker_codes": ["no_eligible_candidate"],
        "excluded_candidates": [
            {
                "actor_id": 23,
                "model_binding_id": 29,
                "hard_blocker_codes": ["data_policy_missing"],
            }
        ],
    },
    RoutingOperationalEvent.ASSIGNMENT_SELECTED: {
        **_COMMON,
        "assessment_id": 11,
        "assessment_task_version": 3,
        "assignment_id": 31,
        "actor_id": 17,
        "model_binding_id": 19,
        "model_binding_revision": 2,
        "model_catalog_id": 37,
        "model_catalog_revision": 4,
        "routing_preview_id": "preview-safe-3",
        "routing_preview_digest": _DIGEST_A,
        "purpose": "execution",
        "review_mode": "independent",
        "reason_codes": ["hard-gates-passed"],
    },
    RoutingOperationalEvent.STALE_CONFLICT: {
        **_COMMON,
        "assignment_id": 31,
        "routing_preview_id": "preview-safe-4",
        "conflict_code": "routing_preview_stale",
        "reason_codes": ["routing_preview_stale"],
    },
    RoutingOperationalEvent.CONFIGURED_OBSERVED_MISMATCH: {
        **_COMMON,
        "assignment_id": 31,
        "actor_id": 17,
        "model_binding_id": 19,
        "model_binding_revision": 2,
        "model_catalog_id": 37,
        "model_catalog_revision": 4,
        "conflict_code": "resolved_model_mismatch",
        "model_evidence_source": "worker_report",
        "model_attested": False,
        "reason_codes": ["configured_observed_mismatch"],
    },
    RoutingOperationalEvent.VERIFIER_REJECTED: {
        **_COMMON,
        "assignment_id": 41,
        "actor_id": 43,
        "review_mode": "independent",
        "failure_category": "reasoning_insufficiency",
        "lineage_digest": _DIGEST_A,
        "reason_codes": ["verifier_rejected"],
    },
    RoutingOperationalEvent.REWORK_CREATED: {
        **_COMMON,
        "source_assignment_id": 41,
        "rework_assignment_id": 47,
        "actor_id": 17,
        "failure_category": "reasoning_insufficiency",
        "lineage_digest": _DIGEST_A,
        "reason_codes": ["fresh_selection_required"],
    },
    RoutingOperationalEvent.TIER_ESCALATED: {
        **_COMMON,
        "assignment_id": 47,
        "actor_id": 17,
        "model_binding_id": 53,
        "model_binding_revision": 3,
        "model_catalog_id": 59,
        "model_catalog_revision": 5,
        "failure_category": "reasoning_insufficiency",
        "previous_reasoning_tier": 1,
        "selected_reasoning_tier": 2,
        "previous_context_tier": "small",
        "selected_context_tier": "medium",
        "reason_codes": ["governed_model_failure_escalation"],
    },
}


@pytest.mark.contract
@pytest.mark.parametrize("event", list(RoutingOperationalEvent))
def test_routing_operational_events_are_closed_redacted_and_bounded(
    event: RoutingOperationalEvent,
) -> None:
    payload = build_routing_operational_payload(event, _VALID_VALUES[event])
    encoded = canonical_routing_json_bytes(payload)

    assert len(encoded) <= MAX_ROUTING_OPERATIONAL_EVENT_BYTES
    assert payload["event"] == event.value
    assert payload["policy_version"] == "model-aware-routing-v1"
    assert "prompt" not in encoded.decode("utf-8").lower()
    assert "credential" not in encoded.decode("utf-8").lower()

    with pytest.raises(ValueError, match="unsupported fields"):
        build_routing_operational_payload(
            event,
            {
                **_VALID_VALUES[event],
                "raw_prompt": "PRIVATE-PROMPT-SENTINEL",
            },
        )


@pytest.mark.contract
@pytest.mark.parametrize("event", list(RoutingOperationalEvent))
def test_routing_operational_events_require_their_audit_identity(
    event: RoutingOperationalEvent,
) -> None:
    with pytest.raises(ValueError, match="missing required fields"):
        build_routing_operational_payload(event, {})


@pytest.mark.contract
def test_routing_failure_category_uses_a_closed_taxonomy() -> None:
    with pytest.raises(ValueError, match="failure_category must be one of"):
        build_routing_operational_payload(
            RoutingOperationalEvent.TIER_ESCALATED,
            {
                **_VALID_VALUES[RoutingOperationalEvent.TIER_ESCALATED],
                "failure_category": "caller-authored-failure",
            },
        )


@pytest.mark.contract
def test_dedicated_routing_webhook_catalog_is_complete() -> None:
    assert {
        f"agent.routing.{event.value}" for event in RoutingOperationalEvent
    }.issubset(KNOWN_WEBHOOK_EVENT_TYPES)


@pytest.mark.contract
def test_worst_case_exclusion_projection_stays_within_event_byte_cap() -> None:
    class Exclusion:
        def __init__(self, marker: int):
            self.actor_id = marker
            self.model_binding_id = marker + 100
            self.hard_blocker_codes = [
                f"blocker_{index:02d}_" + ("x" * 52)
                for index in range(20)
            ]

    exclusions = [Exclusion(marker) for marker in range(1, 51)]
    projection = routing_exclusion_projection(exclusions)

    assert len(projection["excluded_candidates"]) == (
        MAX_ROUTING_OPERATIONAL_EXCLUSIONS
    )
    assert all(
        len(candidate["hard_blocker_codes"])
        == MAX_ROUTING_OPERATIONAL_EXCLUSION_CODES
        for candidate in projection["excluded_candidates"]
    )
    assert projection["excluded_candidate_count"] == 50
    assert projection["excluded_candidate_projection_truncated"] is True

    payload = build_routing_operational_payload(
        RoutingOperationalEvent.PREVIEW_RECORDED,
        {
            **_VALID_VALUES[RoutingOperationalEvent.PREVIEW_RECORDED],
            "routing_preview_id": "p" * 255,
            "hard_blocker_codes": [
                f"top_{index:02d}_" + ("y" * 57)
                for index in range(MAX_ROUTING_OPERATIONAL_CODES)
            ],
            **projection,
        },
    )

    assert (
        len(canonical_routing_json_bytes(payload))
        <= MAX_ROUTING_OPERATIONAL_EVENT_BYTES
    )


@pytest.mark.asyncio
async def test_routing_operational_event_stages_equivalent_task_and_webhook_rows(
    db_session: AsyncSession,
    actor_factory,
    task_factory,
) -> None:
    actor = await actor_factory()
    task = await task_factory()
    await db_session.commit()

    task_event_id = await record_routing_operational_event(
        db_session,
        event=RoutingOperationalEvent.ASSESSMENT_CREATED,
        task_id=task.id,
        actor_id=actor.id,
        correlation_id="corr-routing-observability",
        values=_VALID_VALUES[RoutingOperationalEvent.ASSESSMENT_CREATED],
        commit=True,
    )

    task_event = await db_session.get(TaskEvent, task_event_id)
    webhook_event = (
        await db_session.execute(
            select(OutboundWebhookEvent).where(
                OutboundWebhookEvent.event_type
                == "agent.routing.assessment_created"
            )
        )
    ).scalar_one()
    task_payload = json.loads(task_event.payload)

    assert task_payload == webhook_event.payload_json
    assert task_payload["assessment_id"] == 11
    routing_metric_lines = [
        line
        for line in metrics.render_prometheus().splitlines()
        if line.startswith("workchord_agent_routing_events_total{")
    ]
    assert any(
        line.startswith(
            'workchord_agent_routing_events_total{event="assessment_created"}'
        )
        for line in routing_metric_lines
    )
    assert all("task_id" not in line for line in routing_metric_lines)
    assert all("actor_id" not in line for line in routing_metric_lines)
    assert all("model_binding_id" not in line for line in routing_metric_lines)
