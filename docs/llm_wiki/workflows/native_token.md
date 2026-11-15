# native_token

**Entry point:** `identity.native_token`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md)

> Exchange a browser session for a native one, or renew a native or observer session.

A bearer caller is rotated: its old token ends when the new one is issued.
Every successor keeps the caller's access level and original sign-in time,
so renewal stops at the absolute cap.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `authority.internal_authority`
3. `session_service._get_session_by_token`
4. `authority.AuthorityError`
5. `identity_service.IdentityService`
6. `session_service.get_client_ip`
7. `identity_service.session_grant`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)
- [session_service](../modules/session_service.md)

## Behavior

This workflow starts at `identity.native_token`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
