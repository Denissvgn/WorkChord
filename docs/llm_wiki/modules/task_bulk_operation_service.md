# task_bulk_operation_service Module

**Path:** `backend/app/services/task_bulk_operation_service.py`

## Description

Selected-task bulk operation orchestration.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task`, `TaskStatus` |
| `app.schemas.task` | `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskBulkOperationResult`, `TaskResponse`, `TaskUpdate` |
| `app.schemas.team` | `AssigneeRecommendationResponse` |
| `app.services.assignee_recommendation_service` | `AssigneeRecommendationService` |
| `app.services.language_service` | `backend_error_message`, `incomplete_dependency_message`, `invalid_status_transition_message`, `localized`, `resolve_runtime_ui_language`, `task_requires_schedule_message` |
| `app.services.task_service` | `TaskService` |
| `fastapi` | `HTTPException`, `status` |
| `json` | `json` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/iteration.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/routers/tasks.py"]
    n3["backend/app/schemas/task.py"]
    n4["backend/app/schemas/team.py"]
    n5["backend/app/services/assignee_recommendation_service.py"]
    n6["backend/app/services/language_service.py"]
    n7["backend/app/services/task_bulk_operation_service.py"]
    n8["backend/app/services/task_service.py"]
    n0 --> n1
    n1 --> n0
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n3 --> n4
    n5 --> n1
    n5 --> n4
    n7 --> n0
    n7 --> n1
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n8 --> n0
    n8 --> n1
    n8 --> n3
    n8 --> n6
    click n0 "../modules/models_iteration.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/schemas_task.md"
    click n4 "../modules/schemas_team.md"
    click n5 "../modules/assignee_recommendation_service.md"
    click n6 "../modules/language_service.md"
    click n7 "../modules/task_bulk_operation_service.md"
    click n8 "../modules/task_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [tasks](../modules/tasks.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [schemas_team](../modules/schemas_team.md) |
| Outbound | [assignee_recommendation_service](../modules/assignee_recommendation_service.md) |
| Outbound | [language_service](../modules/language_service.md) |
| Outbound | [task_service](../modules/task_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskBulkOperationService](../entities/TaskBulkOperationService.md) | 31 | — | Validate, preview, and apply selected-task bulk operations. |
