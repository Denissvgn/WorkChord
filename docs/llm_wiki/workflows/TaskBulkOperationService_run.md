# TaskBulkOperationService_run

**Entry point:** `task_bulk_operation_service.TaskBulkOperationService.run`
**Modules involved:** [commands](../modules/commands.md), [language_service](../modules/language_service.md), [schemas_task](../modules/schemas_task.md), [task_bulk_operation_service](../modules/task_bulk_operation_service.md)

> Run or preview one bulk operation for selected tasks.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `language_service.resolve_runtime_ui_language`
2. `language_service.localized`
3. `language_service.localized`
4. `commands.lock_iterations`
5. `schemas_task.TaskBulkOperationResult`
6. `language_service.localized`
7. `schemas_task.TaskBulkOperationResult`
8. `language_service.localized`
9. `schemas_task.TaskBulkOperationResult`
10. `language_service.backend_error_message`
11. `schemas_task.TaskBulkOperationResponse`

## Touches

- [commands](../modules/commands.md)
- [language_service](../modules/language_service.md)
- [schemas_task](../modules/schemas_task.md)
- [task_bulk_operation_service](../modules/task_bulk_operation_service.md)

## Behavior

This workflow starts at `task_bulk_operation_service.TaskBulkOperationService.run`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
