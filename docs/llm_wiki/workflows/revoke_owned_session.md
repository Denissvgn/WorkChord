# revoke_owned_session

**Entry point:** `identity.revoke_owned_session`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.require_identity_writes`
2. `authority.AuthorityError`
3. `authority.internal_authority`
4. `authority.AuthorityError`
5. `time.utc_now`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `identity.revoke_owned_session`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
