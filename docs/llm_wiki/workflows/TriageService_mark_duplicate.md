# TriageService_mark_duplicate

**Entry point:** `triage_service.TriageService.mark_duplicate`
**Modules involved:** [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [request_source_service](../modules/request_source_service.md), [triage_service](../modules/triage_service.md)

> Mark a triage item as duplicate of another item or task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `request_source_service.RequestSourceService`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [request_source_service](../modules/request_source_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `triage_service.TriageService.mark_duplicate`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
