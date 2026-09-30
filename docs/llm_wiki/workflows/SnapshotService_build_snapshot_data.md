# SnapshotService_build_snapshot_data

**Entry point:** `snapshot_service.SnapshotService.build_snapshot_data`
**Modules involved:** [iteration_service](../modules/iteration_service.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md), [team_service](../modules/team_service.md), [time](../modules/time.md)

> Build one JSON-native immutable representation of an iteration.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `task_service.TaskService`
3. `team_service.TeamService`
4. `time.utc_now`

## Touches

- [iteration_service](../modules/iteration_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `snapshot_service.SnapshotService.build_snapshot_data`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
