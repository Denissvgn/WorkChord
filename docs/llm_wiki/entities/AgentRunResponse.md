# AgentRunResponse

**Location:** `backend/app/schemas/agent.py:404`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Agent run response.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `task_id` | `Optional[int]` | `task_id` | Yes | Yes | — | — | — | — |
| `actor_id` | `int` | `actor_id` | Yes | No | — | — | — | — |
| `assignment_id` | `Optional[int]` | `assignment_id` | No | Yes | `None` | — | — | — |
| `claim_generation` | `Optional[int]` | `claim_generation` | No | Yes | `None` | — | — | — |
| `status` | `str` | `status` | Yes | No | — | — | — | — |
| `trace_id` | `Optional[str]` | `trace_id` | No | Yes | `None` | — | — | — |
| `model_binding_id` | `Optional[int]` | `model_binding_id` | No | Yes | `None` | — | — | — |
| `model_binding_revision` | `Optional[int]` | `model_binding_revision` | No | Yes | `None` | — | — | — |
| `configured_model_alias` | `Optional[str]` | `configured_model_alias` | No | Yes | `None` | — | — | — |
| `resolved_model_id` | `Optional[str]` | `resolved_model_id` | No | Yes | `None` | — | — | — |
| `model_trust_state` | `Literal['matched', 'mismatch', 'unreported', 'unverifiable']` | `model_trust_state` | No | No | `'unreported'` | — | — | Configured-versus-reported comparison only; matched worker self-report is not launcher attestation. |
| `model_match_basis` | `Optional[Literal['configured_alias', 'catalog_key']]` | `model_match_basis` | No | Yes | `None` | — | — | — |
| `model` | `Optional[str]` | `model` | No | Yes | `None` | — | — | — |
| `tool_name` | `Optional[str]` | `tool_name` | No | Yes | `None` | — | — | — |
| `metadata` | `dict[str, Any]` | `metadata` | Yes | No | — | — | — | — |
| `artifact_links` | `list[str]` | `artifact_links` | Yes | No | — | — | — | — |
| `commit_url` | `Optional[str]` | `commit_url` | No | Yes | `None` | — | — | — |
| `pr_url` | `Optional[str]` | `pr_url` | No | Yes | `None` | — | — | — |
| `summary` | `Optional[str]` | `summary` | No | Yes | `None` | — | — | — |
| `error` | `Optional[str]` | `error` | No | Yes | `None` | — | — | — |
| `started_at` | `datetime` | `started_at` | Yes | No | — | — | — | — |
| `ended_at` | `Optional[datetime]` | `ended_at` | No | Yes | `None` | — | — | — |
| `heartbeat_at` | `Optional[datetime]` | `heartbeat_at` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRunResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["AgentRunDetailResponse (backend/app/schemas/agent.py)"]
    n3["_run_response (backend/app/routers/agent.py)"]
    n4["finish_agent_run (backend/app/routers/agent.py)"]
    n5["list_my_agent_runs (backend/app/routers/agent.py)"]
    n6["start_agent_run (backend/app/routers/agent.py)"]
    n7["AgentWorkService.list_my_runs (backend/app/services/agent_work_service.py)"]
    n8["AgentWorkService.run_response (backend/app/services/agent_work_service.py)"]
    n9["test_legacy_assignment_and_run_responses_remain_readable (backend/tests/test_agent_routing_data.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/schemas_agent.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/routers_agent.md"
    click n5 "../modules/routers_agent.md"
    click n6 "../modules/routers_agent.md"
    click n7 "../modules/agent_work_service.md"
    click n8 "../modules/agent_work_service.md"
    click n9 "../modules/test_agent_routing_data.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `actor_id`, `artifact_links`, `assignment_id`, `claim_generation`, `commit_url`, `configured_model_alias`, `ended_at`, `error`, `heartbeat_at`, `id`, `metadata`, `model` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `AgentRunDetailResponse` | [schemas_agent](../modules/schemas_agent.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_run_response` | call | [routers_agent](../modules/routers_agent.md) | 1 |
| `_run_response` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `finish_agent_run` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `list_my_agent_runs` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `start_agent_run` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.list_my_runs` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService.run_response` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.run_response` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `test_legacy_assignment_and_run_responses_remain_readable` | call | [test_agent_routing_data](../modules/test_agent_routing_data.md) | 1 |
