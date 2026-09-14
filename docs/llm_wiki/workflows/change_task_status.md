# change_task_status

**Entry point:** `tasks.change_task_status`
**Modules involved:** [iteration_service](../modules/iteration_service.md), [language_service](../modules/language_service.md), [schemas_task](../modules/schemas_task.md), [tasks](../modules/tasks.md)

> Change task status with validation and side effects.

Valid transitions:
- planned -> active: Sets actual_start_date, recalculates end_date if late
- active -> resolved: Work completed, pending validation
- resolved -> active: Return for rework
- resolved -> closed: Full completion, sets actual_end_date

Cascade updates: When dates shift, dependent tasks are automatically updated.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `language_service.resolve_runtime_ui_language`
2. `language_service.invalid_status_transition_message`
3. `iteration_service.IterationService`
4. `schemas_task.TaskStatusChangeResponse`
5. `schemas_task.CascadeUpdateInfo`

## Touches

- [iteration_service](../modules/iteration_service.md)
- [language_service](../modules/language_service.md)
- [schemas_task](../modules/schemas_task.md)
- [tasks](../modules/tasks.md)

## Behavior

This workflow starts at `tasks.change_task_status`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
