# TaskDetailService_my_work

**Entry point:** `task_detail_service.TaskDetailService.my_work`
**Modules involved:** [authority](../modules/authority.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [task_detail_service](../modules/task_detail_service.md), [task_domain_service](../modules/task_domain_service.md)

> Bounded human ownership queues, independent of exact-agent assignment decisions.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `task_domain_service.TaskDomainService`
3. `delivery_dependency_service.DeliveryDependencyService`

## Touches

- [authority](../modules/authority.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [task_detail_service](../modules/task_detail_service.md)
- [task_domain_service](../modules/task_domain_service.md)

## Behavior

Builds a permission-scoped leaf-work query for the authenticated human owner, applies requested project/iteration/backlog scope, and reads a bounded live page. Action availability and delivery prerequisites classify each row into active, queued, blocked or awaiting-review work. Closed tasks lacking current attributed acceptance stay visible for reconciliation.
