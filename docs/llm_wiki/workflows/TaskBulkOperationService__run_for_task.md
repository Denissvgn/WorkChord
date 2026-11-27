# TaskBulkOperationService__run_for_task

**Entry point:** `task_bulk_operation_service.TaskBulkOperationService._run_for_task`
**Modules involved:** [language_service](../modules/language_service.md), [schemas_task](../modules/schemas_task.md), [task_bulk_operation_service](../modules/task_bulk_operation_service.md), [task_routing_service](../modules/task_routing_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_task.TaskBulkOperationResult`
2. `language_service.localized`
3. `task_routing_service.RoutingConsistencyConflict`
4. `schemas_task.TaskBulkOperationResult`
5. `language_service.localized`
6. `language_service.invalid_status_transition_message`
7. `language_service.localized`
8. `schemas_task.TaskBulkOperationResult`
9. `task_routing_service.routing_check_for`

## Touches

- [language_service](../modules/language_service.md)
- [schemas_task](../modules/schemas_task.md)
- [task_bulk_operation_service](../modules/task_bulk_operation_service.md)
- [task_routing_service](../modules/task_routing_service.md)

## Behavior

This workflow starts at `task_bulk_operation_service.TaskBulkOperationService._run_for_task`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
