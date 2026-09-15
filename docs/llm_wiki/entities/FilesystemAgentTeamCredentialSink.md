# FilesystemAgentTeamCredentialSink

**Location:** `backend/app/services/agent_team_setup_service.py:137`
**Kind:** Class
**Bases:** —
**Module:** [agent_team_setup_service](../modules/agent_team_setup_service.md)

## Description

Write one-time credentials to an operator-owned mode-0700 directory.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(*, directory: str, reference: str)` | — | — |
| `available` | `() -> bool` | `@property` | — |
| `deliver` | *(async)* `(*, credential_ref: str, actor_key: str, actor_name: str, api_key: str) -> str` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["FilesystemAgentTeamCredentialSink (backend/app/services/agent_team_setup_service.py)"]
    n1["AgentTeamSetupService.__init__ (backend/app/services/agent_team_setup_service.py)"]
    n1 --> n0
    click n0 "../modules/agent_team_setup_service.md"
    click n1 "../modules/agent_team_setup_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup_service](../modules/agent_team_setup_service.md) | 3 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentTeamSetupService.__init__` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
