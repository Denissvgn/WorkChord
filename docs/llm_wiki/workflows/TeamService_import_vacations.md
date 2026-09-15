# TeamService_import_vacations

**Entry point:** `team_service.TeamService.import_vacations`
**Modules involved:** [commands](../modules/commands.md), [schemas_team](../modules/schemas_team.md), [team_member](../modules/team_member.md), [team_service](../modules/team_service.md)

> Import vacation ranges for iteration team members from CSV text.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_team.VacationImportError`
2. `schemas_team.VacationImportError`
3. `schemas_team.VacationImportError`
4. `schemas_team.VacationImportError`
5. `schemas_team.VacationImportError`
6. `schemas_team.VacationImportError`
7. `schemas_team.VacationImportError`
8. `team_member.Vacation`
9. `commands.commit_or_flush`
10. `schemas_team.VacationImportResponse`

## Touches

- [commands](../modules/commands.md)
- [schemas_team](../modules/schemas_team.md)
- [team_member](../modules/team_member.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `team_service.TeamService.import_vacations`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
