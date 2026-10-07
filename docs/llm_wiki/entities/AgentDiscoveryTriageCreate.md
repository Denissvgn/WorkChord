# AgentDiscoveryTriageCreate

**Location:** `backend/app/schemas/agent.py:1113`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Claim-bound report of work discovered outside the assigned scope.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_evidence_size` | field | evidence | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `assignment_id` | `int` | `assignment_id` | Yes | No | — | — | — | — |
| `run_id` | `int` | `run_id` | Yes | No | — | — | — | — |
| `claim_id` | `str` | `claim_id` | Yes | No | — | min_length=16; max_length=64 | — | — |
| `claim_generation` | `int` | `claim_generation` | Yes | No | — | ge=1 | — | — |
| `expected_task_version` | `int` | `expected_task_version` | Yes | No | — | ge=1 | — | — |
| `title` | `str` | `title` | Yes | No | — | min_length=1; max_length=500 | — | — |
| `description` | `str` | `description` | Yes | No | — | min_length=1; max_length=12000 | — | — |
| `blocking` | `bool` | `blocking` | No | No | `False` | — | — | — |
| `evidence` | `dict[str, Any]` | `evidence` | No | No | factory: `dict` | max_length=unknown (MAX_AGENT_JSON_FIELDS) | — | — |
| `suggested_labels` | `list[str]` | `suggested_labels` | No | No | factory: `list` | max_length=50 | — | — |
| `priority_hint` | `Optional[int]` | `priority_hint` | No | Yes | `None` | ge=1; le=10 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_evidence_size` | `(value: dict[str, Any]) -> dict[str, Any]` | `@field_validator('evidence')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentDiscoveryTriageCreate (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["report_discovery (backend/app/mcp_agent_tools.py)"]
    n3["report_agent_discovery (backend/app/routers/agent.py)"]
    n4["AgentWorkService.report_discovery (backend/app/services/agent_work_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 1 | `assignment_id`, `blocking`, `claim_generation`, `claim_id`, `description`, `evidence`, `expected_task_version`, `priority_hint`, `run_id`, `suggested_labels`, `task_id`, `title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `report_discovery` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `report_agent_discovery` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.report_discovery` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
