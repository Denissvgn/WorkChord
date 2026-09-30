# ProjectService_create

**Entry point:** `project_service.ProjectService.create`
**Modules involved:** [commands](../modules/commands.md), [models_project](../modules/models_project.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [project_service](../modules/project_service.md)

> Create a project, optionally leaving commit ownership to the caller.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `models_project.Project`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [models_project](../modules/models_project.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [project_service](../modules/project_service.md)

## Behavior

This workflow starts at `project_service.ProjectService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
