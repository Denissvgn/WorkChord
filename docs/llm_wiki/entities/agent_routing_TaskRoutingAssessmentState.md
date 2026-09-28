# TaskRoutingAssessmentState

**Location:** `backend/app/schemas/agent_routing.py:801`
**Kind:** Pydantic model
**Bases:** `RoutingContractModel`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Explicit current, stale, or absent assessment state for one task.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_lifecycle_state` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | ge=1; strict=True | — | — |
| `current_task_version` | `int` | `current_task_version` | Yes | No | — | ge=1; strict=True | — | — |
| `state` | `Literal['none', 'current', 'stale']` | `state` | Yes | No | — | — | — | — |
| `assessment` | `TaskRoutingAssessmentResponse \| None` | `assessment` | No | Yes | `None` | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_lifecycle_state` | `() -> 'TaskRoutingAssessmentState'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskRoutingAssessmentState (backend/app/schemas/agent_routing.py)"]
    n1["RoutingContractModel (backend/app/schemas/agent_routing.py)"]
    n2["get_task_routing_assessment (backend/app/routers/agent_planning.py)"]
    n3["TaskRoutingAssessmentState.validate_lifecycle_state (backend/app/schemas/agent_routing.py)"]
    n4["AgentRoutingService.get_assessment_state (backend/app/services/agent_routing_service.py)"]
    n5["test_assessment_state_and_history_are_explicit_and_version_bound (backend/tests/test_agent_routing_wave3_contract.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/routers_agent_planning.md"
    click n3 "../modules/agent_routing.md"
    click n4 "../modules/agent_routing_service.md"
    click n5 "../modules/test_agent_routing_wave3_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 1 | `assessment`, `current_task_version`, `state`, `task_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RoutingContractModel` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_task_routing_assessment` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `TaskRoutingAssessmentState.validate_lifecycle_state` | type_reference | [agent_routing](../modules/agent_routing.md) | — |
| `AgentRoutingService.get_assessment_state` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentRoutingService.get_assessment_state` | type_reference | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `test_assessment_state_and_history_are_explicit_and_version_bound` | call | [test_agent_routing_wave3_contract](../modules/test_agent_routing_wave3_contract.md) | 2 |
