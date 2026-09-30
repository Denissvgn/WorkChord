# AgentTeamApplyRequest

**Location:** `backend/app/schemas/agent_team_setup.py:733`
**Kind:** Pydantic model
**Bases:** `AgentTeamSetupModel`
**Module:** [agent_team_setup](../modules/agent_team_setup.md)

## Description

_Auto-generated from `AgentTeamApplyRequest` in `backend/app/schemas/agent_team_setup.py`._

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `normalize_action_ids` | field | approved_action_ids, confirmed_action_ids | after | — |
| `confirmations_are_approved` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `manifest` | `AgentTeamMaster` | `manifest` | Yes | No | — | — | — | — |
| `expected_topology_revision` | `int` | `expected_topology_revision` | Yes | No | — | ge=0 | — | — |
| `plan_digest` | `str` | `plan_digest` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `approved_action_ids` | `tuple[str, ...]` | `approved_action_ids` | Yes | No | — | min_length=1; max_length=unknown (MAX_AGENT_TEAM_ACTIONS) | — | — |
| `confirmed_action_ids` | `tuple[str, ...]` | `confirmed_action_ids` | No | No | `()` | max_length=unknown (MAX_AGENT_TEAM_ACTIONS) | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `normalize_action_ids` | `(value: tuple[str, ...], info: Any) -> tuple[str, ...]` | `@field_validator('approved_action_ids', 'confirmed_action_ids')`, `@classmethod` | — |
| `confirmations_are_approved` | `() -> 'AgentTeamApplyRequest'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamApplyRequest (backend/app/schemas/agent_team_setup.py)"]
    n1["AgentTeamSetupModel (backend/app/schemas/agent_team_setup.py)"]
    n2["apply_agent_team_reconciliation (backend/app/routers/agent.py)"]
    n3["AgentTeamApplyRequest.confirmations_are_approved (backend/app/schemas/agent_team_setup.py)"]
    n4["AgentTeamSetupService._apply_request_digest (backend/app/services/agent_team_setup_service.py)"]
    n5["AgentTeamSetupService.apply (backend/app/services/agent_team_setup_service.py)"]
    n6["test_confirmed_identity_replacement_disables_old_actor (backend/tests/test_agent_team_setup.py)"]
    n7["test_fresh_apply_replay_onboarding_and_runtime_readiness (backend/tests/test_agent_team_setup.py)"]
    n8["test_uncertain_delivery_requires_explicit_new_reference_recovery (backend/tests/test_agent_team_setup.py)"]
    n9["apply_manifest (backend/tests/test_agent_team_setup_qualification.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/agent_team_setup.md"
    click n1 "../modules/agent_team_setup.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_team_setup.md"
    click n4 "../modules/agent_team_setup_service.md"
    click n5 "../modules/agent_team_setup_service.md"
    click n6 "../modules/test_agent_team_setup.md"
    click n7 "../modules/test_agent_team_setup.md"
    click n8 "../modules/test_agent_team_setup.md"
    click n9 "../modules/test_agent_team_setup_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup](../modules/agent_team_setup.md) | 2 | `approved_action_ids`, `confirmed_action_ids`, `expected_topology_revision`, `manifest`, `plan_digest` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentTeamSetupModel` | [agent_team_setup](../modules/agent_team_setup.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `apply_agent_team_reconciliation` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentTeamApplyRequest.confirmations_are_approved` | type_reference | [agent_team_setup](../modules/agent_team_setup.md) | — |
| `AgentTeamSetupService._apply_request_digest` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService.apply` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `test_confirmed_identity_replacement_disables_old_actor` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 2 |
| `test_fresh_apply_replay_onboarding_and_runtime_readiness` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_uncertain_delivery_requires_explicit_new_reference_recovery` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 2 |
| `apply_manifest` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
