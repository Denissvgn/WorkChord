# task_detail Module

**Path:** `backend/app/schemas/task_detail.py`

## Description

Bounded UI projections with explicit completeness and deterministic cursors.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.task` | `TaskResponse` |
| `datetime` | `datetime` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/task_domain.py"]
    n1["backend/app/schemas/task.py"]
    n2["backend/app/schemas/task_detail.py"]
    n3["backend/app/services/task_detail_service.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n3 --> n1
    n3 --> n2
    click n0 "../modules/routers_task_domain.md"
    click n1 "../modules/schemas_task.md"
    click n2 "../modules/task_detail.md"
    click n3 "../modules/task_detail_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [task_detail_service](../modules/task_detail_service.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskReference](../entities/task_detail_TaskReference.md) | 8 | `BaseModel` | — |
| [TaskReferencePage](../entities/task_detail_TaskReferencePage.md) | 25 | `BaseModel` | — |
| [TaskDetailResponse](../entities/TaskDetailResponse.md) | 33 | `BaseModel` | — |
