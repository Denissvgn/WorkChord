# SnapshotService_create_snapshot

**Entry point:** `snapshot_service.SnapshotService.create_snapshot`
**Modules involved:** [commands](../modules/commands.md), [recovery](../modules/recovery.md), [snapshot_service](../modules/snapshot_service.md), [time](../modules/time.md)

> Persist one pre-command recovery point and retention in the owner's transaction.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.current_command`
2. `commands.lock_iterations`
3. `time.utc_now`
4. `recovery.ApplicationSnapshot`

## Touches

- [commands](../modules/commands.md)
- [recovery](../modules/recovery.md)
- [snapshot_service](../modules/snapshot_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `snapshot_service.SnapshotService.create_snapshot`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
