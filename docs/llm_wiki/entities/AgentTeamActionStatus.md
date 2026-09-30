# AgentTeamActionStatus

**Location:** `backend/app/schemas/agent_team_setup.py:124`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [agent_team_setup](../modules/agent_team_setup.md)

## Description

_Auto-generated from `AgentTeamActionStatus` in `backend/app/schemas/agent_team_setup.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `PENDING` | `'pending'` | — |
| `APPLIED` | `'applied'` | — |
| `NO_CHANGE` | `'no_change'` | — |
| `BLOCKED` | `'blocked'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamActionStatus (backend/app/schemas/agent_team_setup.py)"]
    n1["StrEnum"]
    n2["backend/app/services/agent_team_setup_service.py"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/agent_team_setup.md"
    click n2 "../modules/agent_team_setup_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup](../modules/agent_team_setup.md) | 0 | `APPLIED`, `BLOCKED`, `NO_CHANGE`, `PENDING` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent_team_setup_service` | import | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
