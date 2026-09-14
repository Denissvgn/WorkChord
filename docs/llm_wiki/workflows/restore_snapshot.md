# restore_snapshot

**Entry point:** `snapshots.restore_snapshot`
**Modules involved:** [export](../modules/export.md), [iteration_service](../modules/iteration_service.md), [snapshot](../modules/snapshot.md), [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md), [task_service](../modules/task_service.md), [team_service](../modules/team_service.md)

> Restore iteration state from a snapshot.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `snapshot_service.SnapshotService`
3. `task_service.TaskService`
4. `team_service.TeamService`
5. `export._process_import`
6. `snapshot.SnapshotRestoreResponse`

## Touches

- [export](../modules/export.md)
- [iteration_service](../modules/iteration_service.md)
- [snapshot](../modules/snapshot.md)
- [snapshot_service](../modules/snapshot_service.md)
- [snapshots](../modules/snapshots.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `snapshots.restore_snapshot`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
