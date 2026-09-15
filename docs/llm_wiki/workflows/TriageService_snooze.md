# TriageService_snooze

**Entry point:** `triage_service.TriageService.snooze`
**Modules involved:** [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [time](../modules/time.md), [triage_service](../modules/triage_service.md)

> Snooze a triage item until a future time.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.as_utc`
2. `time.utc_now`
3. `outbound_webhook_service.emit_outbound_webhook_event`
4. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [time](../modules/time.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `triage_service.TriageService.snooze`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
