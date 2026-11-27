# TriageService_update

**Entry point:** `triage_service.TriageService.update`
**Modules involved:** [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [source_link_policy](../modules/source_link_policy.md), [triage_service](../modules/triage_service.md)

> Apply editable triage metadata updates.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source_link_policy.normalize_source_link`
2. `outbound_webhook_service.emit_outbound_webhook_event`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [source_link_policy](../modules/source_link_policy.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `triage_service.TriageService.update`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
