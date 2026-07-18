"""Shared capability handshake contract for REST and MCP projections."""

from __future__ import annotations


MODEL_AWARE_ROUTING_FEATURE = "model-aware-routing-v1"
SKILL_BUNDLES_FEATURE = "skill-bundles-v1"

# Add a feature only after every REST/MCP read, mutation, validation, and
# compatibility boundary behind it is live. In particular, the Wave 1 routing
# persistence models do not by themselves activate model-aware routing.
AGENT_CONTRACT_FEATURES: tuple[str, ...] = (
    "agent-capabilities-v1",
    "actor-roster-v1",
    "actor-task-assignments",
    "my-work-v1",
    "snapshot-pagination-v1",
    "work-etag-v1",
    "complete-task-context",
    "atomic-begin-submit",
    "atomic-renew-v1",
    "fenced-claims",
    "typed-rework-recovery",
    "agent-discovery-triage-v1",
    "pm-control-v1",
    "verification-v1",
    SKILL_BUNDLES_FEATURE,
)


def agent_contract_features(*, include_skill_bundles: bool) -> list[str]:
    """Return one ordered feature projection shared by REST and MCP."""

    return [
        feature
        for feature in AGENT_CONTRACT_FEATURES
        if include_skill_bundles or feature != SKILL_BUNDLES_FEATURE
    ]
