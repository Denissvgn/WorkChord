# TriageActionRequest

**Location:** `backend/app/schemas/triage.py:106`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_triage](../modules/schemas_triage.md)

## Description

Request for simple triage status actions.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `reason` | `Optional[str]` | `reason` | No | Yes | `None` | max_length=500 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageActionRequest (backend/app/schemas/triage.py)"]
    n1["BaseModel"]
    n2["accept_triage_item (backend/app/mcp_agent_tools.py)"]
    n3["decline_triage_item (backend/app/mcp_agent_tools.py)"]
    n4["accept_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n5["decline_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n6["accept_triage_item (backend/app/routers/triage.py)"]
    n7["decline_triage_item (backend/app/routers/triage.py)"]
    n8["backend/app/schemas/__init__.py"]
    n9["TriageService.accept (backend/app/services/triage_service.py)"]
    n10["TriageService.decline (backend/app/services/triage_service.py)"]
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
    click n0 "../modules/schemas_triage.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/routers_agent_planning.md"
    click n6 "../modules/routers_triage.md"
    click n7 "../modules/routers_triage.md"
    click n8 "../modules/schemas___init__.md"
    click n9 "../modules/triage_service.md"
    click n10 "../modules/triage_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_triage](../modules/schemas_triage.md) | 0 | `reason` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `accept_triage_item` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `decline_triage_item` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `accept_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `decline_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `accept_triage_item` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `decline_triage_item` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `TriageService.accept` | type_reference | [triage_service](../modules/triage_service.md) | — |
| `TriageService.decline` | type_reference | [triage_service](../modules/triage_service.md) | — |
