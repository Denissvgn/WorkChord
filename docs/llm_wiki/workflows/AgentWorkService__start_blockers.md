# AgentWorkService__start_blockers

**Entry point:** `agent_work_service.AgentWorkService._start_blockers`
**Modules involved:** [agent_work_service](../modules/agent_work_service.md), [authority](../modules/authority.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [execution_planning_window](../modules/execution_planning_window.md), [retained_planning_output](../modules/retained_planning_output.md), [review_provenance](../modules/review_provenance.md), [services_work_metrics](../modules/services_work_metrics.md), [task_brief_service](../modules/task_brief_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `execution_planning_window.window_authority_matches`
2. `review_provenance.ReworkReadCache`
3. `retained_planning_output.recovery_attestation_hint`
4. `time.as_utc`
5. `time.as_utc`
6. `services_work_metrics.effective_work_flags`
7. `authority.internal_authority`
8. `delivery_dependency_service.DeliveryDependencyService.holds`
9. `delivery_dependency_service.DeliveryDependencyService`
10. `time.as_utc`
11. `time.as_utc`
12. `task_brief_service.brief_definition_blockers`

## Touches

- [agent_work_service](../modules/agent_work_service.md)
- [authority](../modules/authority.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [retained_planning_output](../modules/retained_planning_output.md)
- [review_provenance](../modules/review_provenance.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService._start_blockers`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
