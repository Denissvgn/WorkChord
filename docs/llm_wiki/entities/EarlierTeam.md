# EarlierTeam

**Location:** `backend/tests/test_agent_team_setup_stored_contract.py:236`
**Kind:** Class
**Bases:** —
**Module:** [test_agent_team_setup_stored_contract](../modules/test_agent_team_setup_stored_contract.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

_Auto-generated from `EarlierTeam` in `backend/tests/test_agent_team_setup_stored_contract.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `service` | `AgentTeamSetupService` | *required* | — |
| `sink` | `CapturingCredentialSink` | *required* | — |
| `handoffs` | `dict[str, AgentTeamRuntimeHandoff]` | *required* | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["EarlierTeam (backend/tests/test_agent_team_setup_stored_contract.py)"]
    n1["store_team_under_earlier_rules (backend/tests/test_agent_team_setup_stored_contract.py)"]
    n1 --> n0
    click n0 "../modules/test_agent_team_setup_stored_contract.md"
    click n1 "../modules/test_agent_team_setup_stored_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_agent_team_setup_stored_contract](../modules/test_agent_team_setup_stored_contract.md) | 0 | `handoffs`, `service`, `sink` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `store_team_under_earlier_rules` | call | [test_agent_team_setup_stored_contract](../modules/test_agent_team_setup_stored_contract.md) | 1 |
| `store_team_under_earlier_rules` | type_reference | [test_agent_team_setup_stored_contract](../modules/test_agent_team_setup_stored_contract.md) | — |
