# ExecutionUsageService_write

**Entry point:** `execution_usage_service.ExecutionUsageService.write`
**Modules involved:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [execution_usage_service](../modules/execution_usage_service.md), [identity_service](../modules/identity_service.md), [models_execution_usage](../modules/models_execution_usage.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `agent_service.AgentPermissionError`
3. `identity_service.IdentityService`
4. `agent_service.AgentConflictError`
5. `agent_service.AgentConflictError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `time.utc_now`
9. `time.as_utc`
10. `time.as_utc`
11. `time.as_utc`
12. `time.as_utc`
13. `time.as_utc`
14. `models_execution_usage.ExecutionUsageRecord`

## Touches

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [execution_usage_service](../modules/execution_usage_service.md)
- [identity_service](../modules/identity_service.md)
- [models_execution_usage](../modules/models_execution_usage.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `execution_usage_service.ExecutionUsageService.write`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
