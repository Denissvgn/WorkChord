# IterationSummary

**Location:** `backend/app/schemas/iteration.py:94`
**Kind:** Class
**Bases:** `WorkMetricSummary`
**Module:** [schemas_iteration](../modules/schemas_iteration.md)

## Description

Summary statistics for an iteration.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `int` | *required* | — |
| `name` | `str` | *required* | — |
| `project_id` | `Optional[int]` | `None` | — |
| `project` | `Optional[IterationProjectSummary]` | `None` | — |
| `start_date` | `date` | *required* | — |
| `end_date` | `date` | *required* | — |
| `working_days` | `int` | *required* | — |
| `total_tasks` | `int` | *required* | — |
| `completed_tasks` | `int` | *required* | — |
| `total_effort_days` | `float` | *required* | — |
| `team_capacity_days` | `float` | *required* | — |
| `overdue_tasks_count` | `int` | *required* | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationSummary (backend/app/schemas/iteration.py)"]
    n1["WorkMetricSummary (backend/app/schemas/work_metrics.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["get_iteration_summary (backend/app/routers/iterations.py)"]
    n4["backend/app/schemas/__init__.py"]
    n5["IterationService.get_summary (backend/app/services/iteration_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_iteration.md"
    click n1 "../modules/schemas_work_metrics.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/iterations.md"
    click n4 "../modules/schemas___init__.md"
    click n5 "../modules/iteration_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_iteration](../modules/schemas_iteration.md) | 0 | `completed_tasks`, `end_date`, `id`, `name`, `overdue_tasks_count`, `project`, `project_id`, `start_date`, `team_capacity_days`, `total_effort_days`, `total_tasks`, `working_days` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `WorkMetricSummary` | [schemas_work_metrics](../modules/schemas_work_metrics.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `get_iteration_summary` | type_reference | [iterations](../modules/iterations.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `IterationService.get_summary` | call | [iteration_service](../modules/iteration_service.md) | 1 |
| `IterationService.get_summary` | type_reference | [iteration_service](../modules/iteration_service.md) | — |
