# AgentTeamManifestRequest

**Location:** `backend/app/schemas/agent_team_setup.py:761`
**Kind:** Pydantic model
**Bases:** `AgentTeamSetupModel`
**Module:** [agent_team_setup](../modules/agent_team_setup.md)

## Description

_Auto-generated from `AgentTeamManifestRequest` in `backend/app/schemas/agent_team_setup.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `manifest` | `AgentTeamMaster` | `manifest` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamManifestRequest (backend/app/schemas/agent_team_setup.py)"]
    n1["AgentTeamSetupModel (backend/app/schemas/agent_team_setup.py)"]
    n2["validate_agent_team_master (backend/app/routers/agent.py)"]
    n3["AgentTeamSetupService.validate (backend/app/services/agent_team_setup_service.py)"]
    n4["test_deployed_catalog_supports_validation_and_bound_planning (backend/tests/test_agent_team_catalog.py)"]
    n5["test_fresh_apply_replay_onboarding_and_runtime_readiness (backend/tests/test_agent_team_setup.py)"]
    n6["test_starting_points_offer_a_valid_catalog_filled_template_and_the_applied_manifest (backend/tests/test_agent_team_setup.py)"]
    n7["test_setup_scenario_11_compatibility_preflight_is_non_mutating (backend/tests/test_agent_team_setup_qualification.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/agent_team_setup.md"
    click n1 "../modules/agent_team_setup.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_team_setup_service.md"
    click n4 "../modules/test_agent_team_catalog.md"
    click n5 "../modules/test_agent_team_setup.md"
    click n6 "../modules/test_agent_team_setup.md"
    click n7 "../modules/test_agent_team_setup_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup](../modules/agent_team_setup.md) | 0 | `manifest` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentTeamSetupModel` | [agent_team_setup](../modules/agent_team_setup.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `validate_agent_team_master` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentTeamSetupService.validate` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `test_deployed_catalog_supports_validation_and_bound_planning` | call | [test_agent_team_catalog](../modules/test_agent_team_catalog.md) | 1 |
| `test_fresh_apply_replay_onboarding_and_runtime_readiness` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_starting_points_offer_a_valid_catalog_filled_template_and_the_applied_manifest` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_setup_scenario_11_compatibility_preflight_is_non_mutating` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
