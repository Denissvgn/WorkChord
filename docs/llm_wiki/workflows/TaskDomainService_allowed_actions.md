# TaskDomainService_allowed_actions

**Entry point:** `task_domain_service.TaskDomainService.allowed_actions`
**Modules involved:** [agent_work_service](../modules/agent_work_service.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [schemas_task_domain](../modules/schemas_task_domain.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `delivery_dependency_service.DeliveryDependencyService.ready`
2. `delivery_dependency_service.DeliveryDependencyService`
3. `task_brief_service.TaskBriefService.require_review`
4. `task_brief_service.TaskBriefService`
5. `agent_work_service.AgentWorkService._start_blockers`
6. `agent_work_service.AgentWorkService`
7. `time.utc_now`
8. `time.as_utc`
9. `time.as_utc`
10. `time.utc_now`
11. `task_brief_service.TaskBriefService.require_review`
12. `task_brief_service.TaskBriefService`
13. `schemas_task_domain.TaskActionsResponse`

## Touches

- [agent_work_service](../modules/agent_work_service.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [schemas_task_domain](../modules/schemas_task_domain.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_domain_service.TaskDomainService.allowed_actions`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
