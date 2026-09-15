# IdentityService_issue_session

**Entry point:** `identity_service.IdentityService.issue_session`
**Modules involved:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [time](../modules/time.md), [user_session](../modules/user_session.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `user_session.UserSession`
3. `time.utc_now`
4. `time.utc_now`
5. `config.get_settings`

## Touches

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [time](../modules/time.md)
- [user_session](../modules/user_session.md)

## Behavior

This workflow starts at `identity_service.IdentityService.issue_session`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
