# CredentialDeliveryError

**Location:** `backend/app/services/agent_team_credentials.py:9`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [agent_team_credentials](../modules/agent_team_credentials.md)

## Description

Raised when a one-time actor key did not reach the approved sink.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CredentialDeliveryError (backend/app/services/agent_team_credentials.py)"]
    n1["RuntimeError"]
    n2["FilesystemAgentTeamCredentialSink.deliver (backend/app/services/agent_team_credentials.py)"]
    n3["AgentTeamSetupService._apply_create_or_update (backend/app/services/agent_team_setup_service.py)"]
    n4["AgentTeamSetupService._apply_identity_replacement (backend/app/services/agent_team_setup_service.py)"]
    n5["AgentTeamSetupService._apply_replace_recovery (backend/app/services/agent_team_setup_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/agent_team_credentials.md"
    click n2 "../modules/agent_team_credentials.md"
    click n3 "../modules/agent_team_setup_service.md"
    click n4 "../modules/agent_team_setup_service.md"
    click n5 "../modules/agent_team_setup_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_credentials](../modules/agent_team_credentials.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `FilesystemAgentTeamCredentialSink.deliver` | call | [agent_team_credentials](../modules/agent_team_credentials.md) | 5 |
| `AgentTeamSetupService._apply_create_or_update` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService._apply_identity_replacement` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService._apply_replace_recovery` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 2 |
