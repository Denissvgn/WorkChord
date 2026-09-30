# login

**Entry point:** `identity.login`
**Modules involved:** [config](../modules/config.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.IdentityService`
2. `session_service._cookie_options`
3. `config.get_settings`
4. `session_service._get_session_by_token`

## Touches

- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)
- [session_service](../modules/session_service.md)

## Behavior

This workflow starts at `identity.login`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
