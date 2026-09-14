# AgentWorkService_get_work

**Entry point:** `agent_work_service.AgentWorkService.get_work`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [schemas_agent](../modules/schemas_agent.md), [time](../modules/time.md)

> Return the authoritative resume/begin/wait/recovery decision.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `agent_service.AgentConflictError`
3. `schemas_agent.AgentWorkDecisionResponse`
4. `agent_service.AgentConflictError`
5. `schemas_agent.AgentWorkDecisionResponse`
6. `agent_service.AgentConflictError`
7. `schemas_agent.AgentWorkDecisionResponse`
8. `time.as_utc`
9. `time.as_utc`
10. `time.as_utc`
11. `schemas_agent.AgentWorkDecisionResponse`
12. `schemas_agent.AgentWorkDecisionResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [schemas_agent](../modules/schemas_agent.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.get_work`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
