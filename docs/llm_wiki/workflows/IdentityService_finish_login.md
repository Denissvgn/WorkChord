# IdentityService_finish_login

**Entry point:** `identity_service.IdentityService.finish_login`
**Modules involved:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [models_identity](../modules/models_identity.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `time.as_utc`
3. `time.utc_now`
4. `authority.AuthorityError`
5. `time.utc_now`
6. `authority.AuthorityError`
7. `config.get_settings`
8. `config.get_settings`
9. `config.get_settings`
10. `config.get_settings`
11. `models_identity.Principal`
12. `models_identity.IdentitySubject`
13. `authority.AuthorityError`

## Touches

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [models_identity](../modules/models_identity.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `identity_service.IdentityService.finish_login`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
