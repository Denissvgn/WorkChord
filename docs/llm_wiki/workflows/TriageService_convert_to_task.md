# TriageService_convert_to_task

**Entry point:** `triage_service.TriageService.convert_to_task`
**Modules involved:** [outbound_webhook_service](../modules/outbound_webhook_service.md), [request_source_service](../modules/request_source_service.md), [schemas_task](../modules/schemas_task.md), [triage_service](../modules/triage_service.md)

> Convert a triage item to a planned task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_task.TaskCreate`
2. `request_source_service.RequestSourceService`
3. `outbound_webhook_service.emit_outbound_webhook_event`

## Touches

- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [request_source_service](../modules/request_source_service.md)
- [schemas_task](../modules/schemas_task.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `triage_service.TriageService.convert_to_task`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
