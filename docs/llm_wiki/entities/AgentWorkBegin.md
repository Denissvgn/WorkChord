# AgentWorkBegin

**Location:** `backend/app/schemas/agent.py:982`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Atomically accept and start a server-selected work assignment.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_metadata_size` | field | metadata | after | — |
| `validate_branch_url` | field | branch_url | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `assignment_id` | `int` | `assignment_id` | Yes | No | — | — | — | — |
| `queue_revision` | `int` | `queue_revision` | Yes | No | — | ge=1 | — | — |
| `lease_seconds` | `int` | `lease_seconds` | No | No | `3600` | ge=60; le=86400 | — | — |
| `trace_id` | `Optional[str]` | `trace_id` | No | Yes | `None` | max_length=255 | — | — |
| `model` | `Optional[str]` | `model` | No | Yes | `None` | max_length=255 | — | — |
| `tool_name` | `Optional[str]` | `tool_name` | No | Yes | `None` | max_length=255 | — | — |
| `metadata` | `dict[str, Any]` | `metadata` | No | No | factory: `dict` | max_length=unknown (MAX_AGENT_JSON_FIELDS) | — | — |
| `branch_url` | `Optional[str]` | `branch_url` | No | Yes | `None` | max_length=1000 | — | GitHub branch URL of the work; WorkChord links it to the task. |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_metadata_size` | `(value: dict[str, Any]) -> dict[str, Any]` | `@field_validator('metadata')`, `@classmethod` | — |
| `validate_branch_url` | `(value: Optional[str]) -> Optional[str]` | `@field_validator('branch_url')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentWorkBegin (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["begin_my_agent_work (backend/app/routers/agent.py)"]
    n4["renew_my_agent_work (backend/app/routers/agent.py)"]
    n5["AgentWorkService._live_fence_receipt (backend/app/services/agent_work_service.py)"]
    n6["AgentWorkService._replay_live_fence_receipt (backend/app/services/agent_work_service.py)"]
    n7["AgentWorkService.begin (backend/app/services/agent_work_service.py)"]
    n8["AgentWorkService.renew_work (backend/app/services/agent_work_service.py)"]
    n9["backend/tests/support/runtime_peer.py"]
    n10["backend/tests/test_agent_model_catalog_api.py"]
    n11["begins (backend/tests/test_harness_session_metadata.py)"]
    n12["test_supervised_execution_and_exact_independent_review (backend/tests/test_review_provenance.py)"]
    n13["test_unassigned_run_remains_unknown_and_optional_supervisor_needs_no_profile (backend/tests/test_review_provenance.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/routers_agent.md"
    click n5 "../modules/agent_work_service.md"
    click n6 "../modules/agent_work_service.md"
    click n7 "../modules/agent_work_service.md"
    click n8 "../modules/agent_work_service.md"
    click n9 "../modules/runtime_peer.md"
    click n10 "../modules/test_agent_model_catalog_api.md"
    click n11 "../modules/test_harness_session_metadata.md"
    click n12 "../modules/test_review_provenance.md"
    click n13 "../modules/test_review_provenance.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 2 | `assignment_id`, `branch_url`, `lease_seconds`, `metadata`, `model`, `queue_revision`, `tool_name`, `trace_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `begin_my_agent_work` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `renew_my_agent_work` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService._live_fence_receipt` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService._replay_live_fence_receipt` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService.begin` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService.renew_work` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `runtime_peer` | import | [runtime_peer](../modules/runtime_peer.md) | — |
| `test_agent_model_catalog_api` | import | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | — |
| `begins` | call | [test_harness_session_metadata](../modules/test_harness_session_metadata.md) | 1 |
| `test_supervised_execution_and_exact_independent_review` | call | [test_review_provenance](../modules/test_review_provenance.md) | 1 |
| `test_unassigned_run_remains_unknown_and_optional_supervisor_needs_no_profile` | call | [test_review_provenance](../modules/test_review_provenance.md) | 1 |

> References: showing 12 of 14 logical references; 2 omitted by the 12-row generated summary limit.
