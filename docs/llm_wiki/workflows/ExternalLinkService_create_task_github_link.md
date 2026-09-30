# ExternalLinkService_create_task_github_link

**Entry point:** `external_link_service.ExternalLinkService.create_task_github_link`
**Modules involved:** [commands](../modules/commands.md), [external_link_service](../modules/external_link_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [schemas_external_link](../modules/schemas_external_link.md)

> Parse and create a manual GitHub link for a task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_external_link.TaskExternalLinkCreate`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [external_link_service](../modules/external_link_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [schemas_external_link](../modules/schemas_external_link.md)

## Behavior

This workflow starts at `external_link_service.ExternalLinkService.create_task_github_link`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
