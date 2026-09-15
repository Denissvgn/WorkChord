# RequestSourceService_unlink

**Entry point:** `request_source_service.RequestSourceService.unlink`
**Modules involved:** [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [request_source_service](../modules/request_source_service.md), [task_context_revision_service](../modules/task_context_revision_service.md)

> Remove a request-source link without deleting the source.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_context_revision_service.reserve_task_context_revision`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [request_source_service](../modules/request_source_service.md)
- [task_context_revision_service](../modules/task_context_revision_service.md)

## Behavior

This workflow starts at `request_source_service.RequestSourceService.unlink`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
