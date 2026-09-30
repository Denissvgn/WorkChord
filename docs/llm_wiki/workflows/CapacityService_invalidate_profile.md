# CapacityService_invalidate_profile

**Entry point:** `capacity_service.CapacityService.invalidate_profile`
**Modules involved:** [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Update private derived revisions without exposing or rewriting their planning content.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `commands.lock_iterations`
3. `snapshot_service.SnapshotService`
4. `task_service.TaskService`

## Touches

- [authority](../modules/authority.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `capacity_service.CapacityService.invalidate_profile`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
