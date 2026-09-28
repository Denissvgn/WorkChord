# TaskDomainService_allowed_actions

**Entry point:** `task_domain_service.TaskDomainService.allowed_actions`
**Modules involved:** [agent_work_service](../modules/agent_work_service.md), [schemas_task_domain](../modules/schemas_task_domain.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_brief_service.TaskBriefService`
2. `agent_work_service.AgentWorkService`
3. `time.utc_now`
4. `time.as_utc`
5. `time.as_utc`
6. `time.utc_now`
7. `task_brief_service.TaskBriefService`
8. `schemas_task_domain.TaskActionsResponse`

## Touches

- [agent_work_service](../modules/agent_work_service.md)
- [schemas_task_domain](../modules/schemas_task_domain.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_domain_service.TaskDomainService.allowed_actions`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
