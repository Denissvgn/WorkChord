# AgentService_start_run

**Entry point:** `agent_service.AgentService.start_run`
**Modules involved:** [agent_service](../modules/agent_service.md), [models_agent](../modules/models_agent.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [time](../modules/time.md)

> Start an agent run.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `models_agent.AgentRun`
2. `time.utc_now`
3. `outbound_webhook_service.emit_outbound_webhook_event`

## Touches

- [agent_service](../modules/agent_service.md)
- [models_agent](../modules/models_agent.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_service.AgentService.start_run`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
