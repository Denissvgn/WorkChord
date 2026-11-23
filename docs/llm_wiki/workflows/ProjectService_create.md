# ProjectService_create

**Entry point:** `project_service.ProjectService.create`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [models_project](../modules/models_project.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [project_service](../modules/project_service.md)

> Create a project, optionally leaving commit ownership to the caller.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `models_project.Project`
3. `outbound_webhook_service.emit_outbound_webhook_event`
4. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [models_project](../modules/models_project.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [project_service](../modules/project_service.md)

## Behavior

This workflow starts at `project_service.ProjectService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
