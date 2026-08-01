"""Bounded operational evidence for model-aware routing.

Routing telemetry deliberately uses a closed event vocabulary and closed payload
fields.  Task prose, prompts, provider configuration, credentials, raw model
identifiers, and arbitrary evidence never cross this boundary.
"""

from __future__ import annotations

from enum import StrEnum
import hashlib
import json
from typing import Any, Mapping, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.runtime_telemetry import metrics
from app.services.agent_routing_policy import (
    MAX_ROUTING_EXCLUSIONS,
    MODEL_FAILURE_CATEGORIES,
    NON_MODEL_FAILURE_CATEGORY,
    ROUTING_POLICY_VERSION,
    canonical_routing_json_bytes,
)
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.task_service import TaskService


MAX_ROUTING_OPERATIONAL_EVENT_BYTES = 8_192
MAX_ROUTING_OPERATIONAL_CODES = 32
MAX_ROUTING_OPERATIONAL_CODE_LENGTH = 64
MAX_ROUTING_OPERATIONAL_SCALAR_LENGTH = 255
MAX_ROUTING_OPERATIONAL_EXCLUSIONS = min(MAX_ROUTING_EXCLUSIONS, 12)
MAX_ROUTING_OPERATIONAL_EXCLUSION_CODES = 4


class RoutingOperationalEvent(StrEnum):
    """Closed, low-cardinality routing outcome vocabulary."""

    ASSESSMENT_CREATED = "assessment_created"
    PREVIEW_RECORDED = "preview_recorded"
    NO_ELIGIBLE_CANDIDATE = "no_eligible_candidate"
    ASSIGNMENT_SELECTED = "assignment_selected"
    STALE_CONFLICT = "stale_conflict"
    CONFIGURED_OBSERVED_MISMATCH = "configured_observed_mismatch"
    VERIFIER_REJECTED = "verifier_rejected"
    REWORK_CREATED = "rework_created"
    TIER_ESCALATED = "tier_escalated"


_COMMON_FIELDS = frozenset(
    {
        "task_version",
        "policy_version",
        "rollout_mode",
        "assessment_id",
        "assessment_task_version",
        "assignment_id",
        "source_assignment_id",
        "rework_assignment_id",
        "run_id",
        "actor_id",
        "model_binding_id",
        "model_binding_revision",
        "model_catalog_id",
        "model_catalog_revision",
        "routing_preview_id",
        "routing_preview_digest",
        "input_digest",
        "lineage_digest",
        "band",
        "review_mode",
        "purpose",
        "conflict_code",
        "failure_category",
        "model_evidence_source",
        "model_attested",
        "previous_reasoning_tier",
        "selected_reasoning_tier",
        "previous_context_tier",
        "selected_context_tier",
        "recommended_actor_id",
        "recommended_model_binding_id",
        "recommended_model_binding_revision",
        "recommended_model_catalog_id",
        "recommended_model_catalog_revision",
        "reason_codes",
        "hard_blocker_codes",
        "excluded_candidates",
        "excluded_candidate_count",
        "excluded_candidate_projection_truncated",
    }
)

