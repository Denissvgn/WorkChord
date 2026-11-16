# AgentService_start_run

**Entry point:** `agent_service.AgentService.start_run`
**Modules involved:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [schemas_agent](../modules/schemas_agent.md), [time](../modules/time.md)

> Start an agent run.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `models_agent.AgentRun`
2. `schemas_agent.declared_harness`
3. `schemas_agent.declared_harness`
4. `time.utc_now`
5. `outbound_webhook_service.emit_outbound_webhook_event`
6. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [schemas_agent](../modules/schemas_agent.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_service.AgentService.start_run`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
