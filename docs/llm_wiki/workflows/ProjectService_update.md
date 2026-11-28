# ProjectService_update

**Entry point:** `project_service.ProjectService.update`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [project_service](../modules/project_service.md), [time](../modules/time.md)

> Apply a partial project update, optionally deferring the commit.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `authority.require_operator`
3. `time.as_utc`
4. `outbound_webhook_service.emit_outbound_webhook_event`
5. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [project_service](../modules/project_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `project_service.ProjectService.update`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