_EVENT_FIELDS: Mapping[RoutingOperationalEvent, frozenset[str]] = {
    RoutingOperationalEvent.ASSESSMENT_CREATED: frozenset(
        {
            "task_version",
            "policy_version",
            "assessment_id",
            "assessment_task_version",
            "band",
            "review_mode",
            "reason_codes",
        }
    ),
    RoutingOperationalEvent.PREVIEW_RECORDED: frozenset(
        {
            "task_version",
            "policy_version",
            "rollout_mode",
            "assessment_id",
            "assessment_task_version",
            "purpose",
            "routing_preview_id",
            "routing_preview_digest",
            "input_digest",
            "recommended_actor_id",
            "recommended_model_binding_id",
            "recommended_model_binding_revision",
            "recommended_model_catalog_id",
            "recommended_model_catalog_revision",
            "hard_blocker_codes",
            "excluded_candidates",
            "excluded_candidate_count",
            "excluded_candidate_projection_truncated",
        }
    ),
    RoutingOperationalEvent.NO_ELIGIBLE_CANDIDATE: frozenset(
        {
            "task_version",
            "policy_version",
            "rollout_mode",
            "assessment_id",
            "assessment_task_version",
            "purpose",
            "routing_preview_id",
            "routing_preview_digest",
            "input_digest",
            "hard_blocker_codes",
            "excluded_candidates",
            "excluded_candidate_count",
            "excluded_candidate_projection_truncated",
        }
    ),
    RoutingOperationalEvent.ASSIGNMENT_SELECTED: frozenset(
        {
            "task_version",
            "policy_version",
            "rollout_mode",
            "assessment_id",
            "assessment_task_version",
            "assignment_id",
            "actor_id",
            "model_binding_id",
            "model_binding_revision",
            "model_catalog_id",
            "model_catalog_revision",
            "routing_preview_id",
            "routing_preview_digest",
            "reason_codes",
            "purpose",
            "review_mode",
        }
    ),
    RoutingOperationalEvent.STALE_CONFLICT: frozenset(
        {
            "task_version",
            "policy_version",
            "rollout_mode",
            "assessment_id",
            "assignment_id",
            "actor_id",
            "model_binding_id",
            "model_binding_revision",
            "routing_preview_id",
            "conflict_code",
            "reason_codes",
        }
    ),
    RoutingOperationalEvent.CONFIGURED_OBSERVED_MISMATCH: frozenset(
        {
            "task_version",
            "policy_version",
            "rollout_mode",
            "assignment_id",
            "actor_id",
            "model_binding_id",
            "model_binding_revision",
            "model_catalog_id",
            "model_catalog_revision",
            "conflict_code",
            "model_evidence_source",
            "model_attested",
            "reason_codes",
        }
    ),
    RoutingOperationalEvent.VERIFIER_REJECTED: frozenset(
        {
            "task_version",
            "policy_version",
            "assignment_id",
            "actor_id",
            "review_mode",
            "failure_category",
            "lineage_digest",
            "reason_codes",
        }
    ),
    RoutingOperationalEvent.REWORK_CREATED: frozenset(
        {
            "task_version",
            "policy_version",
            "source_assignment_id",
            "rework_assignment_id",
            "actor_id",
            "failure_category",
            "lineage_digest",
            "reason_codes",
        }
    ),
    RoutingOperationalEvent.TIER_ESCALATED: frozenset(
        {
            "task_version",
            "policy_version",
            "assignment_id",
            "actor_id",
            "model_binding_id",
            "model_binding_revision",
            "model_catalog_id",
            "model_catalog_revision",
            "failure_category",
            "previous_reasoning_tier",
            "selected_reasoning_tier",
            "previous_context_tier",
            "selected_context_tier",
            "reason_codes",
        }
    ),
}
_EVENT_REQUIRED_FIELDS: Mapping[RoutingOperationalEvent, frozenset[str]] = {
    RoutingOperationalEvent.ASSESSMENT_CREATED: frozenset(
        {
            "task_version",
            "assessment_id",
            "assessment_task_version",
            "band",
            "review_mode",
        }
    ),
    RoutingOperationalEvent.PREVIEW_RECORDED: frozenset(
        {
            "task_version",
            "rollout_mode",
            "assessment_id",
            "assessment_task_version",
            "routing_preview_id",
            "routing_preview_digest",
            "input_digest",
        }
    ),
    RoutingOperationalEvent.NO_ELIGIBLE_CANDIDATE: frozenset(
        {
            "task_version",
            "rollout_mode",
            "assessment_id",
            "assessment_task_version",
            "routing_preview_id",
            "routing_preview_digest",
            "input_digest",
            "hard_blocker_codes",
        }
    ),
    RoutingOperationalEvent.ASSIGNMENT_SELECTED: frozenset(
        {
            "task_version",
            "assessment_id",
            "assessment_task_version",
            "assignment_id",
            "actor_id",
            "model_binding_id",
            "model_binding_revision",
            "model_catalog_id",
            "model_catalog_revision",
            "routing_preview_id",
            "routing_preview_digest",
            "purpose",
            "review_mode",
        }
    ),
    RoutingOperationalEvent.STALE_CONFLICT: frozenset(
        {"task_version", "conflict_code", "reason_codes"}
    ),
    RoutingOperationalEvent.CONFIGURED_OBSERVED_MISMATCH: frozenset(
        {
            "task_version",
            "assignment_id",
            "actor_id",
            "model_binding_id",
            "model_binding_revision",
            "model_catalog_id",
            "model_catalog_revision",
            "conflict_code",
            "model_evidence_source",
            "model_attested",
        }
    ),
    RoutingOperationalEvent.VERIFIER_REJECTED: frozenset(
        {
            "task_version",
            "assignment_id",
            "actor_id",
            "failure_category",
            "lineage_digest",
        }
    ),
    RoutingOperationalEvent.REWORK_CREATED: frozenset(
        {
            "task_version",
            "source_assignment_id",
            "rework_assignment_id",
            "actor_id",
            "failure_category",
            "lineage_digest",
        }
    ),
    RoutingOperationalEvent.TIER_ESCALATED: frozenset(
        {
            "task_version",
            "assignment_id",
            "actor_id",
            "model_binding_id",
            "model_binding_revision",
            "model_catalog_id",
            "model_catalog_revision",
            "failure_category",
            "previous_reasoning_tier",
            "selected_reasoning_tier",
            "previous_context_tier",
            "selected_context_tier",
        }
    ),
}

