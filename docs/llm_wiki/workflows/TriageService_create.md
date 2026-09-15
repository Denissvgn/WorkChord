# TriageService_create

**Entry point:** `triage_service.TriageService.create`
**Modules involved:** [commands](../modules/commands.md), [models_triage](../modules/models_triage.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [triage_service](../modules/triage_service.md)

> Create a triage item.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `models_triage.TriageItem`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [models_triage](../modules/models_triage.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `triage_service.TriageService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
