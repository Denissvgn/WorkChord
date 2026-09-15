# RequestSourceService_create_link

**Entry point:** `request_source_service.RequestSourceService.create_link`
**Modules involved:** [commands](../modules/commands.md), [models_request_source](../modules/models_request_source.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [request_source_service](../modules/request_source_service.md), [task_context_revision_service](../modules/task_context_revision_service.md)

> Create a link from an existing or new request source.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_context_revision_service.reserve_task_context_revision`
2. `models_request_source.RequestSourceLink`
3. `outbound_webhook_service.emit_outbound_webhook_event`
4. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [models_request_source](../modules/models_request_source.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [request_source_service](../modules/request_source_service.md)
- [task_context_revision_service](../modules/task_context_revision_service.md)

## Behavior

This workflow starts at `request_source_service.RequestSourceService.create_link`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
