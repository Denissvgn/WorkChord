# AgentWorkService_list_recovery_tasks

**Entry point:** `agent_work_service.AgentWorkService.list_recovery_tasks`
**Modules involved:** [agent_work_service](../modules/agent_work_service.md), [execution_planning_window](../modules/execution_planning_window.md), [schemas_agent](../modules/schemas_agent.md), [time](../modules/time.md)

> Return typed active/resolved recovery diagnoses and ownership tuples.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `time.as_utc`
3. `time.as_utc`
4. `execution_planning_window.window_authority_matches`
5. `execution_planning_window.window_authority_matches`
6. `schemas_agent.AgentRecoveryItem`
7. `schemas_agent.AgentRecoveryListResponse`

## Touches

- [agent_work_service](../modules/agent_work_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [schemas_agent](../modules/schemas_agent.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.list_recovery_tasks`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
