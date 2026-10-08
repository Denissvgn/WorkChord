# prospective_member_profiles

**Entry point:** `planning_input_context.prospective_member_profiles`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [import_parser](../modules/import_parser.md), [planning_input_context](../modules/planning_input_context.md), [team_service](../modules/team_service.md)

> Resolve import and allocation intent without creating profiles or changing data.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.PlanningConflict`
2. `import_parser.parse_team_members_text`
3. `authority.internal_authority`
4. `commands.PlanningConflict`
5. `commands.PlanningConflict`
6. `commands.PlanningConflict`
7. `team_service.TeamService`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [import_parser](../modules/import_parser.md)
- [planning_input_context](../modules/planning_input_context.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `planning_input_context.prospective_member_profiles`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
