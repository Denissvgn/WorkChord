# callback

**Entry point:** `identity.callback`
**Modules involved:** [config](../modules/config.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.IdentityService`
2. `session_service.get_client_ip`
3. `session_service._cookie_options`
4. `config.get_settings`

## Touches

- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)
- [session_service](../modules/session_service.md)

## Behavior

This workflow starts at `identity.callback`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
