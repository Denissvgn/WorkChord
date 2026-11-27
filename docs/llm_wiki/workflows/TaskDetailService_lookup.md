# TaskDetailService_lookup

**Entry point:** `task_detail_service.TaskDetailService.lookup`
**Modules involved:** [authority](../modules/authority.md), [sql_semantics](../modules/sql_semantics.md), [task_detail_service](../modules/task_detail_service.md), [task_display_state](../modules/task_display_state.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `task_display_state.task_state_clause`
3. `task_display_state.validate_state_filter`
4. `authority.require_project`
5. `sql_semantics.portable_contains`

## Touches

- [authority](../modules/authority.md)
- [sql_semantics](../modules/sql_semantics.md)
- [task_detail_service](../modules/task_detail_service.md)
- [task_display_state](../modules/task_display_state.md)

## Behavior

This workflow starts at `task_detail_service.TaskDetailService.lookup`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
