# TaskDomainService_allowed_actions

**Entry point:** `task_domain_service.TaskDomainService.allowed_actions`
**Modules involved:** [agent_work_service](../modules/agent_work_service.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [schemas_task_domain](../modules/schemas_task_domain.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [task_postponement_service](../modules/task_postponement_service.md), [task_replacement_service](../modules/task_replacement_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `delivery_dependency_service.DeliveryDependencyService.ready`
2. `delivery_dependency_service.DeliveryDependencyService`
3. `task_replacement_service.replaced_by`
4. `task_replacement_service.replacing`
5. `task_brief_service.TaskBriefService.require_review`
6. `task_brief_service.TaskBriefService`
7. `task_postponement_service.postponement_actions`
8. `agent_work_service.AgentWorkService._start_blockers`
9. `agent_work_service.AgentWorkService`
10. `time.utc_now`
11. `time.as_utc`
12. `time.as_utc`
13. `time.utc_now`
14. `task_brief_service.TaskBriefService.require_review`
15. `task_brief_service.TaskBriefService`
16. `schemas_task_domain.TaskActionsResponse`

## Touches

- [agent_work_service](../modules/agent_work_service.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [schemas_task_domain](../modules/schemas_task_domain.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_postponement_service](../modules/task_postponement_service.md)
- [task_replacement_service](../modules/task_replacement_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_domain_service.TaskDomainService.allowed_actions`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