_INTEGER_FIELDS = frozenset(
    {
        field
        for field in _COMMON_FIELDS
        if (field.endswith("_id") and field != "routing_preview_id")
        or field.endswith("_revision")
        or field.endswith("_task_version")
        or field == "task_version"
        or field
        in {
            "excluded_candidate_count",
            "previous_reasoning_tier",
            "selected_reasoning_tier",
        }
    }
)
_BOOLEAN_FIELDS = frozenset(
    {"excluded_candidate_projection_truncated", "model_attested"}
)
_DIGEST_FIELDS = frozenset(
    {"routing_preview_digest", "input_digest", "lineage_digest"}
)
_CODE_LIST_FIELDS = frozenset({"reason_codes", "hard_blocker_codes"})
_CLOSED_SCALAR_VALUES: Mapping[str, frozenset[str]] = {
    "policy_version": frozenset({ROUTING_POLICY_VERSION}),
    "rollout_mode": frozenset({"off", "shadow", "enforced"}),
    "purpose": frozenset({"execution", "verification"}),
    "review_mode": frozenset(
        {"none", "standard", "independent", "specialist-independent"}
    ),
    "band": frozenset({"routine", "standard", "advanced"}),
    "previous_context_tier": frozenset({"small", "medium", "large"}),
    "selected_context_tier": frozenset({"small", "medium", "large"}),
    "model_evidence_source": frozenset(
        {"worker_report", "trusted_launcher", "unreported"}
    ),
    "failure_category": frozenset(
        {*MODEL_FAILURE_CATEGORIES, NON_MODEL_FAILURE_CATEGORY}
    ),
}
_EXCLUSION_FIELDS = frozenset(
    {"actor_id", "model_binding_id", "hard_blocker_codes"}
)


def opaque_value_digest(value: str | None) -> str | None:
    """Hash an opaque runtime identity when correlation is operationally useful."""

    if value is None:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _bounded_code(value: Any, *, field: str) -> str:
    code = str(value).strip()
    if not code or len(code) > MAX_ROUTING_OPERATIONAL_CODE_LENGTH:
        raise ValueError(
            f"{field} entries must be 1-{MAX_ROUTING_OPERATIONAL_CODE_LENGTH} characters"
        )
    if any(ord(character) < 32 or ord(character) == 127 for character in code):
        raise ValueError(f"{field} entries must not contain control characters")
    return code


def _bounded_scalar(value: Any, *, field: str) -> str:
    scalar = str(value).strip()
    if not scalar or len(scalar) > MAX_ROUTING_OPERATIONAL_SCALAR_LENGTH:
        raise ValueError(
            f"{field} must be 1-{MAX_ROUTING_OPERATIONAL_SCALAR_LENGTH} characters"
        )
    if any(
        ord(character) < 32 or ord(character) == 127 for character in scalar
    ):
        raise ValueError(f"{field} must not contain control characters")
    return scalar


def _code_list(
    value: Any,
    *,
    field: str,
    max_items: int = MAX_ROUTING_OPERATIONAL_CODES,
) -> list[str]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{field} must be a list")
    if len(value) > max_items:
        raise ValueError(
            f"{field} exceeds the {max_items}-entry limit"
        )
    return sorted({_bounded_code(item, field=field) for item in value})


def _excluded_candidates(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, (list, tuple)):
        raise ValueError("excluded_candidates must be a list")
    if len(value) > MAX_ROUTING_OPERATIONAL_EXCLUSIONS:
        raise ValueError(
            "excluded_candidates exceeds the "
            f"{MAX_ROUTING_OPERATIONAL_EXCLUSIONS}-entry limit"
        )
    normalized: list[dict[str, Any]] = []
    for raw in value:
        if not isinstance(raw, Mapping):
            raise ValueError("excluded_candidates entries must be objects")
        unknown = set(raw) - _EXCLUSION_FIELDS
        if unknown:
            raise ValueError(
                "excluded_candidates contains unsupported fields: "
                + ", ".join(sorted(unknown))
            )
        actor_id = raw.get("actor_id")
        binding_id = raw.get("model_binding_id")
        if not isinstance(actor_id, int) or actor_id <= 0:
            raise ValueError("excluded candidate actor_id must be positive")
        if binding_id is not None and (
            not isinstance(binding_id, int) or binding_id <= 0
        ):
            raise ValueError(
                "excluded candidate model_binding_id must be positive or null"
            )
        normalized.append(
            {
                "actor_id": actor_id,
                "model_binding_id": binding_id,
                "hard_blocker_codes": _code_list(
                    raw.get("hard_blocker_codes", []),
                    field="hard_blocker_codes",
                    max_items=MAX_ROUTING_OPERATIONAL_EXCLUSION_CODES,
                ),
            }
        )
    return sorted(
        normalized,
        key=lambda item: (
            item["actor_id"],
            item["model_binding_id"] or 0,
        ),
    )


