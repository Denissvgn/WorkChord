# work_metrics Module

**Path:** `backend/app/schemas/work_metrics.py`

## Description

Shared additive delivery metrics; legacy completed fields mean implemented work.

## Imports

| Source | Symbols |
|--------|---------|
| `pydantic` | `BaseModel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/schemas/gantt.py"]
    n1["backend/app/schemas/iteration.py"]
    n2["backend/app/schemas/project.py"]
    n3["backend/app/schemas/release.py"]
    n4["backend/app/schemas/task.py"]
    n5["backend/app/schemas/work_metrics.py"]
    n0 --> n1
    n0 --> n4
    n0 --> n5
    n1 --> n5
    n2 --> n5
    n3 --> n5
    n4 --> n5
    click n0 "../modules/schemas_gantt.md"
    click n1 "../modules/schemas_iteration.md"
    click n2 "../modules/schemas_project.md"
    click n3 "../modules/schemas_release.md"
    click n4 "../modules/schemas_task.md"
    click n5 "../modules/schemas_work_metrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [schemas_gantt](../modules/schemas_gantt.md) |
| Inbound | [schemas_iteration](../modules/schemas_iteration.md) |
| Inbound | [schemas_project](../modules/schemas_project.md) |
| Inbound | [schemas_release](../modules/schemas_release.md) |
| Inbound | [schemas_task](../modules/schemas_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [WorkMetricSummary](../entities/WorkMetricSummary.md) | 6 | `BaseModel` | — |
| [TaskMetricSignals](../entities/TaskMetricSignals.md) | 24 | `BaseModel` | — |
