# FailingForOneMemberSink

**Location:** `backend/tests/test_agent_team_setup_stored_contract.py:123`
**Kind:** Class
**Bases:** `CapturingCredentialSink`
**Module:** [test_agent_team_setup_stored_contract](../modules/test_agent_team_setup_stored_contract.md)

## Description

Lose the first credential delivery for one chosen member.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(actor_key: str) -> None` | — | — |
| `deliver` | *(async)* `(*, credential_ref: str, actor_key: str, actor_name: str, api_key: str) -> str` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["FailingForOneMemberSink (backend/tests/test_agent_team_setup_stored_contract.py)"]
    n1["CapturingCredentialSink (backend/tests/test_agent_team_setup.py)"]
    n2["test_lost_credential_on_an_outdated_contract_recovers_and_updates_it (backend/tests/test_agent_team_setup_stored_contract.py)"]
    n3["test_lost_credential_recovery_still_changes_only_the_credential (backend/tests/test_agent_team_setup_stored_contract.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/test_agent_team_setup_stored_contract.md"
    click n1 "../modules/test_agent_team_setup.md"
    click n2 "../modules/test_agent_team_setup_stored_contract.md"
    click n3 "../modules/test_agent_team_setup_stored_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_agent_team_setup_stored_contract](../modules/test_agent_team_setup_stored_contract.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `CapturingCredentialSink` | [test_agent_team_setup](../modules/test_agent_team_setup.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_lost_credential_on_an_outdated_contract_recovers_and_updates_it` | call | [test_agent_team_setup_stored_contract](../modules/test_agent_team_setup_stored_contract.md) | 1 |
| `test_lost_credential_recovery_still_changes_only_the_credential` | call | [test_agent_team_setup_stored_contract](../modules/test_agent_team_setup_stored_contract.md) | 1 |
