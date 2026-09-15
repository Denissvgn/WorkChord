# logout

**Entry point:** `identity.logout`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.require_identity_writes`
2. `authority.internal_authority`
3. `time.utc_now`
4. `session_service._cookie_options`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)
- [session_service](../modules/session_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `identity.logout`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
