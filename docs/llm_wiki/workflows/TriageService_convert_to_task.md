# TriageService_convert_to_task

**Entry point:** `triage_service.TriageService.convert_to_task`
**Modules involved:** [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [request_source_service](../modules/request_source_service.md), [schemas_task](../modules/schemas_task.md), [schemas_triage](../modules/schemas_triage.md), [source_link_policy](../modules/source_link_policy.md), [task_brief_service](../modules/task_brief_service.md), [triage_service](../modules/triage_service.md)

> Convert a triage item to a planned task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source_link_policy.evaluate_source_link`
2. `schemas_triage.current_triage_brief`
3. `task_brief_service.brief_from_draft`
4. `schemas_task.TaskCreate`
5. `request_source_service.RequestSourceService.copy_triage_links_to_task`
6. `request_source_service.RequestSourceService`
7. `outbound_webhook_service.emit_outbound_webhook_event`
8. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [request_source_service](../modules/request_source_service.md)
- [schemas_task](../modules/schemas_task.md)
- [schemas_triage](../modules/schemas_triage.md)
- [source_link_policy](../modules/source_link_policy.md)
- [task_brief_service](../modules/task_brief_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `triage_service.TriageService.convert_to_task`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
