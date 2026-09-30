# TeamService_import_members

**Entry point:** `team_service.TeamService.import_members`
**Modules involved:** [commands](../modules/commands.md), [import_parser](../modules/import_parser.md), [team_member](../modules/team_member.md), [team_service](../modules/team_service.md)

> Import multiple team members from text format.

Format:
-- "John Doe" Developer 100 1.0 20
-- "Jane Smith" Designer 80 1.2 15

Returns list of created team members.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `import_parser.parse_team_members_text`
2. `team_member.TeamMember`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [import_parser](../modules/import_parser.md)
- [team_member](../modules/team_member.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `team_service.TeamService.import_members`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
