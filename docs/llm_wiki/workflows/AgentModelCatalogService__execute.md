# AgentModelCatalogService__execute

**Entry point:** `agent_model_catalog_service.AgentModelCatalogService._execute`
**Modules involved:** [agent_model_catalog_service](../modules/agent_model_catalog_service.md), [agent_routing](../modules/agent_routing.md), [agent_service](../modules/agent_service.md), [models_agent](../modules/models_agent.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.require_scope`
2. `agent_service.AgentPermissionError`
3. `agent_service.validate_idempotency_key`
4. `agent_routing.AgentModelMutationReceipt`
5. `models_agent.AgentIdempotencyRecord`

## Touches

- [agent_model_catalog_service](../modules/agent_model_catalog_service.md)
- [agent_routing](../modules/agent_routing.md)
- [agent_service](../modules/agent_service.md)
- [models_agent](../modules/models_agent.md)

## Behavior

This workflow starts at `agent_model_catalog_service.AgentModelCatalogService._execute`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
