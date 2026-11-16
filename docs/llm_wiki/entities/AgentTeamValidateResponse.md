# AgentTeamValidateResponse

**Location:** `backend/app/schemas/agent_team_setup.py:766`
**Kind:** Class
**Bases:** `AgentTeamSetupModel`
**Module:** [agent_team_setup](../modules/agent_team_setup.md)

## Description

_Auto-generated from `AgentTeamValidateResponse` in `backend/app/schemas/agent_team_setup.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `schema_version` | `Literal['agent-team-validation-v1']` | `'agent-team-validation-v1'` | — |
| `valid` | `bool` | *required* | — |
| `manifest_digest` | `str` | *required* | — |
| `normalized_manifest` | `AgentTeamMaster` | *required* | — |
| `blocker_codes` | `tuple[str, ...]` | `()` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamValidateResponse (backend/app/schemas/agent_team_setup.py)"]
    n1["AgentTeamSetupModel (backend/app/schemas/agent_team_setup.py)"]
    n2["validate_agent_team_master (backend/app/routers/agent.py)"]
    n3["AgentTeamSetupService.validate (backend/app/services/agent_team_setup_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/agent_team_setup.md"
    click n1 "../modules/agent_team_setup.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_team_setup_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup](../modules/agent_team_setup.md) | 0 | `blocker_codes`, `manifest_digest`, `normalized_manifest`, `schema_version`, `valid` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentTeamSetupModel` | [agent_team_setup](../modules/agent_team_setup.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `validate_agent_team_master` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentTeamSetupService.validate` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService.validate` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
