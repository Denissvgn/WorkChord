# AgentService_get_pipeline

**Entry point:** `agent_service.AgentService.get_pipeline`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [authority](../modules/authority.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [query_limits](../modules/query_limits.md), [time](../modules/time.md)

> Fetch and segment all tasks in the agent pipeline columns.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `query_limits.CollectionLimitExceededError`
3. `agent_work_service.AgentWorkService`
4. `authority.internal_authority`
5. `delivery_dependency_service.DeliveryDependencyService.holds`
6. `delivery_dependency_service.DeliveryDependencyService`
7. `agent_work_service.AgentWorkService._start_blockers`
8. `time.as_utc`
9. `agent_work_service.AgentWorkService._pending_recovery_signal`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [authority](../modules/authority.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [query_limits](../modules/query_limits.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_service.AgentService.get_pipeline`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
