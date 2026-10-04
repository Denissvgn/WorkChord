# NativeSessionService_start

**Entry point:** `native_session_service.NativeSessionService.start`
**Modules involved:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [native_connection](../modules/native_connection.md), [native_session_service](../modules/native_session_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.require_identity_writes`
2. `config.get_settings`
3. `authority.AuthorityError`
4. `time.utc_now`
5. `identity_service.digest`
6. `authority.internal_authority`
7. `authority.AuthorityError`
8. `native_connection.NativeConnection`
9. `identity_service.digest`

## Touches

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [native_connection](../modules/native_connection.md)
- [native_session_service](../modules/native_session_service.md)
- [time](../modules/time.md)

## Behavior

Creates a ten-minute request with a hashed random identity, an S256 challenge, and a displayed verification code. It uses managed authentication, bounded attempt counts and bounded expired-request cleanup. The response points to a local browser consent path and carries no access token or device verifier.
