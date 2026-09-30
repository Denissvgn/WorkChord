# IdentityService_begin_login

**Entry point:** `identity_service.IdentityService.begin_login`
**Modules involved:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [models_identity](../modules/models_identity.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `models_identity.OIDCLoginAttempt`
3. `time.utc_now`
4. `config.get_settings`
5. `config.get_settings`

## Touches

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [models_identity](../modules/models_identity.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `identity_service.IdentityService.begin_login`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
