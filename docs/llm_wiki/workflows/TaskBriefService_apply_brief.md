# TaskBriefService_apply_brief

**Entry point:** `task_brief_service.TaskBriefService.apply_brief`
**Modules involved:** [authority](../modules/authority.md), [models_task_brief](../modules/models_task_brief.md), [task_brief_service](../modules/task_brief_service.md), [task_routing_service](../modules/task_routing_service.md)

> Apply one canonical representation under the task command's existing fence.

A changed routing is filled from the model catalog and, unless the caller checks it
after its own changes (enforce=False), checked against the task's assignee.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `task_routing_service.resolve_routing`
3. `task_routing_service.enforce_routing`
4. `models_task_brief.TaskBriefRevision`
5. `task_routing_service.enforce_routing`

## Touches

- [authority](../modules/authority.md)
- [models_task_brief](../modules/models_task_brief.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_routing_service](../modules/task_routing_service.md)

## Behavior

This workflow starts at `task_brief_service.TaskBriefService.apply_brief`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
