# metric_matches

**Entry point:** `task_domain.metric_matches`
**Modules involved:** [authority](../modules/authority.md), [release_service](../modules/release_service.md), [routers_task_domain](../modules/routers_task_domain.md), [services_work_metrics](../modules/services_work_metrics.md)

> The tasks behind one work-metric count, chosen by the predicate that counts them.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `release_service.ReleaseService`
2. `release_service.ReleaseService.get_by_id`
3. `release_service.ReleaseService.metric_task_ids`
4. `authority.require_project`
5. `services_work_metrics.aggregate_metrics`
6. `authority.require_project`
7. `services_work_metrics.aggregate_metrics`

## Touches

- [authority](../modules/authority.md)
- [release_service](../modules/release_service.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [services_work_metrics](../modules/services_work_metrics.md)

## Behavior

This workflow starts at `task_domain.metric_matches`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