def build_routing_operational_payload(
    event: RoutingOperationalEvent | str,
    values: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one secret-free operational projection and enforce its byte cap."""

    event = RoutingOperationalEvent(event)
    allowed = _EVENT_FIELDS[event]
    unknown = set(values) - allowed
    if unknown:
        raise ValueError(
            f"{event.value} contains unsupported fields: "
            + ", ".join(sorted(unknown))
        )
    missing = {
        field
        for field in _EVENT_REQUIRED_FIELDS[event]
        if field not in values or values[field] is None
    }
    if missing:
        raise ValueError(
            f"{event.value} is missing required fields: "
            + ", ".join(sorted(missing))
        )

    payload: dict[str, Any] = {
        "schema_version": "agent-routing-operational-event-v1",
        "event": event.value,
        "policy_version": ROUTING_POLICY_VERSION,
    }
    for field in sorted(allowed):
        if field not in values or values[field] is None:
            continue
        value = values[field]
        if field in _INTEGER_FIELDS:
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"{field} must be a positive integer")
            payload[field] = value
        elif field in _BOOLEAN_FIELDS:
            if not isinstance(value, bool):
                raise ValueError(f"{field} must be a boolean")
            payload[field] = value
        elif field in _DIGEST_FIELDS:
            digest = str(value).strip().lower()
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError(f"{field} must be a SHA-256 digest")
            payload[field] = digest
        elif field in _CODE_LIST_FIELDS:
            payload[field] = _code_list(value, field=field)
        elif field == "excluded_candidates":
            payload[field] = _excluded_candidates(value)
        else:
            scalar = _bounded_scalar(value, field=field)
            permitted = _CLOSED_SCALAR_VALUES.get(field)
            if permitted is not None and scalar not in permitted:
                raise ValueError(
                    f"{field} must be one of: {', '.join(sorted(permitted))}"
                )
            payload[field] = scalar

    encoded = canonical_routing_json_bytes(payload)
    if len(encoded) > MAX_ROUTING_OPERATIONAL_EVENT_BYTES:
        raise ValueError(
            "Routing operational event exceeds the "
            f"{MAX_ROUTING_OPERATIONAL_EVENT_BYTES}-byte limit"
        )
    # Return a detached JSON-native value so mutable caller collections cannot
    # alter the already-validated projection.
    return json.loads(encoded)


async def record_routing_operational_event(
    db: AsyncSession,
    *,
    event: RoutingOperationalEvent | str,
    task_id: int,
    values: Mapping[str, Any],
    actor_id: int | None = None,
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    commit: bool = False,
) -> int:
    """Stage a task audit event, durable webhook intent, and aggregate metric."""

    event = RoutingOperationalEvent(event)
    payload = build_routing_operational_payload(event, values)
    task_event = await TaskService(db).record_task_event(
        task_id,
        f"agent.routing.{event.value}",
        payload,
        actor_type="agent" if actor_id is not None else "system",
        actor_id=actor_id,
        correlation_id=correlation_id,
        idempotency_key=idempotency_key,
    )
    await emit_outbound_webhook_event(
        db,
        event_type=f"agent.routing.{event.value}",
        entity_type="task",
        entity_id=task_id,
        data=payload,
        commit=False,
    )
    metrics.increment(
        "workchord_agent_routing_events_total",
        labels={"event": event.value},
    )
    if commit:
        await db.commit()
    return task_event.id


def routing_exclusion_projection(
    exclusions: Sequence[Any],
) -> dict[str, Any]:
    """Project exclusions without allowing telemetry to fail a valid preview."""

    projected: list[dict[str, Any]] = []
    truncated = len(exclusions) > MAX_ROUTING_OPERATIONAL_EXCLUSIONS
    for exclusion in exclusions[:MAX_ROUTING_OPERATIONAL_EXCLUSIONS]:
        blocker_codes = sorted(set(exclusion.hard_blocker_codes))
        if len(blocker_codes) > MAX_ROUTING_OPERATIONAL_EXCLUSION_CODES:
            truncated = True
        projected.append(
            {
                "actor_id": int(exclusion.actor_id),
                "model_binding_id": (
                    int(exclusion.model_binding_id)
                    if exclusion.model_binding_id is not None
                    else None
                ),
                "hard_blocker_codes": blocker_codes[
                    :MAX_ROUTING_OPERATIONAL_EXCLUSION_CODES
                ],
            }
        )
    result: dict[str, Any] = {
        "excluded_candidates": projected,
        "excluded_candidate_projection_truncated": truncated,
    }
    if exclusions:
        result["excluded_candidate_count"] = len(exclusions)
    return result
