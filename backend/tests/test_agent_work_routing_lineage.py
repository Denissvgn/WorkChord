"""Focused assignment/run evidence tests that do not require a database."""

from datetime import UTC, datetime
import hashlib
import json

import pytest
from pydantic import ValidationError

from app.models.agent import AgentRun, AgentTaskAssignment
from app.models.task import Task
from app.schemas.agent import (
    ModelAwareAgentTaskAssignmentCreate,
    ModelAwareAgentWorkBegin,
)
from app.services.agent_routing_policy import canonical_routing_json_bytes
from app.services.agent_routing_service import (
    AgentRoutingConflictError,
    AgentRoutingService,
)
from app.services.agent_work_service import AgentWorkService


def _assignment(
    *,
    assignment_id: int,
    snapshot: dict[str, object],
    reviewer_profile_id: int | None = None,
) -> AgentTaskAssignment:
    timestamp = datetime(2026, 7, 27, 12, assignment_id, tzinfo=UTC)
    return AgentTaskAssignment(
        id=assignment_id,
        task_id=7,
        actor_id=10 + assignment_id,
        purpose="execution",
        queue_class="normal",
        state="fulfilled",
        queue_rank=assignment_id,
        reviewer_profile_id=reviewer_profile_id,
        task_version=3,
        routing_snapshot=canonical_routing_json_bytes(snapshot).decode("utf-8"),
        created_at=timestamp,
        updated_at=timestamp,
    )


@pytest.mark.contract
def test_model_aware_commands_own_selection_and_observed_model_fields() -> None:
    digest = "a" * 64
    assignment = ModelAwareAgentTaskAssignmentCreate(
        task_id=7,
        actor_id=11,
        expected_task_version=3,
        purpose="execution",
        assessment_id=5,
        model_binding_id=13,
        model_binding_revision=2,
        routing_preview_id="preview-id",
        routing_preview_digest=digest,
    )
    begin = ModelAwareAgentWorkBegin(
        assignment_id=17,
        queue_revision=4,
        model_binding_id=13,
        model_binding_revision=2,
        resolved_model_id="catalog-key",
    )

    assert "routing_snapshot" not in ModelAwareAgentTaskAssignmentCreate.model_fields
    assert "model" not in ModelAwareAgentWorkBegin.model_fields
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        ModelAwareAgentTaskAssignmentCreate.model_validate(
            {
                **assignment.model_dump(mode="json"),
                "routing_snapshot": {"spoofed": True},
            }
        )
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        ModelAwareAgentWorkBegin.model_validate(
            {
                **begin.model_dump(mode="json"),
                "model": "caller-controlled",
            }
        )


@pytest.mark.contract
def test_lineage_snapshot_preserves_decision_and_review_floor_without_escalating() -> None:
    prior_snapshot = {
        "schema_version": "routing-decision-snapshot-v1",
        "policy_version": "model-aware-routing-v1",
        "selection_pending": False,
        "task_id": 7,
        "task_version": 3,
        "assessment_id": 5,
        "assessment_task_version": 3,
        "assessment_band": "advanced",
        "purpose": "execution",
        "actor_id": 11,
        "model_binding_id": 13,
        "model_binding_revision": 2,
        "model_catalog_id": 19,
        "model_catalog_key": "advanced-code",
        "model_catalog_revision": 4,
        "configured_model_alias": "runtime-advanced-code",
        "selected_reasoning_tier": 3,
        "selected_context_tier": "medium",
        "review_mode": "independent",
        "reviewer_profile_id": 23,
        "routing_preview_id": "preview-id",
        "routing_preview_digest": "b" * 64,
        "input_digest": "c" * 64,
        "selected_rank": 1,
        "adequacy_class": 0,
        "selection_reason_codes": ["eligible"],
        "confidence": 0.9,
        "trust_lineage": {
            "assessment_assessor_actor_id": 3,
            "preview_requested_by_actor_id": 3,
            "assignment_created_by_actor_id": 3,
            "evidence_kind": "declared-and-worker-reported",
            "attested": False,
        },
    }
    source = _assignment(assignment_id=1, snapshot=prior_snapshot)
    task = Task(id=7, title="Reroute", version=4)

    lineage = AgentWorkService._routing_lineage_snapshot(
        task=task,
        source_assignments=[source],
        transition="rework",
        provisional_actor_id=29,
        reason="Verification found a tool-driven correctness gap.",
        evidence={"failure_category": "tool_insufficiency"},
    )

    assert lineage["selection_pending"] is True
    assert lineage["source_assignment_ids"] == [source.id]
    assert lineage["prior_decisions"][0]["model_binding_id"] == 13
    assert lineage["prior_decisions"][0]["snapshot_sha256"] == hashlib.sha256(
        canonical_routing_json_bytes(prior_snapshot)
    ).hexdigest()
    assert lineage["review_floor"] == {
        "review_mode": "independent",
        "reviewer_profile_ids": [23],
        "independence_must_be_revalidated": True,
    }
    assert lineage["cause"]["category"] == "tool_insufficiency"
    assert lineage["model_tier_change"] == {
        "eligible": True,
        "applied": False,
        "reason": "fresh_selection_required",
    }
    assert AgentWorkService._selection_pending(
        _assignment(assignment_id=2, snapshot=lineage)
    )


