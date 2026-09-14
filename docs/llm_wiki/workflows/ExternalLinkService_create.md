# ExternalLinkService_create

**Entry point:** `external_link_service.ExternalLinkService.create`
**Modules involved:** [external_link_service](../modules/external_link_service.md), [models_external_link](../modules/models_external_link.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [task_context_revision_service](../modules/task_context_revision_service.md)

> Create a generic external link.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_context_revision_service.reserve_task_context_revision`
2. `models_external_link.ExternalLink`
3. `outbound_webhook_service.emit_outbound_webhook_event`

## Touches

- [external_link_service](../modules/external_link_service.md)
- [models_external_link](../modules/models_external_link.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [task_context_revision_service](../modules/task_context_revision_service.md)

## Behavior

This workflow starts at `external_link_service.ExternalLinkService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
