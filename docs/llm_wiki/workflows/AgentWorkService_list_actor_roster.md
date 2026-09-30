# AgentWorkService_list_actor_roster

**Entry point:** `agent_work_service.AgentWorkService.list_actor_roster`
**Modules involved:** [agent_model_catalog_service](../modules/agent_model_catalog_service.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [agent_work_service](../modules/agent_work_service.md), [query_limits](../modules/query_limits.md), [schemas_agent](../modules/schemas_agent.md)

> Return bounded exact-actor/profile/binding evidence without key material.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_setup_service.AgentTeamSetupService`
2. `query_limits.CollectionLimitExceededError`
3. `agent_model_catalog_service.AgentModelCatalogService`
4. `schemas_agent.AgentActorRosterItem`

## Touches

- [agent_model_catalog_service](../modules/agent_model_catalog_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [query_limits](../modules/query_limits.md)
- [schemas_agent](../modules/schemas_agent.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.list_actor_roster`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
