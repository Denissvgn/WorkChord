# AgentService_renew_claim

**Entry point:** `agent_service.AgentService.renew_claim`
**Modules involved:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [time](../modules/time.md)

> Renew a task lease.

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

This workflow starts at `agent_service.AgentService.renew_claim`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
