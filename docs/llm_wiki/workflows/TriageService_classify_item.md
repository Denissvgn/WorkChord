# TriageService_classify_item

**Entry point:** `triage_service.TriageService.classify_item`
**Modules involved:** [llm_service](../modules/llm_service.md), [models_triage](../modules/models_triage.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [triage_service](../modules/triage_service.md)

> Create an advisory classification suggestion for a triage item.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `llm_service.LLMService.from_runtime`
2. `models_triage.TriageClassificationSuggestion`
3. `outbound_webhook_service.emit_outbound_webhook_event`

## Touches

- [llm_service](../modules/llm_service.md)
- [models_triage](../modules/models_triage.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `triage_service.TriageService.classify_item`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
