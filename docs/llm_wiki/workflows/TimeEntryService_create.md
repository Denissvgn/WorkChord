# TimeEntryService_create

**Entry point:** `time_entry_service.TimeEntryService.create`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [models_time_entry](../modules/models_time_entry.md), [time](../modules/time.md), [time_entry_service](../modules/time_entry_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `commands.PlanningConflict`
3. `authority.internal_authority`
4. `authority.internal_authority`
5. `time.utc_now`
6. `models_time_entry.TimeEntry`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [models_time_entry](../modules/models_time_entry.md)
- [time](../modules/time.md)
- [time_entry_service](../modules/time_entry_service.md)

## Behavior

This workflow starts at `time_entry_service.TimeEntryService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
