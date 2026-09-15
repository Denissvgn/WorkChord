# ProjectMilestoneTaskGroup

**Location:** `backend/app/schemas/project.py:256`
**Kind:** Pydantic model
**Bases:** `WorkMetricSummary`
**Module:** [schemas_project](../modules/schemas_project.md)

## Description

Task progress metrics grouped under one milestone or unassigned work.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `milestone_id` | `Optional[int]` | `milestone_id` | No | Yes | `None` | — | — | — |
| `milestone` | `Optional[ProjectMilestoneSummary]` | `milestone` | No | Yes | `None` | — | — | — |
| `name` | `str` | `name` | Yes | No | — | — | — | — |
| `task_count` | `int` | `task_count` | No | No | `0` | — | — | — |
| `completed_tasks` | `int` | `completed_tasks` | No | No | `0` | — | — | — |
| `completion_percent` | `float` | `completion_percent` | No | No | `0.0` | — | — | — |
| `status_counts` | `dict[str, int]` | `status_counts` | No | No | factory: `lambda: {'planned': 0, 'active': 0, 'resolved': 0, 'closed': 0}` | — | — | — |
| `total_effort_days` | `float` | `total_effort_days` | No | No | `0.0` | — | — | — |
| `remaining_effort_days` | `float` | `remaining_effort_days` | No | No | `0.0` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectMilestoneTaskGroup (backend/app/schemas/project.py)"]
    n1["WorkMetricSummary (backend/app/schemas/work_metrics.py)"]
    n2["backend/app/schemas/__init__.py"]
    n3["ProjectService._aggregated_milestone_groups (backend/app/services/project_service.py)"]
    n4["ProjectService._build_milestone_task_group (backend/app/services/project_service.py)"]
    n5["ProjectService._calculate_milestone_groups (backend/app/services/project_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_project.md"
    click n1 "../modules/schemas_work_metrics.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/project_service.md"
    click n4 "../modules/project_service.md"
    click n5 "../modules/project_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_project](../modules/schemas_project.md) | 0 | `completed_tasks`, `completion_percent`, `milestone`, `milestone_id`, `name`, `remaining_effort_days`, `status_counts`, `task_count`, `total_effort_days` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `WorkMetricSummary` | [schemas_work_metrics](../modules/schemas_work_metrics.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `ProjectService._aggregated_milestone_groups` | call | [project_service](../modules/project_service.md) | 1 |
| `ProjectService._aggregated_milestone_groups` | type_reference | [project_service](../modules/project_service.md) | — |
| `ProjectService._build_milestone_task_group` | call | [project_service](../modules/project_service.md) | 1 |
| `ProjectService._build_milestone_task_group` | type_reference | [project_service](../modules/project_service.md) | — |
| `ProjectService._calculate_milestone_groups` | type_reference | [project_service](../modules/project_service.md) | — |
