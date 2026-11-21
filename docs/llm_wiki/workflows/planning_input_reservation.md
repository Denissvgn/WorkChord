# planning_input_reservation

**Entry point:** `commands.planning_input_reservation`
**Modules involved:** [calendar_rules](../modules/calendar_rules.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [mutation_versions](../modules/mutation_versions.md), [planning_input_context](../modules/planning_input_context.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Validate one complete outer observation and bound nested input writes to it.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `planning_input_context.affected_iteration_ids`
2. `mutation_versions.require_mutation_revision`
3. `execution_planning_window.extension_input`
4. `snapshot_service.SnapshotService`
5. `calendar_rules.reserve_iteration_annuals`
6. `task_service.TaskService`
7. `execution_planning_window.live_assignments`
8. `execution_planning_window.task_context`
9. `execution_planning_window.current_window`
10. `task_service.TaskService.reserve_task_version`
11. `execution_planning_window.task_context`
12. `execution_planning_window.make_window`
13. `execution_planning_window.seal_authority`
14. `task_service.TaskService.record_task_event`

## Touches

- [calendar_rules](../modules/calendar_rules.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [mutation_versions](../modules/mutation_versions.md)
- [planning_input_context](../modules/planning_input_context.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `commands.planning_input_reservation`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
