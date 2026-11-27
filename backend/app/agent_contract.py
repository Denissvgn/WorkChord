"""Shared capability handshake contract for REST and MCP projections."""

from __future__ import annotations


MODEL_AWARE_ROUTING_FEATURE = "model-aware-routing-v1"
REVIEW_PROVENANCE_FEATURE = "review-provenance-v1"
SCOPED_REVIEW_EVIDENCE_FEATURE = "scoped-review-evidence-v1"
EXECUTION_PLANNING_WINDOW_FEATURE = "iteration-window-execution-recovery-v1"
ANNUAL_CALENDAR_FEATURE = "annual-calendar-coverage-v1"
SKILL_BUNDLES_FEATURE = "skill-bundles-v1"
AGENT_TEAM_MASTER_FEATURE = "agent-team-master-v1"
WORK_DELIVERY_LINKS_FEATURE = "work-delivery-links-v1"
GITHUB_RECONCILIATION_FEATURE = "github-reconciliation-v1"
DELIVERY_PREREQUISITE_BRANCHES_FEATURE = "delivery-prerequisite-branches-v1"
RUNTIME_INSTANCE_IDENTITY_FEATURE = "runtime-instance-identity-v1"
TASK_POSTPONEMENT_FEATURE = "agent-task-postponement-v1"

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
    "canonical-task-brief-v1",
    "execution-usage-v1",
    "atomic-begin-submit",
    "atomic-renew-v1",
    "fenced-claims",
    "typed-rework-recovery",
    EXECUTION_PLANNING_WINDOW_FEATURE,
    ANNUAL_CALENDAR_FEATURE,
    "agent-discovery-triage-v1",
    "pm-control-v1",
    "verification-v1",
    REVIEW_PROVENANCE_FEATURE,
    SCOPED_REVIEW_EVIDENCE_FEATURE,
    # Work starts once its dependencies are done; calculated dates then follow
    # the actual start and submit, and a change of dates keeps queued dispatch valid.
    "schedule-follows-actuals-v1",
    # Begin takes branch_url and submit takes branch_url and commit_urls; WorkChord
    # links the branch, commits, and pull request to the task as GitHub links.
    WORK_DELIVERY_LINKS_FEATURE,
    # agent_get_github_reconciliation reads a task's pull requests as last observed;
    # agent_run_github_catch_up reads them from GitHub with the REST catch-up's authority.
    GITHUB_RECONCILIATION_FEATURE,
    # agent_list_delivery_dependencies, agent_add_delivery_dependency and
    # agent_retarget_delivery_dependency record or change a prerequisite's target branch.
    DELIVERY_PREREQUISITE_BRANCHES_FEATURE,
    # The onboarding handoff carries runtime_instance_id and the acknowledgement returns it;
    # team status shows the acknowledging identity. A runtime that lists this feature must send it.
    RUNTIME_INSTANCE_IDENTITY_FEATURE,
    # agent_postpone_task and agent_reactivate_task stop and resume work with the REST
    # commands' authority (the project's PM agent only); agent_get_task_postponement
    # reads the reason and each requirement's state. The owner decision is not an agent tool.
    TASK_POSTPONEMENT_FEATURE,
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
