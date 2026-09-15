# link_profile

**Entry point:** `identity.link_profile`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [models_identity](../modules/models_identity.md), [routers_identity](../modules/routers_identity.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `identity_service.require_identity_writes`
3. `authority.internal_authority`
4. `authority.AuthorityError`
5. `authority.AuthorityError`
6. `models_identity.PrincipalProfileLink`
7. `models_identity.CommandAudit`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [models_identity](../modules/models_identity.md)
- [routers_identity](../modules/routers_identity.md)

## Behavior

This workflow starts at `identity.link_profile`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
