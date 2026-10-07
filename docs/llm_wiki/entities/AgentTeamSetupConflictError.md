# AgentTeamSetupConflictError

**Location:** `backend/app/services/agent_team_setup_service.py:101`
**Kind:** Class
**Bases:** `AgentConflictError`
**Module:** [agent_team_setup_service](../modules/agent_team_setup_service.md)

## Description

Stable conflict envelope shared by setup REST and MCP reads.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code: str, message: str, **context: Any)` | — | — |
| `detail` | `() -> dict[str, Any]` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamSetupConflictError (backend/app/services/agent_team_setup_service.py)"]
    n1["AgentConflictError (backend/app/services/agent_service.py)"]
    n2["backend/app/mcp_server.py"]
    n3["backend/app/routers/agent.py"]
    n4["AgentTeamSetupService._apply_create_or_update (backend/app/services/agent_team_setup_service.py)"]
    n5["AgentTeamSetupService._apply_disable (backend/app/services/agent_team_setup_service.py)"]
    n6["AgentTeamSetupService._apply_identity_replacement (backend/app/services/agent_team_setup_service.py)"]
    n7["AgentTeamSetupService._apply_replace_recovery (backend/app/services/agent_team_setup_service.py)"]
    n8["AgentTeamSetupService._catalog_entries (backend/app/services/agent_team_setup_service.py)"]
    n9["AgentTeamSetupService._current_snapshot (backend/app/services/agent_team_setup_service.py)"]
    n10["AgentTeamSetupService._ensure_topology_for_apply (backend/app/services/agent_team_setup_service.py)"]
    n11["AgentTeamSetupService._execute_action (backend/app/services/agent_team_setup_service.py)"]
    n12["AgentTeamSetupService._increment_ack_attempt (backend/app/services/agent_team_setup_service.py)"]
    n13["AgentTeamSetupService._replay_apply (backend/app/services/agent_team_setup_service.py)"]
    n0 --> n1
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
    n12 --> n0
    n13 --> n0
    click n0 "../modules/agent_team_setup_service.md"
    click n1 "../modules/agent_service.md"
    click n2 "../modules/mcp_server.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/agent_team_setup_service.md"
    click n5 "../modules/agent_team_setup_service.md"
    click n6 "../modules/agent_team_setup_service.md"
    click n7 "../modules/agent_team_setup_service.md"
    click n8 "../modules/agent_team_setup_service.md"
    click n9 "../modules/agent_team_setup_service.md"
    click n10 "../modules/agent_team_setup_service.md"
    click n11 "../modules/agent_team_setup_service.md"
    click n12 "../modules/agent_team_setup_service.md"
    click n13 "../modules/agent_team_setup_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup_service](../modules/agent_team_setup_service.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentConflictError` | [agent_service](../modules/agent_service.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `AgentTeamSetupService._apply_create_or_update` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 4 |
| `AgentTeamSetupService._apply_disable` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 2 |
| `AgentTeamSetupService._apply_identity_replacement` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 4 |
| `AgentTeamSetupService._apply_replace_recovery` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 2 |
| `AgentTeamSetupService._catalog_entries` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService._current_snapshot` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService._ensure_topology_for_apply` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 2 |
| `AgentTeamSetupService._execute_action` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 3 |
| `AgentTeamSetupService._increment_ack_attempt` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService._replay_apply` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |

> References: showing 12 of 22 logical references; 10 omitted by the 12-row generated summary limit.
