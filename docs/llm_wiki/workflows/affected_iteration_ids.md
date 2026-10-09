# affected_iteration_ids

**Entry point:** `planning_input_context.affected_iteration_ids`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [planning_input_context](../modules/planning_input_context.md)

> Resolve one complete scope for both read observations and atomic writes.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `authority.require_operator`
3. `authority.require_project`
4. `authority.internal_authority`
5. `commands.PlanningConflict`
6. `authority.AuthorityError`
7. `authority.AuthorityError`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [planning_input_context](../modules/planning_input_context.md)

## Behavior

This workflow starts at `planning_input_context.affected_iteration_ids`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
