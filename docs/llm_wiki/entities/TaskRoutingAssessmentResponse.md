# TaskRoutingAssessmentResponse

**Location:** `backend/app/schemas/agent_routing.py:753`
**Kind:** Pydantic model
**Bases:** `PersistedTaskRoutingAssessmentFields`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Audit-readable assessment projection with fail-closed routeability.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `require_conformant_current_assessment` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |
| `policy_conformant` | `bool` | `policy_conformant` | No | No | `False` | — | — | — |
| `is_current` | `bool` | `is_current` | Yes | No | — | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `require_conformant_current_assessment` | `() -> 'TaskRoutingAssessmentResponse'` | `@model_validator(mode='after')` | — |
| `from_record` | `(record: Any, *, current_task_version: int) -> 'TaskRoutingAssessmentResponse'` | `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskRoutingAssessmentResponse (backend/app/schemas/agent_routing.py)"]
    n1["PersistedTaskRoutingAssessmentFields (backend/app/schemas/agent_routing.py)"]
    n2["TaskRoutingAssessmentResponse.from_record (backend/app/schemas/agent_routing.py)"]
    n3["TaskRoutingAssessmentResponse.require_conformant_current_assessment (backend/app/schemas/agent_routing.py)"]
    n4["backend/app/services/agent_routing_service.py"]
    n5["backend/tests/test_agent_routing_contract.py"]
    n6["backend/tests/test_agent_routing_data.py"]
    n7["_history (backend/tests/test_agent_routing_history_surfaces.py)"]
    n8["_assessment_response (backend/tests/test_agent_routing_wave3_contract.py)"]
    n9["_assert_selected_snapshot (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n10["_create_assessment_with_parity (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n11["_dispatch (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n12["_preview_with_parity (backend/tests/test_agent_routing_wave6_qualification.py)"]
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
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/agent_routing.md"
    click n3 "../modules/agent_routing.md"
    click n4 "../modules/agent_routing_service.md"
    click n5 "../modules/test_agent_routing_contract.md"
    click n6 "../modules/test_agent_routing_data.md"
    click n7 "../modules/test_agent_routing_history_surfaces.md"
    click n8 "../modules/test_agent_routing_wave3_contract.md"
    click n9 "../modules/test_agent_routing_wave6_qualification.md"
    click n10 "../modules/test_agent_routing_wave6_qualification.md"
    click n11 "../modules/test_agent_routing_wave6_qualification.md"
    click n12 "../modules/test_agent_routing_wave6_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 2 | `created_at`, `id`, `is_current`, `policy_conformant` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PersistedTaskRoutingAssessmentFields` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRoutingAssessmentResponse.from_record` | type_reference | [agent_routing](../modules/agent_routing.md) | — |
| `TaskRoutingAssessmentResponse.require_conformant_current_assessment` | type_reference | [agent_routing](../modules/agent_routing.md) | — |
| `agent_routing_service` | import | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `test_agent_routing_contract` | import | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
| `test_agent_routing_data` | import | [test_agent_routing_data](../modules/test_agent_routing_data.md) | — |
| `_history` | call | [test_agent_routing_history_surfaces](../modules/test_agent_routing_history_surfaces.md) | 1 |
| `_assessment_response` | call | [test_agent_routing_wave3_contract](../modules/test_agent_routing_wave3_contract.md) | 1 |
| `_assessment_response` | type_reference | [test_agent_routing_wave3_contract](../modules/test_agent_routing_wave3_contract.md) | — |
| `_assert_selected_snapshot` | type_reference | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | — |
| `_create_assessment_with_parity` | type_reference | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | — |
| `_dispatch` | type_reference | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | — |
| `_preview_with_parity` | type_reference | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | — |
