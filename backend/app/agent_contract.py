"""Shared capability handshake contract for REST and MCP projections."""

from __future__ import annotations


MODEL_AWARE_ROUTING_FEATURE = "model-aware-routing-v1"
SKILL_BUNDLES_FEATURE = "skill-bundles-v1"
AGENT_TEAM_MASTER_FEATURE = "agent-team-master-v1"

# Add a feature only after every REST/MCP read, mutation, validation, and
# compatibility boundary behind it is live. In particular, the Wave 1 routing
# persistence models do not by themselves activate model-aware routing.
AGENT_CONTRACT_FEATURES: tuple[str, ...] = (
    "agent-capabilities-v1",
    "actor-roster-v1",
    AGENT_TEAM_MASTER_FEATURE,
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


def agent_contract_features(
    *,
    include_skill_bundles: bool,
    model_aware_routing_mode: str = "off",
) -> list[str]:
    """Return one ordered feature projection shared by REST and MCP."""

    if model_aware_routing_mode not in {"off", "shadow", "enforced"}:
        raise ValueError("Unsupported model-aware routing mode")

    features = [
        feature
        for feature in AGENT_CONTRACT_FEATURES
        if include_skill_bundles or feature != SKILL_BUNDLES_FEATURE
    ]
    if model_aware_routing_mode != "off":
        features.insert(
            features.index("actor-roster-v1") + 1,
            MODEL_AWARE_ROUTING_FEATURE,
        )
    return features
