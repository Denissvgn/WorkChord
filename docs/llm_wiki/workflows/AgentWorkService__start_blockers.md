# AgentWorkService__start_blockers

**Entry point:** `agent_work_service.AgentWorkService._start_blockers`
**Modules involved:** [agent_work_service](../modules/agent_work_service.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [services_work_metrics](../modules/services_work_metrics.md), [task_brief_service](../modules/task_brief_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.as_utc`
2. `time.as_utc`
3. `services_work_metrics.effective_work_flags`
4. `services_work_metrics.working_today`
5. `delivery_dependency_service.DeliveryDependencyService`
6. `time.as_utc`
7. `time.as_utc`
8. `task_brief_service.brief_definition_blockers`

## Touches

- [agent_work_service](../modules/agent_work_service.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService._start_blockers`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
