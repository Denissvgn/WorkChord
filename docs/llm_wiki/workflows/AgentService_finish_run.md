# AgentService_finish_run

**Entry point:** `agent_service.AgentService.finish_run`
**Modules involved:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [time](../modules/time.md)

> Finish an agent run and attach final trace metadata.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_service.AgentService.finish_run`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
