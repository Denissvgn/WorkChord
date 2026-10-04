# test_agent_work_routing_lineage Module

**Path:** `backend/tests/test_agent_work_routing_lineage.py`

## Description

Focused assignment/run evidence tests that do not require a database.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.agent` | `AgentRun`, `AgentTaskAssignment` |
| `app.models.task` | `Task` |
| `app.schemas.agent` | `AgentTaskContextResponse`, `ModelAwareAgentTaskAssignmentCreate`, `ModelAwareAgentWorkBegin` |
| `app.schemas.task` | `TaskResponse` |
| `app.schemas.task_brief` | `BriefCriterion`, `TaskBrief` |
| `app.services.agent_routing_policy` | `canonical_routing_json_bytes` |
| `app.services.agent_routing_service` | `AgentRoutingConflictError`, `AgentRoutingService` |
| `app.services.agent_work_service` | `AgentWorkService` |
| `datetime` | `UTC`, `datetime` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/agent.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/schemas/agent.py"]
    n3["backend/app/schemas/task.py"]
    n4["backend/app/schemas/task_brief.py"]
    n5["backend/app/services/agent_routing_policy.py"]
    n6["backend/app/services/agent_routing_service.py"]
    n7["backend/app/services/agent_work_service.py"]
    n8["backend/tests/test_agent_work_routing_lineage.py"]
    n0 --> n1
    n1 --> n0
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n3 --> n4
    n6 --> n0
    n6 --> n1
    n6 --> n5
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n5
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n6
    n8 --> n7
    click n0 "../modules/models_agent.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/schemas_agent.md"
    click n3 "../modules/schemas_task.md"
    click n4 "../modules/schemas_task_brief.md"
    click n5 "../modules/agent_routing_policy.md"
    click n6 "../modules/agent_routing_service.md"
    click n7 "../modules/agent_work_service.md"
    click n8 "../modules/test_agent_work_routing_lineage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [schemas_agent](../modules/schemas_agent.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [schemas_task_brief](../modules/schemas_task_brief.md) |
| Outbound | [agent_routing_policy](../modules/agent_routing_policy.md) |
| Outbound | [agent_routing_service](../modules/agent_routing_service.md) |
| Outbound | [agent_work_service](../modules/agent_work_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_worker_context_identifies_authoritative_brief` | `(canonical: bool) -> None` | `@pytest.mark.contract`, `@pytest.mark.parametrize('canonical', [True, False])` | — |
| `_assignment` | `(*, assignment_id: int, snapshot: dict[str, object], reviewer_profile_id: int \| None = None) -> AgentTaskAssignment` | — | — |
| `test_model_aware_commands_own_selection_and_observed_model_fields` | `() -> None` | `@pytest.mark.contract` | — |
| `test_lineage_snapshot_preserves_decision_and_review_floor_without_escalating` | `() -> None` | `@pytest.mark.contract` | — |
| `test_lineage_failure_classification_is_conservative_and_bounded` | `() -> None` | `@pytest.mark.contract` | — |
| `test_completed_rework_selection_retains_lineage_and_governs_escalation` | `() -> None` | `@pytest.mark.contract` | — |
| `test_run_response_keeps_legacy_model_evidence_explicit` | `(model: str \| None, trust_state: str) -> None` | `@pytest.mark.contract`, `@pytest.mark.parametrize(('model', 'trust_state'), [(None, 'unreported'), ('legacy-model', 'unverifiable')])` | — |
