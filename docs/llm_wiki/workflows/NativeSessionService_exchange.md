# NativeSessionService_exchange

**Entry point:** `native_session_service.NativeSessionService.exchange`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [native_session_service](../modules/native_session_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.require_identity_writes`
2. `authority.internal_authority`
3. `identity_service.digest`
4. `authority.AuthorityError`
5. `time.as_utc`
6. `time.utc_now`
7. `authority.AuthorityError`
8. `time.utc_now`
9. `time.utc_now`
10. `authority.AuthorityError`
11. `identity_service.IdentityService`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [native_session_service](../modules/native_session_service.md)
- [time](../modules/time.md)

## Behavior

Checks the device verifier against the S256 challenge before revealing connection state. Pending consent produces a pending response. Approved exchange locks principal then session, rechecks enabled human identity and valid browser approval, and conditionally consumes the request in the same transaction as native session issuance. Replay or expiry fails explicitly.
