# workspace_member

**Entry point:** `identity.workspace_member`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [models_identity](../modules/models_identity.md), [routers_identity](../modules/routers_identity.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `identity_service.require_identity_writes`
3. `authority.AuthorityError`
4. `authority.AuthorityError`
5. `authority.internal_authority`
6. `authority.AuthorityError`
7. `models_identity.WorkspaceMembership`
8. `models_identity.CommandAudit`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [models_identity](../modules/models_identity.md)
- [routers_identity](../modules/routers_identity.md)

## Behavior

This workflow starts at `identity.workspace_member`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
