# NativeSessionService_connection

**Entry point:** `native_session_service.NativeSessionService.connection`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [native_session_service](../modules/native_session_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.digest`
2. `authority.AuthorityError`
3. `time.as_utc`
4. `time.utc_now`
5. `authority.AuthorityError`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [native_session_service](../modules/native_session_service.md)
- [time](../modules/time.md)

## Behavior

Looks up the hashed request identity and rejects absent, consumed, or expired requests. It does not reconstruct or replace a request identity.
