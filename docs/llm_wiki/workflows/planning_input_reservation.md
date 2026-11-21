# planning_input_reservation

**Entry point:** `commands.planning_input_reservation`
**Modules involved:** [allocation_removal](../modules/allocation_removal.md), [calendar_rules](../modules/calendar_rules.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [mutation_versions](../modules/mutation_versions.md), [planning_input_context](../modules/planning_input_context.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Validate one complete outer observation and bound nested input writes to it.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `planning_input_context.affected_iteration_ids`
2. `allocation_removal.inspect_allocation_history`
3. `planning_input_context.affected_iteration_ids`
4. `mutation_versions.require_mutation_revision`
5. `allocation_removal.is_unused_allocation`
6. `execution_planning_window.extension_input`
7. `snapshot_service.SnapshotService`
8. `calendar_rules.reserve_iteration_annuals`
9. `task_service.TaskService`
10. `execution_planning_window.live_assignments`
11. `execution_planning_window.task_context`
12. `execution_planning_window.current_window`
13. `task_service.TaskService.reserve_task_version`
14. `execution_planning_window.task_context`
15. `execution_planning_window.make_window`
16. `execution_planning_window.seal_authority`
17. `task_service.TaskService.record_task_event`

## Touches

- [allocation_removal](../modules/allocation_removal.md)
- [calendar_rules](../modules/calendar_rules.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [mutation_versions](../modules/mutation_versions.md)
- [planning_input_context](../modules/planning_input_context.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `commands.planning_input_reservation`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
