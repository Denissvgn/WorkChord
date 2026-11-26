# TriageConvertToTaskResponse

**Location:** `backend/app/schemas/triage.py:322`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_triage](../modules/schemas_triage.md)

## Description

Response for triage item conversion.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `triage_item` | `TriageItemResponse` | `triage_item` | Yes | No | — | — | — | — |
| `task` | `TaskResponse` | `task` | Yes | No | — | — | — | — |
| `source_link` | `Optional[TriageSourceLinkOutcome]` | `source_link` | No | Yes | `None` | — | — | Set when the source link was rewritten to a relative path or dropped; absent when there was no link or it was kept as a normal link. |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageConvertToTaskResponse (backend/app/schemas/triage.py)"]
    n1["BaseModel"]
    n2["convert_triage_to_backlog (backend/app/mcp_agent_tools.py)"]
    n3["convert_triage_to_task (backend/app/mcp_agent_tools.py)"]
    n4["convert_planning_triage_item_to_task (backend/app/routers/agent_planning.py)"]
    n5["convert_triage_item_to_backlog (backend/app/routers/triage.py)"]
    n6["convert_triage_item_to_task (backend/app/routers/triage.py)"]
    n7["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_triage.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/routers_triage.md"
    click n6 "../modules/routers_triage.md"
    click n7 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_triage](../modules/schemas_triage.md) | 0 | `source_link`, `task`, `triage_item` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `convert_triage_to_backlog` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `convert_triage_to_task` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `convert_planning_triage_item_to_task` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `convert_triage_item_to_backlog` | call | [routers_triage](../modules/routers_triage.md) | 1 |
| `convert_triage_item_to_backlog` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `convert_triage_item_to_task` | call | [routers_triage](../modules/routers_triage.md) | 1 |
| `convert_triage_item_to_task` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
