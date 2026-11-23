# AgentWorkService_get_work

**Entry point:** `agent_work_service.AgentWorkService.get_work`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [review_provenance](../modules/review_provenance.md), [schemas_agent](../modules/schemas_agent.md), [time](../modules/time.md)

> Return the authoritative resume/begin/wait/recovery decision.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `review_provenance.ReworkReadCache`
3. `agent_service.AgentConflictError`
4. `schemas_agent.AgentWorkDecisionResponse`
5. `agent_service.AgentConflictError`
6. `schemas_agent.AgentWorkDecisionResponse`
7. `agent_service.AgentConflictError`
8. `schemas_agent.AgentWorkDecisionResponse`
9. `time.as_utc`
10. `time.as_utc`
11. `time.as_utc`
12. `schemas_agent.AgentWorkDecisionResponse`
13. `schemas_agent.AgentWorkDecisionResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.get_work`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
