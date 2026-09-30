# TriageConvertToBacklogRequest

**Location:** `backend/app/schemas/triage.py:294`
**Kind:** Pydantic model
**Bases:** `TriageConvertToTaskRequest`
**Module:** [schemas_triage](../modules/schemas_triage.md)

## Description

Explicit project backlog destination; the legacy iteration contract stays required.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `project_id` | `int` | `project_id` | Yes | No | — | ge=1 | — | — |
| `iteration_id` | `None` | `iteration_id` | No | Yes | `None` | — | — | — |
| `destination` | `Literal['project_backlog']` | `destination` | No | No | `'project_backlog'` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageConvertToBacklogRequest (backend/app/schemas/triage.py)"]
    n1["TriageConvertToTaskRequest (backend/app/schemas/triage.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["convert_triage_item_to_backlog (backend/app/routers/triage.py)"]
    n4["test_triage_handoff_preserves_canonical_fields_and_criterion_ids (backend/tests/test_task_domain.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_triage.md"
    click n1 "../modules/schemas_triage.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_triage.md"
    click n4 "../modules/test_task_domain.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_triage](../modules/schemas_triage.md) | 0 | `destination`, `iteration_id`, `project_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `TriageConvertToTaskRequest` | [schemas_triage](../modules/schemas_triage.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `convert_triage_item_to_backlog` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `test_triage_handoff_preserves_canonical_fields_and_criterion_ids` | call | [test_task_domain](../modules/test_task_domain.md) | 1 |