@pytest.mark.contract
def test_lineage_failure_classification_is_conservative_and_bounded() -> None:
    task = Task(id=7, title="Recover", version=4)
    source = _assignment(assignment_id=1, snapshot={})
    lineage = AgentWorkService._routing_lineage_snapshot(
        task=task,
        source_assignments=[source],
        transition="recovery",
        provisional_actor_id=29,
        reason="reasoning insufficiency words alone are not governed evidence",
        evidence={"error": "reasoning insufficiency"},
    )

    assert lineage["cause"]["category"] == "non_model_or_unclassified"
    assert lineage["model_tier_change"] == {
        "eligible": False,
        "applied": False,
        "reason": "non_model_failure_no_escalation",
    }
    assert len(canonical_routing_json_bytes(lineage)) < 32_768


@pytest.mark.contract
def test_completed_rework_selection_retains_lineage_and_governs_escalation() -> None:
    prior_snapshot = {
        "schema_version": "routing-decision-snapshot-v1",
        "policy_version": "model-aware-routing-v1",
        "task_id": 7,
        "task_version": 3,
        "assessment_id": 5,
        "assessment_task_version": 3,
        "assessment_band": "standard",
        "purpose": "execution",
        "actor_id": 11,
        "model_binding_id": 13,
        "model_binding_revision": 2,
        "model_catalog_id": 19,
        "model_catalog_key": "standard-code",
        "model_catalog_revision": 4,
        "configured_model_alias": "runtime-standard-code",
        "selected_reasoning_tier": 1,
        "selected_context_tier": "small",
        "review_mode": "none",
        "routing_preview_id": "preview-id",
        "routing_preview_digest": "b" * 64,
        "input_digest": "c" * 64,
        "selected_rank": 1,
        "adequacy_class": 0,
        "selection_reason_codes": ["eligible"],
        "confidence": 0.9,
    }
    source = _assignment(assignment_id=1, snapshot=prior_snapshot)
    pending = AgentWorkService._routing_lineage_snapshot(
        task=Task(id=7, title="Reroute", version=4),
        source_assignments=[source],
        transition="rework",
        provisional_actor_id=29,
        reason="The selected model lacked the required tool capability.",
        evidence={"failure_category": "tool_insufficiency"},
    )
    pending_assignment = _assignment(assignment_id=2, snapshot=pending)

    completed = AgentRoutingService._completed_prior_lineage(
        pending_assignment,
        selected_reasoning_tier=2,
        selected_context_tier="medium",
    )

    assert completed is not None
    assert completed["cause"]["category"] == "tool_insufficiency"
    assert completed["prior_decisions"][0]["model_binding_id"] == 13
    assert completed["selection_result"] == {
        "completed_by_snapshot": True,
        "assignment_id": pending_assignment.id,
    }
    assert completed["model_tier_change"]["applied"] is True
    assert completed["model_tier_change"]["reason"] == (
        "governed_model_failure_escalation"
    )

    non_model_pending = AgentWorkService._routing_lineage_snapshot(
        task=Task(id=7, title="Recover", version=4),
        source_assignments=[source],
        transition="recovery",
        provisional_actor_id=29,
        reason="An external dependency was unavailable.",
        evidence={"failure_category": "external_service"},
    )
    with pytest.raises(
        AgentRoutingConflictError,
        match="non-model failure",
    ) as conflict:
        AgentRoutingService._completed_prior_lineage(
            _assignment(assignment_id=3, snapshot=non_model_pending),
            selected_reasoning_tier=2,
            selected_context_tier="medium",
        )
    assert conflict.value.code == "routing_model_escalation_not_allowed"


@pytest.mark.contract
@pytest.mark.parametrize(
    ("model", "trust_state"),
    [(None, "unreported"), ("legacy-model", "unverifiable")],
)
def test_run_response_keeps_legacy_model_evidence_explicit(
    model: str | None,
    trust_state: str,
) -> None:
    timestamp = datetime(2026, 7, 27, 12, tzinfo=UTC)
    run = AgentRun(
        id=1,
        actor_id=2,
        status="succeeded",
        model=model,
        model_trust_state=trust_state,
        model_match_basis=None,
        run_metadata=json.dumps({}),
        artifact_links=json.dumps([]),
        started_at=timestamp,
    )

    response = AgentWorkService.run_response(run)

    assert response.model == model
    assert response.model_trust_state == trust_state
    assert response.model_match_basis is None
