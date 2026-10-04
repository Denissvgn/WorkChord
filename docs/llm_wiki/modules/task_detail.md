# task_detail Module

**Path:** `backend/app/schemas/task_detail.py`

## Description

Bounded UI projections with explicit completeness and deterministic cursors.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.task` | `TaskResponse` |
| `app.schemas.task_domain` | `TaskActionAvailability` |
| `datetime` | `datetime` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/task_domain.py"]
    n1["backend/app/schemas/task.py"]
    n2["backend/app/schemas/task_detail.py"]
    n3["backend/app/schemas/task_domain.py"]
    n4["backend/app/services/task_detail_service.py"]
    n5["scripts/generate_mobile_contract_fixtures.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n2 --> n1
    n2 --> n3
    n4 --> n1
    n4 --> n2
    n5 --> n1
    n5 --> n2
    n5 --> n3
    click n0 "../modules/routers_task_domain.md"
    click n1 "../modules/schemas_task.md"
    click n2 "../modules/task_detail.md"
    click n3 "../modules/schemas_task_domain.md"
    click n4 "../modules/task_detail_service.md"
    click n5 "../modules/generate_mobile_contract_fixtures.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [task_detail_service](../modules/task_detail_service.md) |
| Inbound | [generate_mobile_contract_fixtures](../modules/generate_mobile_contract_fixtures.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [schemas_task_domain](../modules/schemas_task_domain.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskReference](../entities/task_detail_TaskReference.md) | 9 | `BaseModel` | — |
| [TaskReferencePage](../entities/task_detail_TaskReferencePage.md) | 26 | `BaseModel` | — |
| [TaskDetailResponse](../entities/TaskDetailResponse.md) | 34 | `BaseModel` | — |
| [HumanWorkReference](../entities/HumanWorkReference.md) | 43 | `TaskReference` | — |
| [HumanWorkResponse](../entities/HumanWorkResponse.md) | 47 | `BaseModel` | — |
