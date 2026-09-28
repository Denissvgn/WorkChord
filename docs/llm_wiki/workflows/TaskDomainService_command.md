# TaskDomainService_command

**Entry point:** `task_domain_service.TaskDomainService.command`
**Modules involved:** [authority](../modules/authority.md), [snapshot_service](../modules/snapshot_service.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [task_status_log](../modules/task_status_log.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `snapshot_service.SnapshotService`
3. `time.utc_now`
4. `task_brief_service.clear_acceptance`
5. `task_brief_service.clear_acceptance`
6. `task_status_log.TaskStatusLog`

## Touches

- [authority](../modules/authority.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_status_log](../modules/task_status_log.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_domain_service.TaskDomainService.command`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
