# HierarchyRepairService_repair

**Entry point:** `hierarchy_repair_service.HierarchyRepairService.repair`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [hierarchy_repair_service](../modules/hierarchy_repair_service.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `commands.AggregateVersionConflict`
3. `commands.lock_iterations`
4. `task_service.TaskService`
5. `task_service.TaskVersionConflictError`
6. `snapshot_service.SnapshotService`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [hierarchy_repair_service](../modules/hierarchy_repair_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `hierarchy_repair_service.HierarchyRepairService.repair`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
