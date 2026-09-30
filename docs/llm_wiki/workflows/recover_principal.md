# recover_principal

**Entry point:** `identity.recover_principal`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [models_identity](../modules/models_identity.md), [routers_identity](../modules/routers_identity.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `identity_service.require_identity_writes`
3. `authority.internal_authority`
4. `authority.AuthorityError`
5. `time.utc_now`
6. `models_identity.CommandAudit`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [models_identity](../modules/models_identity.md)
- [routers_identity](../modules/routers_identity.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `identity.recover_principal`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
