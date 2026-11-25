# IterationDateMoveRequest

**Location:** `backend/app/schemas/iteration.py:176`
**Kind:** Class
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_iteration](../modules/schemas_iteration.md)

## Description

A proposed iteration start, end and calendar to check against shared capacity.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_proposal` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `start_date` | `Optional[date]` | `start_date` | No | Yes | `None` | — | — | — |
| `end_date` | `Optional[date]` | `end_date` | No | Yes | `None` | — | — | — |
| `calendar_id` | `Optional[int]` | `calendar_id` | No | Yes | `None` | — | — | — |
| `additional_calendar_ids` | `list[int] \| None` | `additional_calendar_ids` | No | Yes | `None` | max_length=100 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_proposal` | `() -> 'IterationDateMoveRequest'` | `@model_validator(mode='after')` | — |
| `as_update` | `() -> IterationUpdate` | — | The iteration update that applies this proposal. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationDateMoveRequest (backend/app/schemas/iteration.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["preview_iteration_date_move (backend/app/routers/iterations.py)"]
    n4["IterationDateMoveRequest.validate_proposal (backend/app/schemas/iteration.py)"]
    n5["IterationDateMoveService.preview (backend/app/services/iteration_date_move.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_iteration.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/iterations.md"
    click n4 "../modules/schemas_iteration.md"
    click n5 "../modules/iteration_date_move.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_iteration](../modules/schemas_iteration.md) | 2 | `additional_calendar_ids`, `calendar_id`, `end_date`, `start_date` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningInputRevisions` | [planning_inputs](../modules/planning_inputs.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `preview_iteration_date_move` | type_reference | [iterations](../modules/iterations.md) | — |
| `IterationDateMoveRequest.validate_proposal` | type_reference | [schemas_iteration](../modules/schemas_iteration.md) | — |
| `IterationDateMoveService.preview` | type_reference | [iteration_date_move](../modules/iteration_date_move.md) | — |
