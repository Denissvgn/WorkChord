# IterationService_create

**Entry point:** `iteration_service.IterationService.create`
**Modules involved:** [calendar_service](../modules/calendar_service.md), [commands](../modules/commands.md), [iteration_service](../modules/iteration_service.md), [models_iteration](../modules/models_iteration.md)

> Create an iteration, optionally leaving commit ownership to the caller.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `models_iteration.Iteration`
3. `calendar_service.CalendarService.selected_years`
4. `calendar_service.CalendarService`
5. `commands.commit_or_flush`

## Touches

- [calendar_service](../modules/calendar_service.md)
- [commands](../modules/commands.md)
- [iteration_service](../modules/iteration_service.md)
- [models_iteration](../modules/models_iteration.md)

## Behavior

This workflow starts at `iteration_service.IterationService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
