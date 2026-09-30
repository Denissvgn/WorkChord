# ReleaseService_create_for_project

**Entry point:** `release_service.ReleaseService.create_for_project`
**Modules involved:** [commands](../modules/commands.md), [models_release](../modules/models_release.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [release_service](../modules/release_service.md)

> Create a release for a project.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `models_release.Release`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `outbound_webhook_service.emit_outbound_webhook_event`
4. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [models_release](../modules/models_release.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [release_service](../modules/release_service.md)

## Behavior

This workflow starts at `release_service.ReleaseService.create_for_project`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
