# AgentService_authenticate

**Entry point:** `agent_service.AgentService.authenticate`
**Modules involved:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [config](../modules/config.md), [time](../modules/time.md)

> Authenticate an API key against stored enabled agent actors.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `time.utc_now`
3. `time.as_utc`
4. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_service.AgentService.authenticate`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
