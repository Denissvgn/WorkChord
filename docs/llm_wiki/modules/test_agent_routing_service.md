# test_agent_routing_service Module

**Path:** `backend/tests/test_agent_routing_service.py`

## Description

End-to-end service coverage for authoritative Wave 3 routing.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.models.agent` | `AgentActor`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentRun`, `AgentTaskAssignment`, `TaskEvent` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `TeamMemberProfileSkill` |
| `app.schemas.agent` | `AgentTaskAssignmentCreate`, `AgentReviewVerdict`, `ModelAwareAgentTaskAssignmentCreate`, `ModelAwareAgentTaskAssignmentUpdate`, `ModelAwareAgentWorkBegin` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext` |
| `app.schemas.agent_routing` | `AgentRoutingPreviewCreate`, `TaskRoutingAssessmentCommand` |
| `app.services.agent_routing_policy` | `ROUTING_POLICY_VERSION` |
| `app.services.agent_routing_rollout` | `AgentRoutingRolloutService`, `AgentRoutingTopologyReadiness` |
| `app.services.agent_routing_service` | `AgentRoutingConflictError`, `AgentRoutingService` |
| `app.services.agent_work_service` | `AgentWorkService` |
| `asyncio` | `asyncio` |
| `datetime` | `UTC`, `date`, `datetime` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `tests.support.transactions` | `reload_session_fixture` |
| `types` | `SimpleNamespace` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_agent_routing_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/test_agent_routing_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (11) |
| Outbound | `backend` (10) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_assessment_command` | `(*, task_version: int, minimum_effort: str \| None = None) -> TaskRoutingAssessmentCommand` | — | — |
| `_command_context` | `(key: str) -> AgentPlanningCommandContext` | — | — |
| `_rollout` | `(mode: str) -> AgentRoutingRolloutService` | — | — |
| `_routing_fixture` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, task_factory)` | — | — |
| `test_assessment_lifecycle_is_replay_safe_and_version_bound` | *(async)* `(db_session: AsyncSession, actor_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `test_untrusted_legacy_lineage_cannot_raise_assessment_review_floor` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `test_selection_input_fence_serializes_sqlite_routing_transactions` | *(async)* `(db_session: AsyncSession, db_session_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `test_assessment_history_trims_deterministic_tail_to_packet_limit` | *(async)* `(db_session: AsyncSession, actor_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `test_preview_is_deterministic_and_relevant_mutation_invalidates_it` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `_extra_worker` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, *, key: str, cost_tier: str, local_first: bool, reasoning_tier: int = 1, effort: str = 'unknown', alias: str \| None = None, profile = None)` | — | — |
| `test_local_first_preference_breaks_ties_but_never_overrides_a_gate` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `test_required_effort_gates_and_orders_entries_of_one_runtime_model` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `test_verification_independence_requires_authoritative_profile_history` | *(async)* `(snapshot_authority: str \| None, run_receipt: str \| None, expected_blocker: str \| None, db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, task_factory) -> None` | `@pytest.mark.asyncio`, `@pytest.mark.parametrize(('snapshot_authority', 'run_receipt', 'expected_blocker'), (('agent-routing-service-v1', None, 'verification_profile_not_independent'), (None, None, 'verification_independence_unverifiable'), (None, 'historical', 'verification_profile_not_independent'), (None, 'current', None), (None, 'changed_to_historical', 'verification_profile_not_independent'), (None, 'foreign_actor', 'verification_independence_unverifiable'), (None, 'missing_revision', 'verification_independence_unverifiable'), (None, 'server_ended_unrecorded', 'verification_independence_unverifiable'), (None, 'server_ended_recorded', None)))` | — |
| `test_model_aware_assignment_and_begin_enforce_observed_model` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `test_completed_rework_update_persists_prior_and_new_routing_lineage` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, team_member_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
| `test_rejection_telemetry_normalizes_adversarial_legacy_lineage` | *(async)* `(db_session: AsyncSession, profile_factory, actor_factory, task_factory) -> None` | `@pytest.mark.asyncio` | — |
