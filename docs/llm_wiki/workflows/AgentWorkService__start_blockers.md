# AgentWorkService__start_blockers

**Entry point:** `agent_work_service.AgentWorkService._start_blockers`
**Modules involved:** [agent_work_service](../modules/agent_work_service.md), [authority](../modules/authority.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [review_provenance](../modules/review_provenance.md), [services_work_metrics](../modules/services_work_metrics.md), [task_brief_service](../modules/task_brief_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `review_provenance.ReworkReadCache`
2. `time.as_utc`
3. `time.as_utc`
4. `services_work_metrics.effective_work_flags`
5. `authority.internal_authority`
6. `delivery_dependency_service.DeliveryDependencyService.ready`
7. `delivery_dependency_service.DeliveryDependencyService`
8. `time.as_utc`
9. `time.as_utc`
10. `task_brief_service.brief_definition_blockers`

## Touches

- [agent_work_service](../modules/agent_work_service.md)
- [authority](../modules/authority.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [review_provenance](../modules/review_provenance.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService._start_blockers`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
