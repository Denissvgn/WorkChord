# TriageConflictError

**Location:** `backend/app/services/triage_service.py:44`
**Kind:** Class
**Bases:** `Exception`
**Module:** [triage_service](../modules/triage_service.md)

## Description

Raised when a triage action conflicts with current item state.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageConflictError (backend/app/services/triage_service.py)"]
    n1["Exception"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["backend/app/mcp_server.py"]
    n4["backend/app/routers/agent_planning.py"]
    n5["backend/app/routers/triage.py"]
    n6["TriageService.convert_to_task (backend/app/services/triage_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/triage_service.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/mcp_server.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/routers_triage.md"
    click n6 "../modules/triage_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [triage_service](../modules/triage_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Exception` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `agent_planning` | import | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `triage` | import | [routers_triage](../modules/routers_triage.md) | — |
| `TriageService.convert_to_task` | call | [triage_service](../modules/triage_service.md) | 2 |
