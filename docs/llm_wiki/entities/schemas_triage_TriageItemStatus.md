# TriageItemStatus

**Location:** `backend/app/schemas/triage.py:11`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_triage](../modules/schemas_triage.md)

## Description

Triage item lifecycle status.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `NEW` | `'new'` | — |
| `ACCEPTED` | `'accepted'` | — |
| `DECLINED` | `'declined'` | — |
| `DUPLICATE` | `'duplicate'` | — |
| `SNOOZED` | `'snoozed'` | — |
| `CONVERTED` | `'converted'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageItemStatus (backend/app/schemas/triage.py)"]
    n1["Enum"]
    n2["str"]
    n3["list_triage_items (backend/app/mcp_agent_tools.py)"]
    n4["list_triage_items (backend/app/routers/triage.py)"]
    n5["backend/app/schemas/__init__.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_triage.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/routers_triage.md"
    click n5 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_triage](../modules/schemas_triage.md) | 0 | `ACCEPTED`, `CONVERTED`, `DECLINED`, `DUPLICATE`, `NEW`, `SNOOZED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `list_triage_items` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `list_triage_items` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
