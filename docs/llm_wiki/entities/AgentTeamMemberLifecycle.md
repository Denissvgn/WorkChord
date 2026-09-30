# AgentTeamMemberLifecycle

**Location:** `backend/app/schemas/agent_team_setup.py:114`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [agent_team_setup](../modules/agent_team_setup.md)

## Description

_Auto-generated from `AgentTeamMemberLifecycle` in `backend/app/schemas/agent_team_setup.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `DESIRED` | `'desired'` | — |
| `CONFIGURED` | `'configured'` | — |
| `CREDENTIAL_DELIVERED` | `'credential_delivered'` | — |
| `ONBOARDING` | `'onboarding'` | — |
| `CONNECTED` | `'connected'` | — |
| `RUNTIME_READY` | `'runtime_ready'` | — |
| `DISABLED` | `'disabled'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamMemberLifecycle (backend/app/schemas/agent_team_setup.py)"]
    n1["StrEnum"]
    n2["AgentTeamSetupService._status_for_topology (backend/app/services/agent_team_setup_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/agent_team_setup.md"
    click n2 "../modules/agent_team_setup_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup](../modules/agent_team_setup.md) | 0 | `CONFIGURED`, `CONNECTED`, `CREDENTIAL_DELIVERED`, `DESIRED`, `DISABLED`, `ONBOARDING`, `RUNTIME_READY` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentTeamSetupService._status_for_topology` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
