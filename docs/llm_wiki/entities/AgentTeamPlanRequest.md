# AgentTeamPlanRequest

**Location:** `backend/app/schemas/agent_team_setup.py:728`
**Kind:** Pydantic model
**Bases:** `AgentTeamSetupModel`
**Module:** [agent_team_setup](../modules/agent_team_setup.md)

## Description

_Auto-generated from `AgentTeamPlanRequest` in `backend/app/schemas/agent_team_setup.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `manifest` | `AgentTeamMaster` | `manifest` | Yes | No | — | — | — | — |
| `expected_topology_revision` | `int` | `expected_topology_revision` | Yes | No | — | ge=0 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamPlanRequest (backend/app/schemas/agent_team_setup.py)"]
    n1["AgentTeamSetupModel (backend/app/schemas/agent_team_setup.py)"]
    n2["plan_agent_team_reconciliation (backend/app/routers/agent.py)"]
    n3["AgentTeamSetupService.apply (backend/app/services/agent_team_setup_service.py)"]
    n4["AgentTeamSetupService.plan (backend/app/services/agent_team_setup_service.py)"]
    n5["test_confirmed_identity_replacement_disables_old_actor (backend/tests/test_agent_team_setup.py)"]
    n6["test_fresh_apply_replay_onboarding_and_runtime_readiness (backend/tests/test_agent_team_setup.py)"]
    n7["test_topologies_share_catalog_and_profile_references_not_identities (backend/tests/test_agent_team_setup.py)"]
    n8["test_uncertain_delivery_requires_explicit_new_reference_recovery (backend/tests/test_agent_team_setup.py)"]
    n9["apply_manifest (backend/tests/test_agent_team_setup_qualification.py)"]
    n10["test_setup_scenario_04_adopts_without_credential_rotation (backend/tests/test_agent_team_setup_qualification.py)"]
    n11["test_setup_scenario_06_add_binding_change_and_explicit_disable (backend/tests/test_agent_team_setup_qualification.py)"]
    n12["test_setup_scenario_11_compatibility_preflight_is_non_mutating (backend/tests/test_agent_team_setup_qualification.py)"]
    n13["test_setup_scenarios_05_07_08_drift_readiness_and_redaction (backend/tests/test_agent_team_setup_qualification.py)"]
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
    click n0 "../modules/agent_team_setup.md"
    click n1 "../modules/agent_team_setup.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_team_setup_service.md"
    click n4 "../modules/agent_team_setup_service.md"
    click n5 "../modules/test_agent_team_setup.md"
    click n6 "../modules/test_agent_team_setup.md"
    click n7 "../modules/test_agent_team_setup.md"
    click n8 "../modules/test_agent_team_setup.md"
    click n9 "../modules/test_agent_team_setup_qualification.md"
    click n10 "../modules/test_agent_team_setup_qualification.md"
    click n11 "../modules/test_agent_team_setup_qualification.md"
    click n12 "../modules/test_agent_team_setup_qualification.md"
    click n13 "../modules/test_agent_team_setup_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup](../modules/agent_team_setup.md) | 0 | `expected_topology_revision`, `manifest` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentTeamSetupModel` | [agent_team_setup](../modules/agent_team_setup.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `plan_agent_team_reconciliation` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentTeamSetupService.apply` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService.plan` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `test_confirmed_identity_replacement_disables_old_actor` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 2 |
| `test_fresh_apply_replay_onboarding_and_runtime_readiness` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_topologies_share_catalog_and_profile_references_not_identities` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_uncertain_delivery_requires_explicit_new_reference_recovery` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 2 |
| `apply_manifest` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenario_04_adopts_without_credential_rotation` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenario_06_add_binding_change_and_explicit_disable` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenario_11_compatibility_preflight_is_non_mutating` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenarios_05_07_08_drift_readiness_and_redaction` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
