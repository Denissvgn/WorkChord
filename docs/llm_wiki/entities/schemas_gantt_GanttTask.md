# GanttTask

**Location:** `backend/app/schemas/gantt.py:28`
**Kind:** Class
**Bases:** `TaskMetricSignals`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

Task representation for Gantt chart.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `int` | *required* | — |
| `title` | `str` | *required* | — |
| `project_id` | `Optional[int]` | `None` | — |
| `milestone_id` | `Optional[int]` | `None` | — |
| `start_date` | `Optional[date]` | *required* | — |
| `end_date` | `Optional[date]` | *required* | — |
| `actual_start_date` | `Optional[date]` | `None` | — |
| `actual_end_date` | `Optional[date]` | `None` | — |
| `min_start_date` | `Optional[date]` | `None` | — |
| `max_end_date` | `Optional[date]` | `None` | — |
| `status` | `Optional[str]` | `None` | — |
| `milestone` | `Optional[GanttMilestone]` | `None` | — |
| `assignee` | `Optional[GanttAssignee]` | `None` | — |
| `assignees` | `list[GanttAssignee]` | `[]` | — |
| `priority` | `int` | *required* | — |
| `progress` | `float` | `0.0` | — |
| `effort_days` | `Optional[float]` | *required* | — |
| `calculated_effort_days` | `Optional[float]` | `None` | — |
| `effort_hours` | `Optional[float]` | *required* | — |
| `version` | `int` | `1` | — |
| `is_overdue` | `bool` | `False` | — |
| `is_delayed` | `bool` | `False` | — |
| `tags` | `list[str]` | `[]` | — |
| `is_composite` | `bool` | `False` | — |
| `is_optional` | `bool` | `False` | — |
| `is_outside_constraints` | `bool` | `False` | — |
| `children` | `list['GanttTask']` | `[]` | — |
| `dependencies` | `list[int]` | `[]` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GanttTask (backend/app/schemas/gantt.py)"]
    n1["TaskMetricSignals (backend/app/schemas/work_metrics.py)"]
    n2["_task_to_gantt (backend/app/routers/gantt.py)"]
    n3["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n1 "../modules/schemas_work_metrics.md"
    click n2 "../modules/routers_gantt.md"
    click n3 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `actual_end_date`, `actual_start_date`, `assignee`, `assignees`, `calculated_effort_days`, `children`, `dependencies`, `effort_days`, `effort_hours`, `end_date`, `id`, `is_composite` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `TaskMetricSignals` | [schemas_work_metrics](../modules/schemas_work_metrics.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_task_to_gantt` | call | [routers_gantt](../modules/routers_gantt.md) | 1 |
| `_task_to_gantt` | type_reference | [routers_gantt](../modules/routers_gantt.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
