# AgentWorkService_get_reviews

**Entry point:** `agent_work_service.AgentWorkService.get_reviews`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [schemas_agent](../modules/schemas_agent.md), [time](../modules/time.md)

> Return the separate verifier-assignment queue.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `agent_service.AgentConflictError`
3. `schemas_agent.AgentReviewQueueResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [schemas_agent](../modules/schemas_agent.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.get_reviews`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
