# NativeSessionService_deny

**Entry point:** `native_session_service.NativeSessionService.deny`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [native_session_service](../modules/native_session_service.md), [time](../modules/time.md)

> End a pending connection from the browser; the device's next exchange sees it as ended.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.require_identity_writes`
2. `authority.internal_authority`
3. `authority.AuthorityError`
4. `time.utc_now`
5. `authority.AuthorityError`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [native_session_service](../modules/native_session_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `native_session_service.NativeSessionService.deny`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
