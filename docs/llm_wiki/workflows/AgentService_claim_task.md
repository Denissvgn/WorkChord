# AgentService_claim_task

**Entry point:** `agent_service.AgentService.claim_task`
**Modules involved:** [agent_readiness](../modules/agent_readiness.md), [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [maintenance_window_service](../modules/maintenance_window_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [time](../modules/time.md)

> Claim a task lease for an agent.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `maintenance_window_service.require_start_admission`
2. `time.utc_now`
3. `agent_readiness.evaluate_agent_readiness`
4. `time.as_utc`
5. `outbound_webhook_service.emit_outbound_webhook_event`
6. `commands.commit_or_flush`

## Touches

- [agent_readiness](../modules/agent_readiness.md)
- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [maintenance_window_service](../modules/maintenance_window_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_service.AgentService.claim_task`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
