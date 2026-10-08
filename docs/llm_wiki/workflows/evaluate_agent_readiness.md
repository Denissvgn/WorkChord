# evaluate_agent_readiness

**Entry point:** `agent_readiness.evaluate_agent_readiness`
**Modules involved:** [agent_readiness](../modules/agent_readiness.md), [schemas_task](../modules/schemas_task.md), [services_work_metrics](../modules/services_work_metrics.md), [task_brief_service](../modules/task_brief_service.md), [time](../modules/time.md)

> Evaluate whether a task is ready for explicit agent execution.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `services_work_metrics.effective_work_flags`
3. `time.as_utc`
4. `time.as_utc`
5. `task_brief_service.brief_definition_blockers`
6. `schemas_task.TaskAgentReadiness`

## Touches

- [agent_readiness](../modules/agent_readiness.md)
- [schemas_task](../modules/schemas_task.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_readiness.evaluate_agent_readiness`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
