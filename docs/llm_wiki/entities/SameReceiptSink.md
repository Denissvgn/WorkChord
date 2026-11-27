# SameReceiptSink

**Location:** `backend/tests/test_agent_team_runtime_identity.py:42`
**Kind:** Class
**Bases:** `CapturingCredentialSink`
**Module:** [test_agent_team_runtime_identity](../modules/test_agent_team_runtime_identity.md)

## Description

A sink whose delivery receipt does not change between deliveries, and that can lose one.

The receipt of the production sink is a digest of fixed inputs, so a runtime
identity must not depend on it.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(lose: str \| None = None) -> None` | — | — |
| `deliver` | *(async)* `(*, credential_ref: str, actor_key: str, actor_name: str, api_key: str) -> str` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SameReceiptSink (backend/tests/test_agent_team_runtime_identity.py)"]
    n1["CapturingCredentialSink (backend/tests/test_agent_team_setup.py)"]
    n2["test_a_recovered_credential_issues_a_new_identity (backend/tests/test_agent_team_runtime_identity.py)"]
    n3["test_a_replaced_member_issues_a_new_identity_and_the_takeover_is_a_visible_change (backend/tests/test_agent_team_runtime_identity.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/test_agent_team_runtime_identity.md"
    click n1 "../modules/test_agent_team_setup.md"
    click n2 "../modules/test_agent_team_runtime_identity.md"
    click n3 "../modules/test_agent_team_runtime_identity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_agent_team_runtime_identity](../modules/test_agent_team_runtime_identity.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `CapturingCredentialSink` | [test_agent_team_setup](../modules/test_agent_team_setup.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_a_recovered_credential_issues_a_new_identity` | call | [test_agent_team_runtime_identity](../modules/test_agent_team_runtime_identity.md) | 1 |
| `test_a_replaced_member_issues_a_new_identity_and_the_takeover_is_a_visible_change` | call | [test_agent_team_runtime_identity](../modules/test_agent_team_runtime_identity.md) | 1 |
