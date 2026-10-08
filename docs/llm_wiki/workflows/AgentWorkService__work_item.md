# AgentWorkService__work_item

**Entry point:** `agent_work_service.AgentWorkService._work_item`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [schemas_agent](../modules/schemas_agent.md), [services_work_metrics](../modules/services_work_metrics.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentConflictError`
2. `time.as_utc`
3. `time.as_utc`
4. `services_work_metrics.effective_work_flags`
5. `schemas_agent.AgentWorkItem`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [schemas_agent](../modules/schemas_agent.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService._work_item`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
