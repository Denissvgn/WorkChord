# import_new_iteration

**Entry point:** `export.import_new_iteration`
**Modules involved:** [commands](../modules/commands.md), [export](../modules/export.md), [iteration_service](../modules/iteration_service.md), [schemas_iteration](../modules/schemas_iteration.md)

> Import a new iteration from JSON export file.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.command_transaction`
2. `commands.planning_input_reservation`
3. `schemas_iteration.IterationCreate`
4. `iteration_service.IterationService`
5. `commands.lock_iterations`

## Touches

- [commands](../modules/commands.md)
- [export](../modules/export.md)
- [iteration_service](../modules/iteration_service.md)
- [schemas_iteration](../modules/schemas_iteration.md)

## Behavior

This workflow starts at `export.import_new_iteration`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
