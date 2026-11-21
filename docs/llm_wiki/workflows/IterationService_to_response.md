# IterationService_to_response

**Entry point:** `iteration_service.IterationService.to_response`
**Modules involved:** [calendar_rules](../modules/calendar_rules.md), [calendar_service](../modules/calendar_service.md), [iteration_service](../modules/iteration_service.md), [schemas_iteration](../modules/schemas_iteration.md)

> Build a public iteration response with computed calendar days.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `calendar_service.CalendarService`
2. `calendar_service.CalendarService.calculate_working_days`
3. `calendar_rules.AnnualCalendars.for_iteration`
4. `schemas_iteration.IterationResponse`

## Touches

- [calendar_rules](../modules/calendar_rules.md)
- [calendar_service](../modules/calendar_service.md)
- [iteration_service](../modules/iteration_service.md)
- [schemas_iteration](../modules/schemas_iteration.md)

## Behavior

This workflow starts at `iteration_service.IterationService.to_response`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
