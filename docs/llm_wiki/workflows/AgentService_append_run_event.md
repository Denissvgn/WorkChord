# AgentService_append_run_event

**Entry point:** `agent_service.AgentService.append_run_event`
**Modules involved:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [time](../modules/time.md)

> Append an event to an agent run.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `models_agent.AgentRunEvent`
2. `time.utc_now`
3. `outbound_webhook_service.emit_outbound_webhook_event`
4. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_service.AgentService.append_run_event`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
