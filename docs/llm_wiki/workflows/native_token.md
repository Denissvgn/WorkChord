# native_token

**Entry point:** `identity.native_token`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `identity_service.IdentityService`
3. `session_service.get_client_ip`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)
- [session_service](../modules/session_service.md)

## Behavior

This workflow starts at `identity.native_token`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
