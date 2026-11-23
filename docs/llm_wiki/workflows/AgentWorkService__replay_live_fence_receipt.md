# AgentWorkService__replay_live_fence_receipt

**Entry point:** `agent_work_service.AgentWorkService._replay_live_fence_receipt`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [execution_planning_window](../modules/execution_planning_window.md), [time](../modules/time.md)

> Replay a fence receipt only while its original authority is still exact.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentConflictError`
2. `time.as_utc`
3. `agent_service.AgentConflictError`
4. `execution_planning_window.assignment_matches`
5. `time.as_utc`
6. `time.as_utc`
7. `time.utc_now`
8. `agent_service.AgentConflictError`
9. `execution_planning_window.require_window_authority`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService._replay_live_fence_receipt`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
