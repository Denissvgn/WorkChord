# project_member

**Entry point:** `identity.project_member`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [models_identity](../modules/models_identity.md), [routers_identity](../modules/routers_identity.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `identity_service.require_identity_writes`
3. `authority.AuthorityError`
4. `authority.internal_authority`
5. `authority.AuthorityError`
6. `models_identity.ProjectMembership`
7. `models_identity.CommandAudit`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [models_identity](../modules/models_identity.md)
- [routers_identity](../modules/routers_identity.md)

## Behavior

This workflow starts at `identity.project_member`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
