# ExternalLinkService_update

**Entry point:** `external_link_service.ExternalLinkService.update`
**Modules involved:** [commands](../modules/commands.md), [external_link_service](../modules/external_link_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [task_context_revision_service](../modules/task_context_revision_service.md)

> Apply a partial external link update.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_context_revision_service.reserve_task_context_revision`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [external_link_service](../modules/external_link_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [task_context_revision_service](../modules/task_context_revision_service.md)

## Behavior

This workflow starts at `external_link_service.ExternalLinkService.update`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
