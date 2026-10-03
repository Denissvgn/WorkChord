# NativeSessionService_approve

**Entry point:** `native_session_service.NativeSessionService.approve`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [native_session_service](../modules/native_session_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.require_identity_writes`
2. `authority.internal_authority`
3. `authority.AuthorityError`
4. `authority.AuthorityError`
5. `time.utc_now`
6. `authority.AuthorityError`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [native_session_service](../modules/native_session_service.md)
- [time](../modules/time.md)

## Behavior

Requires a human session and the matching displayed code. Normal HTTP cookie mutations retain CSRF and Origin checks. A conditional update binds the request to the approving session; another session cannot replace that approval.
