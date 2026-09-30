# AgentService_create_actor

**Entry point:** `agent_service.AgentService.create_actor`
**Modules involved:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [models_identity](../modules/models_identity.md)

> Create an actor and optional secret-free model binding atomically.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `models_agent.AgentActor`
2. `models_identity.Principal`
3. `models_agent.AgentModelBinding`
4. `models_agent.TaskEvent`
5. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [models_identity](../modules/models_identity.md)

## Behavior

This workflow starts at `agent_service.AgentService.create_actor`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
