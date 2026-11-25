# TeamService_bind_profile_seed_key

**Entry point:** `team_service.TeamService.bind_profile_seed_key`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [models_identity](../modules/models_identity.md), [team_service](../modules/team_service.md)

> Bind a seed key once to an existing unkeyed profile, in place.

The profile row keeps its id, so capacity, availability, assignments and
history links stay attached. A seed key is not a scheduling input, so no
planning revision or task version advances. Agent credentials are refused
in every mode; only the operator or a trusted-local person may bind.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `commands.PlanningConflict`
3. `commands.PlanningConflict`
4. `commands.PlanningConflict`
5. `models_identity.CommandAudit`
6. `commands.commit_or_flush`
7. `commands.PlanningConflict`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [models_identity](../modules/models_identity.md)
- [team_service](../modules/team_service.md)

## Behavior

Binds a seed key once, in place, to an existing profile that has none; an already keyed profile is a conflict. The profile row keeps its id, so capacity, availability, assignments and history links stay attached. A seed key is not a scheduling input, so no planning revision or task version advances. Agent credentials are refused in every mode; only the workspace operator or a trusted-local person may bind.
