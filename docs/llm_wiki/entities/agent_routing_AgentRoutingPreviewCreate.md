# AgentRoutingPreviewCreate

**Location:** `backend/app/schemas/agent_routing.py:925`
**Kind:** Pydantic model
**Bases:** `RoutingContractModel`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Non-dispatching exact-actor preview bound to current task state.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `require_review_purpose` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `purpose` | `Literal['execution', 'verification']` | `purpose` | Yes | No | — | — | — | — |
| `assessment_id` | `int` | `assessment_id` | Yes | No | — | ge=1; strict=True | — | — |
| `expected_task_version` | `int` | `expected_task_version` | Yes | No | — | ge=1; strict=True | — | — |
| `reviewer_profile_id` | `int \| None` | `reviewer_profile_id` | No | Yes | `None` | ge=1; strict=True | — | — |
| `review_evidence_id` | `int \| None` | `review_evidence_id` | No | Yes | `None` | ge=1; strict=True | — | — |
| `review_assignment_id` | `int \| None` | `review_assignment_id` | No | Yes | `None` | ge=1; strict=True | — | — |
| `focus_actor_id` | `int \| None` | `focus_actor_id` | No | Yes | `None` | ge=1; strict=True | — | — |
| `focus_model_binding_id` | `int \| None` | `focus_model_binding_id` | No | Yes | `None` | ge=1; strict=True | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `require_review_purpose` | `()` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingPreviewCreate (backend/app/schemas/agent_routing.py)"]
    n1["RoutingContractModel (backend/app/schemas/agent_routing.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["preview_task_routing (backend/app/routers/agent.py)"]
    n4["AgentRoutingService._build_preview (backend/app/services/agent_routing_service.py)"]
    n5["AgentRoutingService.preview_task_routing (backend/app/services/agent_routing_service.py)"]
    n6["AgentRoutingService.validate_assignment_selection (backend/app/services/agent_routing_service.py)"]
    n7["check_supervised_selection (backend/app/services/review_evidence.py)"]
    n8["test_completed_rework_update_persists_prior_and_new_routing_lineage (backend/tests/test_agent_routing_service.py)"]
    n9["test_model_aware_assignment_and_begin_enforce_observed_model (backend/tests/test_agent_routing_service.py)"]
    n10["test_preview_is_deterministic_and_relevant_mutation_invalidates_it (backend/tests/test_agent_routing_service.py)"]
    n11["test_verification_independence_requires_authoritative_profile_history (backend/tests/test_agent_routing_service.py)"]
    n12["test_preview_contract_accepts_eligible_and_explicit_no_candidate_states (backend/tests/test_agent_routing_wave3_contract.py)"]
    n13["_preview_with_parity (backend/tests/test_agent_routing_wave6_qualification.py)"]
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
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/agent_routing_service.md"
    click n5 "../modules/agent_routing_service.md"
    click n6 "../modules/agent_routing_service.md"
    click n7 "../modules/services_review_evidence.md"
    click n8 "../modules/test_agent_routing_service.md"
    click n9 "../modules/test_agent_routing_service.md"
    click n10 "../modules/test_agent_routing_service.md"
    click n11 "../modules/test_agent_routing_service.md"
    click n12 "../modules/test_agent_routing_wave3_contract.md"
    click n13 "../modules/test_agent_routing_wave6_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 1 | `assessment_id`, `expected_task_version`, `focus_actor_id`, `focus_model_binding_id`, `purpose`, `review_assignment_id`, `review_evidence_id`, `reviewer_profile_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RoutingContractModel` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `preview_task_routing` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentRoutingService._build_preview` | type_reference | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `AgentRoutingService.preview_task_routing` | type_reference | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `AgentRoutingService.validate_assignment_selection` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `check_supervised_selection` | call | [services_review_evidence](../modules/services_review_evidence.md) | 1 |
| `test_completed_rework_update_persists_prior_and_new_routing_lineage` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 1 |
| `test_model_aware_assignment_and_begin_enforce_observed_model` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 1 |
| `test_preview_is_deterministic_and_relevant_mutation_invalidates_it` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 1 |
| `test_verification_independence_requires_authoritative_profile_history` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 1 |
| `test_preview_contract_accepts_eligible_and_explicit_no_candidate_states` | call | [test_agent_routing_wave3_contract](../modules/test_agent_routing_wave3_contract.md) | 1 |
| `_preview_with_parity` | call | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | 1 |

> References: showing 12 of 20 logical references; 8 omitted by the 12-row generated summary limit.
