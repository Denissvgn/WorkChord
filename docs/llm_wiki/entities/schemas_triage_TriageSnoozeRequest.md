# TriageSnoozeRequest

**Location:** `backend/app/schemas/triage.py:111`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_triage](../modules/schemas_triage.md)

## Description

Request for snoozing a triage item.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `snoozed_until` | `datetime` | `snoozed_until` | Yes | No | — | — | — | — |
| `reason` | `Optional[str]` | `reason` | No | Yes | `None` | max_length=500 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageSnoozeRequest (backend/app/schemas/triage.py)"]
    n1["BaseModel"]
    n2["snooze_triage_item (backend/app/mcp_agent_tools.py)"]
    n3["snooze_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n4["snooze_triage_item (backend/app/routers/triage.py)"]
    n5["backend/app/schemas/__init__.py"]
    n6["TriageService.snooze (backend/app/services/triage_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_triage.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/routers_triage.md"
    click n5 "../modules/schemas___init__.md"
    click n6 "../modules/triage_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_triage](../modules/schemas_triage.md) | 0 | `reason`, `snoozed_until` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `snooze_triage_item` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `snooze_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `snooze_triage_item` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `TriageService.snooze` | type_reference | [triage_service](../modules/triage_service.md) | — |
