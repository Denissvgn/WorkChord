# IdentityService_issue_session

**Entry point:** `identity_service.IdentityService.issue_session`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [time](../modules/time.md), [user_session](../modules/user_session.md)

> Issue a session; a renewal passes the original sign-in time so its cap still applies.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `time.as_utc`
3. `authority.AuthorityError`
4. `authority.AuthorityError`
5. `authority.internal_authority`
6. `user_session.UserSession`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [time](../modules/time.md)
- [user_session](../modules/user_session.md)

## Behavior

This workflow starts at `identity_service.IdentityService.issue_session`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
