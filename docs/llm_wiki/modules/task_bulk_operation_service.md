# task_bulk_operation_service Module

**Path:** `backend/app/services/task_bulk_operation_service.py`

## Description

Selected-task bulk operation orchestration.

Bulk preview returns original task and iteration revisions. Apply validates those observations before modifying selected work, and any failed item rejects the whole command. Preview defaults are preserved by the request transaction owner; supplied stale revisions cannot be retried as an unchanged plan.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `atomic_command`, `lock_iterations` |
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
    n0["backend/app/commands.py"]
    n1["backend/app/models/iteration.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/routers/tasks.py"]
    n4["backend/app/schemas/task.py"]
    n5["backend/app/schemas/team.py"]
    n6["backend/app/services/assignee_recommendation_service.py"]
    n7["backend/app/services/language_service.py"]
    n8["backend/app/services/task_bulk_operation_service.py"]
    n9["backend/app/services/task_service.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n9
    n1 --> n2
    n2 --> n1
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n4 --> n5
    n6 --> n2
    n6 --> n5
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n4
    n8 --> n5
    n8 --> n6
    n8 --> n7
    n8 --> n9
    n9 --> n0
    n9 --> n1
    n9 --> n2
    n9 --> n4
    n9 --> n7
    click n0 "../modules/commands.md"
    click n1 "../modules/models_iteration.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/tasks.md"
    click n4 "../modules/schemas_task.md"
    click n5 "../modules/schemas_team.md"
    click n6 "../modules/assignee_recommendation_service.md"
    click n7 "../modules/language_service.md"
    click n8 "../modules/task_bulk_operation_service.md"
    click n9 "../modules/task_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [tasks](../modules/tasks.md) |
| Outbound | [commands](../modules/commands.md) |
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
| [TaskBulkOperationService](../entities/TaskBulkOperationService.md) | 33 | — | Validate, preview, and apply selected-task bulk operations. |