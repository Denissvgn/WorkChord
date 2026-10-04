# CapturingCredentialSink

**Location:** `backend/tests/test_agent_team_setup.py:71`
**Kind:** Class
**Bases:** —
**Module:** [test_agent_team_setup](../modules/test_agent_team_setup.md)

## Description

_Auto-generated from `CapturingCredentialSink` in `backend/tests/test_agent_team_setup.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `() -> None` | — | — |
| `deliver` | *(async)* `(*, credential_ref: str, actor_key: str, actor_name: str, api_key: str) -> str` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CapturingCredentialSink (backend/tests/test_agent_team_setup.py)"]
    n1["FailingOnceCredentialSink (backend/tests/test_agent_team_setup.py)"]
    n2["test_confirmed_identity_replacement_disables_old_actor (backend/tests/test_agent_team_setup.py)"]
    n3["test_fresh_apply_replay_onboarding_and_runtime_readiness (backend/tests/test_agent_team_setup.py)"]
    n4["test_topologies_share_catalog_and_profile_references_not_identities (backend/tests/test_agent_team_setup.py)"]
    n5["provision_ready_topology (backend/tests/test_agent_team_setup_qualification.py)"]
    n6["test_setup_scenario_03_runtime_handoff_failure_resumes_in_place (backend/tests/test_agent_team_setup_qualification.py)"]
    n7["test_setup_scenario_04_adopts_without_credential_rotation (backend/tests/test_agent_team_setup_qualification.py)"]
    n8["test_setup_scenario_06_add_binding_change_and_explicit_disable (backend/tests/test_agent_team_setup_qualification.py)"]
    n9["test_setup_scenario_11_compatibility_preflight_is_non_mutating (backend/tests/test_agent_team_setup_qualification.py)"]
    n10["test_setup_scenarios_01_02_fresh_multi_worker_and_noop_reapply (backend/tests/test_agent_team_setup_qualification.py)"]
    n11["test_setup_scenarios_05_07_08_drift_readiness_and_redaction (backend/tests/test_agent_team_setup_qualification.py)"]
    n1 --> n0
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
    click n0 "../modules/test_agent_team_setup.md"
    click n1 "../modules/test_agent_team_setup.md"
    click n2 "../modules/test_agent_team_setup.md"
    click n3 "../modules/test_agent_team_setup.md"
    click n4 "../modules/test_agent_team_setup.md"
    click n5 "../modules/test_agent_team_setup_qualification.md"
    click n6 "../modules/test_agent_team_setup_qualification.md"
    click n7 "../modules/test_agent_team_setup_qualification.md"
    click n8 "../modules/test_agent_team_setup_qualification.md"
    click n9 "../modules/test_agent_team_setup_qualification.md"
    click n10 "../modules/test_agent_team_setup_qualification.md"
    click n11 "../modules/test_agent_team_setup_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_agent_team_setup](../modules/test_agent_team_setup.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Subclass | `FailingOnceCredentialSink` | [test_agent_team_setup](../modules/test_agent_team_setup.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_confirmed_identity_replacement_disables_old_actor` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_fresh_apply_replay_onboarding_and_runtime_readiness` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_topologies_share_catalog_and_profile_references_not_identities` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `provision_ready_topology` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenario_03_runtime_handoff_failure_resumes_in_place` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenario_04_adopts_without_credential_rotation` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenario_06_add_binding_change_and_explicit_disable` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenario_11_compatibility_preflight_is_non_mutating` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenarios_01_02_fresh_multi_worker_and_noop_reapply` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenarios_05_07_08_drift_readiness_and_redaction` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
