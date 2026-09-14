# AgentPlanningService__execute

**Entry point:** `agent_planning_service.AgentPlanningService._execute`
**Modules involved:** [agent_planning_service](../modules/agent_planning_service.md), [agent_service](../modules/agent_service.md), [models_agent](../modules/models_agent.md), [schemas_agent_planning](../modules/schemas_agent_planning.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.require_scope`
2. `agent_service.validate_idempotency_key`
3. `schemas_agent_planning.AgentPlanningReceipt`
4. `models_agent.AgentIdempotencyRecord`

## Touches

- [agent_planning_service](../modules/agent_planning_service.md)
- [agent_service](../modules/agent_service.md)
- [models_agent](../modules/models_agent.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)

## Behavior

This workflow starts at `agent_planning_service.AgentPlanningService._execute`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
