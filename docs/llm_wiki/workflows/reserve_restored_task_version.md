# reserve_restored_task_version

**Entry point:** `task_recovery_service.reserve_restored_task_version`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [task_recovery_service](../modules/task_recovery_service.md), [task_service](../modules/task_service.md)

> Restore strictly above every retained fence inside the scope's locked command.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.current_command`
2. `authority.internal_authority`
3. `authority.AuthorityError`
4. `task_service.TaskService`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [task_recovery_service](../modules/task_recovery_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_recovery_service.reserve_restored_task_version`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

Scheduled and backlog restoration share a version allocator under the owning scope lock. It advances above the saved version, live task, retained history and durable deletion fence. Current progress and acceptance are cleared; immutable history survives. A deleted task without a reliable deletion fence returns snapshot_version_history_unknown (409), requiring recovery from a complete matching database backup.
