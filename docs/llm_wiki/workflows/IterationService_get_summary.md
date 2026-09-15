# IterationService_get_summary

**Entry point:** `iteration_service.IterationService.get_summary`
**Modules involved:** [calendar_service](../modules/calendar_service.md), [iteration_service](../modules/iteration_service.md), [schemas_iteration](../modules/schemas_iteration.md), [services_work_metrics](../modules/services_work_metrics.md)

> Get iteration summary with statistics.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `calendar_service.CalendarService`
2. `services_work_metrics.aggregate_metrics`
3. `schemas_iteration.IterationSummary`

## Touches

- [calendar_service](../modules/calendar_service.md)
- [iteration_service](../modules/iteration_service.md)
- [schemas_iteration](../modules/schemas_iteration.md)
- [services_work_metrics](../modules/services_work_metrics.md)

## Behavior

This workflow starts at `iteration_service.IterationService.get_summary`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
