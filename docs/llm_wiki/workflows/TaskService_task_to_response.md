# TaskService_task_to_response

**Entry point:** `task_service.TaskService.task_to_response`
**Modules involved:** [agent_readiness](../modules/agent_readiness.md), [external_link_service](../modules/external_link_service.md), [schemas_task](../modules/schemas_task.md), [task_service](../modules/task_service.md)

> Convert Task model to TaskResponse schema.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_task.TaskAssignee`
2. `schemas_task.TaskProject`
3. `schemas_task.TaskMilestone`
4. `schemas_task.TaskClaimedBy`
5. `agent_readiness.evaluate_agent_readiness`
6. `schemas_task.TaskResponse`
7. `external_link_service.ExternalLinkService`

## Touches

- [agent_readiness](../modules/agent_readiness.md)
- [external_link_service](../modules/external_link_service.md)
- [schemas_task](../modules/schemas_task.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.task_to_response`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
