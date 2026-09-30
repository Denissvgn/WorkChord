# AgentTeamCurrentSnapshot

**Location:** `backend/app/schemas/agent_team_setup.py:432`
**Kind:** Pydantic model
**Bases:** `AgentTeamSetupModel`
**Module:** [agent_team_setup](../modules/agent_team_setup.md)

## Description

Current topology state with installation-local IDs kept separate.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `topology_key` | `str` | `topology_key` | Yes | No | — | pattern=unknown (STABLE_KEY_PATTERN) | — | — |
| `revision` | `int` | `revision` | Yes | No | — | ge=0 | — | — |
| `manifest_digest` | `str \| None` | `manifest_digest` | No | Yes | `None` | pattern=unknown (SHA256_PATTERN) | — | — |
| `members` | `tuple[AgentTeamCurrentMember, ...]` | `members` | No | No | `()` | max_length=unknown (MAX_AGENT_TEAM_MEMBERS * 2) | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamCurrentSnapshot (backend/app/schemas/agent_team_setup.py)"]
    n1["AgentTeamSetupModel (backend/app/schemas/agent_team_setup.py)"]
    n2["reconcile_agent_team_master (backend/app/schemas/agent_team_setup.py)"]
    n3["AgentTeamSetupService._current_snapshot (backend/app/services/agent_team_setup_service.py)"]
    n4["test_reconciliation_is_stable_and_never_hard_deletes (backend/tests/test_agent_team_setup.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/agent_team_setup.md"
    click n1 "../modules/agent_team_setup.md"
    click n2 "../modules/agent_team_setup.md"
    click n3 "../modules/agent_team_setup_service.md"
    click n4 "../modules/test_agent_team_setup.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup](../modules/agent_team_setup.md) | 0 | `manifest_digest`, `members`, `revision`, `topology_key` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentTeamSetupModel` | [agent_team_setup](../modules/agent_team_setup.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `reconcile_agent_team_master` | type_reference | [agent_team_setup](../modules/agent_team_setup.md) | — |
| `AgentTeamSetupService._current_snapshot` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 2 |
| `AgentTeamSetupService._current_snapshot` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `test_reconciliation_is_stable_and_never_hard_deletes` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 2 |
