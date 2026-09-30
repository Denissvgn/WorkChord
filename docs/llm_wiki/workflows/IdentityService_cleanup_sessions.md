# IdentityService_cleanup_sessions

**Entry point:** `identity_service.IdentityService.cleanup_sessions`
**Modules involved:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `time.utc_now`
3. `config.get_settings`
4. `authority.internal_authority`
5. `time.utc_now`
6. `time.utc_now`

## Touches

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `identity_service.IdentityService.cleanup_sessions`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
